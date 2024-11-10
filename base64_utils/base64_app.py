import streamlit as st
import base64, io
import pandas as pd

st.set_page_config(page_title="Base64 App", page_icon="🔢")
st.title("Base64 App 🔢")

base64_txt = st.secrets["base64_txt"]
decoded_txt = base64.b64decode(base64_txt).decode('utf-8')

# Try different CSV parsing options
df = pd.read_csv(io.StringIO(decoded_txt))
st.dataframe(df)