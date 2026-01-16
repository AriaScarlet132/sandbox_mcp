# 这是一个简单的Python脚本，用于验证我的能力
print("=== 简单的Python脚本验证 ===")
print("1. 打印欢迎信息")
print("Hello! 我是一个数据分析师助手")

print("\n2. 进行简单的数学计算")
a = 10
b = 5
print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b}")

print("\n3. 使用列表和循环")
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
print("我喜欢的水果:")
for i, fruit in enumerate(fruits, 1):
    print(f"  {i}. {fruit}")

print("\n4. 使用字典")
person = {"姓名": "张三", "年龄": 25, "职业": "数据分析师"}
print("个人信息:")
for key, value in person.items():
    print(f"  {key}: {value}")

print("\n5. 导入并使用pandas（验证数据分析能力）")
import pandas as pd
import numpy as np

# 创建一个简单的DataFrame
data = {
    "日期": pd.date_range("2024-01-01", periods=5),
    "销售额": [1000, 1500, 1200, 1800, 2000],
    "客户数": [50, 75, 60, 90, 100]
}
df = pd.DataFrame(data)
print("示例数据:")
print(df)

print(f"\n数据统计:")
print(f"总销售额: {df['销售额'].sum()}")
print(f"平均销售额: {df['销售额'].mean():.2f}")
print(f"最大销售额: {df['销售额'].max()}")
print(f"最小销售额: {df['销售额'].min()}")

print("\n=== 脚本执行完成 ===")