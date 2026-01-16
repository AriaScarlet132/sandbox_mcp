import os
import sys

# 尝试列出当前目录
print("Python版本:", sys.version)
print("当前目录:", os.getcwd())

# 尝试列出文件
try:
    files = os.listdir('.')
    print("目录中的文件:")
    for f in files:
        print(f"  - {f}")
except Exception as e:
    print(f"列出文件时出错: {e}")

# 检查是否有parquet文件
parquet_files = []
for f in files:
    if f.endswith('.parquet'):
        parquet_files.append(f)
        
print(f"\n找到的parquet文件: {parquet_files}")