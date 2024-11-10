# %%

import pandas as pd
df = pd.read_csv('../diigo/diigo_csv_2024_11_09_lite.csv')

# extract 42 first lines
df = df.head(42)
print(df.shape)

df.to_csv('../diigo/diigo_csv_2024_11_09_extract_42.csv', index=False)

# %%

import base64

with open('../diigo/diigo_csv_2024_11_09_extract_42.csv', 'r', encoding='utf-8') as f:
    txt = f.read()

# print(txt)
# %%

# encode to base64
base64_txt = base64.b64encode(txt.encode('utf-8')).decode('utf-8')

# print(base64_txt)

# compute length
print(len(base64_txt))

# %%
with open('../diigo/diigo_csv_2024_11_09_extract_42_base64.txt', 'w', encoding='utf-8') as f:
    f.write(base64_txt)
