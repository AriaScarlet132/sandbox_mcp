import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import os

# 首先检查文件是否存在
print("当前目录内容：")
print(os.listdir('.'))

# 读取parquet文件
print("\n正在读取df_sysaccesslogtestds.parquet文件...")
try:
    df = pd.read_parquet('df_sysaccesslogtestds.parquet')
    print(f"文件读取成功！数据形状：{df.shape}")
    print(f"列名：{df.columns.tolist()}")
    print("\n前5行数据预览：")
    print(df.head())
except Exception as e:
    print(f"读取文件时出错：{e}")