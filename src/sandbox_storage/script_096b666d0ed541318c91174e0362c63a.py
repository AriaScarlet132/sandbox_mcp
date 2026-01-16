# 系统访问量统计摘要
print("=== 系统访问量统计摘要 ===")
print(f"总访问量: 86 次")

# 数据准备
logtypes = ['系统', '系统', '系统', 'View', 'BizLogicStudio', 'View', '系统', '系统']
actions = ['系统启动成功', '自动登录', '用户登录', 'updateData', '登录', 'saveData', '保存集成接口设置', '保存配置']
access_counts = [28, 21, 14, 9, 5, 5, 2, 2]
percentages = [32.56, 24.42, 16.28, 10.47, 5.81, 5.81, 2.33, 2.33]

print("\n=== 按操作类型详细统计 ===")
for i in range(len(actions)):
    print(f"{logtypes[i]}-{actions[i]}: {access_counts[i]} 次 ({percentages[i]}%)")

print("\n=== 分类汇总 ===")
# 计算各类别的汇总
system_total = sum(access_counts[i] for i in range(len(logtypes)) if logtypes[i] == '系统')
view_total = sum(access_counts[i] for i in range(len(logtypes)) if logtypes[i] == 'View')
biz_total = sum(access_counts[i] for i in range(len(logtypes)) if logtypes[i] == 'BizLogicStudio')

system_percent = round(system_total * 100 / 86, 2)
view_percent = round(view_total * 100 / 86, 2)
biz_percent = round(biz_total * 100 / 86, 2)

print(f"系统操作: {system_total} 次 ({system_percent}%)")
print(f"视图操作: {view_total} 次 ({view_percent}%)")
print(f"业务逻辑操作: {biz_total} 次 ({biz_percent}%)")

print("\n=== 主要发现 ===")
print("1. 系统启动成功是最频繁的操作，占32.56%")
print("2. 登录相关操作（自动登录+用户登录）合计占40.70%")
print("3. 数据操作（updateData+saveData）合计占16.28%")
print("4. 配置保存操作占4.66%")
print("5. 系统操作占总访问量的78.49%，是主要访问类型")
print("6. 视图操作占总访问量的16.28%，主要是数据更新和保存操作")
print("7. 业务逻辑操作占总访问量的5.81%，主要是登录操作")

print("\n=== 建议 ===")
print("1. 系统启动和登录操作占比较高，建议优化启动和登录性能")
print("2. 数据操作频率适中，建议关注数据操作的安全性和稳定性")
print("3. 配置操作相对较少，但很重要，建议加强配置管理的监控")