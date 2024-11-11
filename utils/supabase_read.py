
# %%
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

# %% Works only with RLS disabled
try:
    response = supabase.table('articles').select("*").limit(24).execute()
    records = response.data
    
    # Convert to DataFrame for better viewing (optional)
    df_result = pd.DataFrame(records).set_index('id')
    print(df_result)
except Exception as e:
    print(f"Error fetching records: {str(e)}")

# %%
