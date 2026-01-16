# 首先检查文件是否存在
import os

print("当前目录文件列表:")
for file in os.listdir('.'):
    print(file)

print("\n尝试读取数据文件...")
try:
    import pandas as pd
    # 读取数据
    df = pd.read_parquet('df_sysaccesslogtestds_20260115T100453Z_b2d9ed105d9844c385e88baf84887285.parquet')
    print(f"成功读取数据，行数: {len(df)}")
    
    # 简单的统计
    print(f"\n总访问量: {len(df)} 次")
    
    # ACTION统计
    action_counts = df['ACTION'].value_counts()
    print("\n=== ACTION统计 ===")
    for action, count in action_counts.items():
        percent = (count / len(df) * 100)
        print(f"{action}: {count}次 ({percent:.2f}%)")
        
except Exception as e:
    print(f"读取数据时出错: {e}")
    print(f"错误类型: {type(e)}")