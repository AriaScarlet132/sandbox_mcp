import matplotlib.pyplot as plt
import numpy as np

# 数据准备
logtypes = ['系统', '系统', '系统', 'View', 'BizLogicStudio', 'View', '系统', '系统']
actions = ['系统启动成功', '自动登录', '用户登录', 'updateData', '登录', 'saveData', '保存集成接口设置', '保存配置']
access_counts = [28, 21, 14, 9, 5, 5, 2, 2]
percentages = [32.56, 24.42, 16.28, 10.47, 5.81, 5.81, 2.33, 2.33]

# 创建图表
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 柱状图
labels = [f"{logtype}-{action}" for logtype, action in zip(logtypes, actions)]
bars = ax1.bar(labels, access_counts, color='skyblue')
ax1.set_title('系统访问量统计（按操作类型）', fontsize=14, fontweight='bold')
ax1.set_xlabel('操作类型', fontsize=12)
ax1.set_ylabel('访问次数', fontsize=12)
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis='y', alpha=0.3)

# 在柱子上添加数值
for bar, count in zip(bars, access_counts):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{count}', ha='center', va='bottom', fontsize=10)

# 饼图
colors = plt.cm.Set3(np.linspace(0, 1, len(access_counts)))
wedges, texts, autotexts = ax2.pie(access_counts, labels=labels, autopct='%1.1f%%',
                                   colors=colors, startangle=90)
ax2.set_title('系统访问量分布比例', fontsize=14, fontweight='bold')

# 调整饼图标签位置
for text in texts:
    text.set_fontsize(9)

plt.tight_layout()
plt.show()

# 打印统计摘要
print("=== 系统访问量统计摘要 ===")
print(f"总访问量: 86 次")
print("\n按操作类型统计:")
for i in range(len(labels)):
    print(f"{labels[i]}: {access_counts[i]} 次 ({percentages[i]}%)")

print("\n=== 主要发现 ===")
print("1. 系统启动成功是最频繁的操作，占32.56%")
print("2. 登录相关操作（自动登录+用户登录）合计占40.70%")
print("3. 数据操作（updateData+saveData）合计占16.28%")
print("4. 配置保存操作占4.66%")