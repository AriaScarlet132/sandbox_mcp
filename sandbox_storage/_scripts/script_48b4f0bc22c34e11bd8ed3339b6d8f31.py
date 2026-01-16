import pandas as pd
import numpy as np

# 读取数据
df = pd.read_parquet("df_sysaccesslogtestds_20260116T022357Z_8e35a1673ae24250bc0644700fef040b.parquet")

print("数据基本信息:")
print(f"总行数: {len(df)}")
print(f"字段数: {len(df.columns)}")
print("\n字段列表:")
for col in df.columns:
    print(f"- {col}")

print("\n" + "="*50)
print("ACTION字段统计:")
print("="*50)

# 统计ACTION字段的分布
action_counts = df['ACTION'].value_counts()
action_percentages = (action_counts / len(df) * 100).round(2)

# 创建统计结果DataFrame
action_stats = pd.DataFrame({
    'ACTION类型': action_counts.index,
    '数量': action_counts.values,
    '占比(%)': action_percentages.values
})

# 按数量降序排序
action_stats = action_stats.sort_values('数量', ascending=False)

print(f"\nACTION类型总数: {len(action_counts)}")
print("\nACTION类型统计详情:")
print(action_stats.to_string(index=False))

# 计算累计占比
action_stats['累计占比(%)'] = action_stats['占比(%)'].cumsum()
print("\nACTION类型累计占比:")
print(action_stats[['ACTION类型', '数量', '占比(%)', '累计占比(%)']].to_string(index=False))

# 可视化输出
print("\n" + "="*50)
print("ACTION占比分布:")
print("="*50)
for _, row in action_stats.iterrows():
    bar_length = int(row['占比(%)'] / 2)  # 每2%一个字符
    bar = '█' * bar_length
    print(f"{row['ACTION类型']:20s} {row['数量']:3d} ({row['占比(%)']:5.1f}%) {bar}")

# 保存统计结果
output_file = "action_statistics.csv"
action_stats.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n统计结果已保存到: {output_file}")

# 显示前10个ACTION类型的详细信息
print("\n" + "="*50)
print("ACTION类型示例记录:")
print("="*50)
for action_type in action_counts.index[:10]:  # 显示前10个类型
    print(f"\nACTION: {action_type}")
    sample_records = df[df['ACTION'] == action_type].head(2)
    for _, row in sample_records.iterrows():
        print(f"  - LOGINID: {row['LOGINID']}, IP: {row['IP']}, URI: {row['URI']}, LOGTYPE: {row['LOGTYPE']}")