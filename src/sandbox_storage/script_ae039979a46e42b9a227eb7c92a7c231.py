import pandas as pd

# 读取数据
df = pd.read_parquet('df_sysaccesslogtestds_20260115T100453Z_b2d9ed105d9844c385e88baf84887285.parquet')

print("数据总行数:", len(df))
print("数据字段:", list(df.columns))
print("\n" + "="*80 + "\n")

# 1. 按ACTION统计访问量
action_counts = df['ACTION'].value_counts()
print("=== 按ACTION统计访问量 ===")
for action, count in action_counts.items():
    percent = (count / len(df) * 100)
    print(f"{action}: {count}次 ({percent:.2f}%)")
print("\n" + "="*80 + "\n")

# 2. 按LOGTYPE统计访问量
logtype_counts = df['LOGTYPE'].value_counts()
print("=== 按LOGTYPE统计访问量 ===")
for logtype, count in logtype_counts.items():
    percent = (count / len(df) * 100)
    print(f"{logtype}: {count}次 ({percent:.2f}%)")
print("\n" + "="*80 + "\n")

# 3. 按LOGTYPE和ACTION组合统计
grouped = df.groupby(['LOGTYPE', 'ACTION']).size()
print("=== 按LOGTYPE和ACTION组合统计 ===")
for (logtype, action), count in grouped.items():
    percent = (count / len(df) * 100)
    print(f"{logtype}-{action}: {count}次 ({percent:.2f}%)")
print("\n" + "="*80 + "\n")

# 4. 按IP地址统计
ip_counts = df['IP'].value_counts()
print("=== 按IP地址统计 ===")
for ip, count in ip_counts.items():
    percent = (count / len(df) * 100)
    print(f"{ip}: {count}次 ({percent:.2f}%)")
print("\n" + "="*80 + "\n")

# 5. 按用户统计
user_counts = df['LOGINID'].value_counts()
print("=== 按用户统计 ===")
for user, count in user_counts.items():
    percent = (count / len(df) * 100)
    print(f"{user}: {count}次 ({percent:.2f}%)")
print("\n" + "="*80 + "\n")

# 6. 时间分布分析
df['RECORDDATE'] = pd.to_datetime(df['RECORDDATE'])
df['日期'] = df['RECORDDATE'].dt.date
df['小时'] = df['RECORDDATE'].dt.hour

# 按日期统计
date_counts = df['日期'].value_counts().sort_index()
print("=== 按日期统计 ===")
for date, count in date_counts.items():
    print(f"{date}: {count}次")
print("\n" + "="*80 + "\n")

# 按小时统计
hour_counts = df['小时'].value_counts().sort_index()
print("=== 按小时统计 ===")
for hour, count in hour_counts.items():
    percent = (count / len(df) * 100)
    print(f"{hour}:00-{hour+1}:00: {count}次 ({percent:.2f}%)")
print("\n" + "="*80 + "\n")

# 7. 生成详细报告
print("=== 系统访问量详细分析报告 ===")
print(f"总访问量: {len(df)} 次")
print(f"唯一ACTION数量: {df['ACTION'].nunique()} 种")
print(f"唯一LOGTYPE数量: {df['LOGTYPE'].nunique()} 种")
print(f"唯一用户数量: {df['LOGINID'].nunique()} 个")
print(f"唯一IP地址数量: {df['IP'].nunique()} 个")
print(f"数据时间范围: {df['RECORDDATE'].min()} 至 {df['RECORDDATE'].max()}")
print(f"数据天数: {df['日期'].nunique()} 天")

# 8. 关键指标
print("\n=== 关键指标 ===")
# 前3个ACTION占比
top3_actions = action_counts.head(3)
print("前3个ACTION:")
for i, (action, count) in enumerate(top3_actions.items(), 1):
    percent = (count / len(df) * 100)
    print(f"  {i}. {action}: {count}次 ({percent:.2f}%)")

# 最活跃的时间段
top_hour = hour_counts.idxmax()
top_hour_count = hour_counts.max()
top_hour_percent = (top_hour_count / len(df) * 100)
print(f"\n最活跃的时间段: {top_hour}:00-{top_hour+1}:00, {top_hour_count}次 ({top_hour_percent:.2f}%)")

# 最活跃的用户
top_user = user_counts.idxmax()
top_user_count = user_counts.max()
top_user_percent = (top_user_count / len(df) * 100)
print(f"最活跃的用户: {top_user}, {top_user_count}次 ({top_user_percent:.2f}%)")

# 帕累托分析
print("\n=== 帕累托分析 ===")
cumulative_count = 0
cumulative_percent = 0
for i, (action, count) in enumerate(action_counts.items(), 1):
    cumulative_count += count
    cumulative_percent = (cumulative_count / len(df) * 100)
    percent = (count / len(df) * 100)
    print(f"{action}: {count}次 ({percent:.2f}%), 累计: {cumulative_percent:.2f}%")
    if cumulative_percent >= 80:
        print(f"达到80%累计占比的ACTION数量: {i}个")
        break