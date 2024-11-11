import streamlit as st
from urllib.parse import unquote
import pandas as pd
from datetime import datetime
from urllib.parse import quote
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="Knowledge Base", page_icon="📚")
st.logo("img/knowledge_logo_horizontal_3_colors.png", size="large")

# Initialize Supabase connection
supabase = st.connection("supabase", type=SupabaseConnection)

# Initialize page in session state if it doesn't exist
if 'page' not in st.session_state:
    st.session_state.page = 1

if 'user_id' not in st.session_state:
    st.session_state.user_id = None

@st.cache_data
def load_data():
    # df = pd.read_csv('diigo/diigo_csv_2024_11_09_lite.csv')
    df = supabase.table('articles').select("*").eq('user_id', st.session_state.user_id).execute()
    df = pd.DataFrame(df.data).set_index('id')
    return df

# Function to create clickable tags
def display_tags(tags_str):
    tags = tags_str.split(',')
    tag_links = []
    for tag in tags:
        tag = tag.strip()
        if tag:  # Only display non-empty tags
            encoded_tag = quote(tag)
            tag_links.append(f"[`{tag}`](/?tag={encoded_tag})")
    
    # Join all tags with separator and display in a single line
    st.markdown(" | ".join(tag_links), unsafe_allow_html=True)

# Add this after the data loading
def get_tag_counts(df):
    # Split and flatten all tags
    all_tags = [tag.strip() 
                for tags in df.tags.str.split(',') 
                for tag in tags if tag.strip()]
    
    # Count occurrences of each tag
    tag_counts = pd.Series(all_tags).value_counts()
    return tag_counts


st.markdown("""
    <style>
    .stSidebar {
        background-color: #f8f9fa;
    }
    .stSidebar a {
        color: #444;
        text-decoration: none;
    }
    .stSidebar a:hover {
        color: #000;
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# Get URL parameters
selected_tag = unquote(st.query_params.get('tag', ''))
view_mode = st.query_params.get('view', '')


# User Authentication Section
if st.session_state.user_id is None:
    # st.subheader('Log in')
    with st.form("Sign in"):
        st.write("**Log in**")
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input(label="Enter your email ID")
        with col2:
            password = st.text_input(
            label="Enter your password",
            placeholder="Min 6 characters",
            type="password",
            help="Password is encrypted",
        )
        if st.form_submit_button('Login📚'):
            try:
                response = supabase.auth.sign_in_with_password({"email": email, "password": password}) 
                st.session_state.user_id = response.user.id
                st.session_state.user_email = response.user.email
                st.rerun()
            except Exception as e:
                st.error(str(e), icon="❌")
    st.write("To get early access to the Knowledge Base, email slevin.an209@gadz.org")
   

else:
    # Read and prepare data
    df = load_data()
    df.tags = df.tags.fillna('')

    # st.sidebar.title("📚 Knowledge Base")

    # Filter data if a tag is selected
    if selected_tag:
        df = df[df.tags.str.contains(selected_tag, case=False, na=False)]
        st.subheader(f"🏷️ Tag: {selected_tag}")
        

    # Handle special views (all_tags or top_300)
    if view_mode in ['all_tags', 'top_300']:
        tag_counts = get_tag_counts(df)
        st.header("All Tags" if view_mode == 'all_tags' else "Top 300 Tags")
        
        # Determine how many tags to show
        n_tags = len(tag_counts) if view_mode == 'all_tags' else 300
        
        # Create a multi-column layout for tags
        cols = st.columns(3)
        for idx, (tag, count) in enumerate(tag_counts.head(n_tags).items()):
            with cols[idx % 3]:
                encoded_tag = quote(tag)
                st.markdown(f"[{tag}](/?tag={encoded_tag}) ({count})")
        st.stop()  # Stop rendering the rest of the app for these views

    # Add pagination controls
    total_pages = len(df) // 24 + (1 if len(df) % 24 > 0 else 0)

    # Calculate start and end indices for current page
    start_idx = (st.session_state.page - 1) * 24
    end_idx = min(start_idx + 24, len(df))

    # Add page navigation with inline page selector at the top
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
    with col1:
        st.write(f"{len(df)} items") # , 24 items/page
        # st.write(f"{start_idx + 1}-{end_idx}")
    with col2:
        if st.session_state.page > 1:
            if st.button("←", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()
    with col3:
        # Center-align the page selector and update session state when changed
        new_page = st.number_input("Page number", min_value=1, max_value=total_pages, 
                                value=st.session_state.page,
                                key="page_selector",
                                label_visibility="collapsed")
        if new_page != st.session_state.page:
            st.session_state.page = new_page
            st.rerun()
    with col4:
        if st.session_state.page < total_pages:
            if st.button("→", use_container_width=True):
                st.session_state.page += 1
                st.rerun()


    # Add sidebar
    with st.sidebar:
        st.header("🔝 Top Tags")
        
        # Get tag counts
        tag_counts = get_tag_counts(df)
        
        # Display top tags with counts
        for tag, count in tag_counts.head(10).items():
            encoded_tag = quote(tag)
            st.markdown(f"[{tag}](/?tag={encoded_tag}) ({count})")
        
        # Add links to view all tags
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("[All tags](/?view=all_tags)")
        with col2:
            st.markdown("[Top 300](/?view=top_300)")
        
        if st.toggle("Debug mode", value=False):
            st.write(df)

    # Display entries for current page only
    for idx in range(start_idx, end_idx):
        row = df.iloc[idx]
        # Title as clickable link
        st.markdown(f"### [{row['title']}]({row['url']})")
        
        # Create columns for tags and date
        col1, col2 = st.columns([3, 1])
        with col1:
            display_tags(row['tags'])
        with col2:
            # Update datetime parsing to handle ISO format
            created_date = datetime.fromisoformat(row['created_at'].replace('Z', '+00:00'))
            st.write(created_date.strftime('%B %d, %Y'))
        
        # Add a separator between entries
        st.markdown("---")