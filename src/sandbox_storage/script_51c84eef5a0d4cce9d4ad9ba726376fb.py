import os

# 检查当前目录和文件
print("当前工作目录：", os.getcwd())
print("\n目录内容：")
for item in os.listdir('.'):
    print(f"  {item}")

# 检查是否有parquet文件
parquet_files = [f for f in os.listdir('.') if f.endswith('.parquet')]
print(f"\n找到的parquet文件：{parquet_files}")