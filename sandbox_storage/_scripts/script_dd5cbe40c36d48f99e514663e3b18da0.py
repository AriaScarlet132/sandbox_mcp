import pandas as pd
df = pd.read_parquet('demo_test.parquet')
print(df.head().to_string(index=False))
