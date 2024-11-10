import streamlit as st
import base64
import pandas as pd
import io
import csv

st.set_page_config(page_title="Base64 App", page_icon="🔢")
st.title("Base64 App 🔢")

base64_txt = st.secrets["base64_txt"]

# Add padding if necessary
while len(base64_txt) % 4 != 0:
    base64_txt += '='

try:
    # decode base64
    decoded_txt = base64.b64decode(base64_txt).decode('utf-8')
    
    # Debug: Show raw decoded text
    st.text("Raw decoded text:")
    st.text(decoded_txt[:500] + "...")  # Show first 500 chars
    
    # Try different CSV parsing options
    df = pd.read_csv(
        io.StringIO(decoded_txt),
        on_bad_lines='skip',      # Skip problematic lines
        escapechar='\\',          # Handle escaped characters
        quoting=csv.QUOTE_ALL,    # Try stricter quote handling
        lineterminator='\n'       # Explicitly set line terminator
    )
    st.dataframe(df)
    
    # Show parsing stats
    st.text(f"Successfully parsed {len(df)} rows")
except Exception as e:
    st.error(f"Error decoding base64 string: {str(e)}")
    # Debug: Show the problematic text around error
    if 'decoded_txt' in locals():
        st.text("Decoded text sample around error:")
        lines = decoded_txt.split('\n')
        if len(lines) >= 46:
            st.text("\n".join(lines[44:48]))  # Show lines around line 46
