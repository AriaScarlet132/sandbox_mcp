import pandas as pd
import json
from datetime import datetime

# 读取数据
df = pd.read_parquet('df_sysaccesslogtestds_20260115T100453Z_b2d9ed105d9844c385e88baf84887285.parquet')

print(f"数据总行数: {len(df)}")
print(f"数据字段: {df.columns.tolist()}")
print("\n" + "="*80 + "\n")

# 1. 按ACTION统计访问量
action_stats = df['ACTION'].value_counts().reset_index()
action_stats.columns = ['ACTION', '访问次数']
action_stats['占比(%)'] = (action_stats['访问次数'] / len(df) * 100).round(2)
action_stats['累计占比(%)'] = action_stats['占比(%)'].cumsum()

print("=== 按ACTION统计访问量 ===")
for i, row in action_stats.iterrows():
    print(f"{row['ACTION']}: {row['访问次数']}次 ({row['占比(%)']}%)")
print("\n" + "="*80 + "\n")

# 2. 按LOGTYPE统计访问量
logtype_stats = df['LOGTYPE'].value_counts().reset_index()
logtype_stats.columns = ['LOGTYPE', '访问次数']
logtype_stats['占比(%)'] = (logtype_stats['访问次数'] / len(df) * 100).round(2)

print("=== 按LOGTYPE统计访问量 ===")
for i, row in logtype_stats.iterrows():
    print(f"{row['LOGTYPE']}: {row['访问次数']}次 ({row['占比(%)']}%)")
print("\n" + "="*80 + "\n")

# 3. 按LOGTYPE和ACTION组合统计
grouped_stats = df.groupby(['LOGTYPE', 'ACTION']).size().reset_index(name='访问次数')
grouped_stats['占比(%)'] = (grouped_stats['访问次数'] / len(df) * 100).round(2)
grouped_stats = grouped_stats.sort_values('访问次数', ascending=False)

print("=== 按LOGTYPE和ACTION组合统计 ===")
for i, row in grouped_stats.iterrows():
    print(f"{row['LOGTYPE']}-{row['ACTION']}: {row['访问次数']}次 ({row['占比(%)']}%)")
print("\n" + "="*80 + "\n")

# 4. 按IP地址统计
ip_stats = df['IP'].value_counts().reset_index()
ip_stats.columns = ['IP', '访问次数']
ip_stats['占比(%)'] = (ip_stats['访问次数'] / len(df) * 100).round(2)

print("=== 按IP地址统计 ===")
for i, row in ip_stats.iterrows():
    print(f"{row['IP']}: {row['访问次数']}次 ({row['占比(%)']}%)")
print("\n" + "="*80 + "\n")

# 5. 按用户统计
user_stats = df['LOGINID'].value_counts().reset_index()
user_stats.columns = ['LOGINID', '访问次数']
user_stats['占比(%)'] = (user_stats['访问次数'] / len(df) * 100).round(2)

print("=== 按用户统计 ===")
for i, row in user_stats.iterrows():
    print(f"{row['LOGINID']}: {row['访问次数']}次 ({row['占比(%)']}%)")
print("\n" + "="*80 + "\n")

# 6. 时间分布分析
# 将RECORDDATE转换为datetime格式
df['RECORDDATE'] = pd.to_datetime(df['RECORDDATE'])
df['日期'] = df['RECORDDATE'].dt.date
df['小时'] = df['RECORDDATE'].dt.hour

# 按日期统计
date_stats = df['日期'].value_counts().sort_index().reset_index()
date_stats.columns = ['日期', '访问次数']

print("=== 按日期统计 ===")
for i, row in date_stats.iterrows():
    print(f"{row['日期']}: {row['访问次数']}次")
print("\n" + "="*80 + "\n")

# 按小时统计
hour_stats = df['小时'].value_counts().sort_index().reset_index()
hour_stats.columns = ['小时', '访问次数']
hour_stats['占比(%)'] = (hour_stats['访问次数'] / len(df) * 100).round(2)

print("=== 按小时统计 ===")
for i, row in hour_stats.iterrows():
    print(f"{row['小时']}:00-{row['小时']+1}:00: {row['访问次数']}次 ({row['占比(%)']}%)")
print("\n" + "="*80 + "\n")

# 7. 生成详细报告
print("=== 系统访问量详细分析报告 ===")
print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"总访问量: {len(df)} 次")
print(f"唯一ACTION数量: {df['ACTION'].nunique()} 种")
print(f"唯一LOGTYPE数量: {df['LOGTYPE'].nunique()} 种")
print(f"唯一用户数量: {df['LOGINID'].nunique()} 个")
print(f"唯一IP地址数量: {df['IP'].nunique()} 个")
print(f"数据时间范围: {df['RECORDDATE'].min()} 至 {df['RECORDDATE'].max()}")
print(f"数据天数: {df['日期'].nunique()} 天")

# 8. 保存统计结果到文件
stats_summary = {
    '总访问量': len(df),
    '唯一ACTION数量': int(df['ACTION'].nunique()),
    '唯一LOGTYPE数量': int(df['LOGTYPE'].nunique()),
    '唯一用户数量': int(df['LOGINID'].nunique()),
    '唯一IP地址数量': int(df['IP'].nunique()),
    '数据时间范围': f"{df['RECORDDATE'].min()} 至 {df['RECORDDATE'].max()}",
    '数据天数': int(df['日期'].nunique()),
    'ACTION统计': action_stats.to_dict('records'),
    'LOGTYPE统计': logtype_stats.to_dict('records'),
    '组合统计': grouped_stats.to_dict('records'),
    'IP统计': ip_stats.to_dict('records'),
    '用户统计': user_stats.to_dict('records'),
    '日期统计': date_stats.to_dict('records'),
    '小时统计': hour_stats.to_dict('records')
}

with open('access_stats_summary.json', 'w', encoding='utf-8') as f:
    json.dump(stats_summary, f, ensure_ascii=False, indent=2, default=str)

print(f"\n详细统计结果已保存到: access_stats_summary.json")

# 9. 关键指标
print("\n=== 关键指标 ===")
# 前3个ACTION占比
top3_actions = action_stats.head(3)
print("前3个ACTION:")
for i, row in top3_actions.iterrows():
    print(f"  {i+1}. {row['ACTION']}: {row['访问次数']}次 ({row['占比(%)']}%)")

# 最活跃的时间段
top_hour = hour_stats.loc[hour_stats['访问次数'].idxmax()]
print(f"\n最活跃的时间段: {top_hour['小时']}:00-{top_hour['小时']+1}:00, {top_hour['访问次数']}次 ({top_hour['占比(%)']}%)")

# 最活跃的用户
top_user = user_stats.head(1).iloc[0]
print(f"最活跃的用户: {top_user['LOGINID']}, {top_user['访问次数']}次 ({top_user['占比(%)']}%)")

# 帕累托分析
print("\n=== 帕累托分析 ===")
cumulative_count = 0
for i, row in action_stats.iterrows():
    cumulative_count += row['访问次数']
    cumulative_percent = (cumulative_count / len(df) * 100).round(2)
    print(f"{row['ACTION']}: {row['访问次数']}次 ({row['占比(%)']}%), 累计: {cumulative_percent}%")
    if cumulative_percent >= 80:
        print(f"达到80%累计占比的ACTION数量: {i+1}个")
        break