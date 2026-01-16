import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

print("=== Python脚本验证能力 ===")
print("1. 基本数学运算:")
print(f"   2 + 3 = {2 + 3}")
print(f"   10 * 5 = {10 * 5}")
print(f"   100 / 4 = {100 / 4}")

print("\n2. 字符串操作:")
text = "Hello, World!"
print(f"   原始字符串: {text}")
print(f"   大写: {text.upper()}")
print(f"   小写: {text.lower()}")
print(f"   反转: {text[::-1]}")

print("\n3. 列表和字典操作:")
numbers = [1, 2, 3, 4, 5]
print(f"   列表: {numbers}")
print(f"   列表平方: {[x**2 for x in numbers]}")

person = {"name": "Alice", "age": 25, "city": "Beijing"}
print(f"   字典: {person}")
print(f"   姓名: {person['name']}")

print("\n4. 数据分析和统计:")
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, 35, 40, 45],
    'salary': [50000, 60000, 70000, 80000, 90000]
}
df = pd.DataFrame(data)
print("   数据框:")
print(df)

print(f"\n   平均年龄: {df['age'].mean():.2f}")
print(f"   平均薪资: {df['salary'].mean():.2f}")
print(f"   年龄标准差: {df['age'].std():.2f}")

print("\n5. 文件操作:")
with open('test_file.txt', 'w') as f:
    f.write("这是一个测试文件\n")
    f.write("第二行内容\n")
    f.write("第三行内容\n")

with open('test_file.txt', 'r') as f:
    content = f.read()
    print("   文件内容:")
    print(content)

print("\n6. 当前时间:")
current_time = datetime.now()
print(f"   当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

print("\n=== 脚本执行完成 ===")