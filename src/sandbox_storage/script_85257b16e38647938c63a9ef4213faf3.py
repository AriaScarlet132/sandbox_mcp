# 简单的Python脚本验证
print("=== Python脚本验证能力 ===")

# 1. 基本运算
print("1. 基本数学运算:")
result1 = 10 + 20
result2 = 50 * 3
result3 = 100 / 4
print(f"   10 + 20 = {result1}")
print(f"   50 * 3 = {result2}")
print(f"   100 / 4 = {result3}")

# 2. 字符串操作
print("\n2. 字符串操作:")
text = "Hello, Python!"
print(f"   原始字符串: {text}")
print(f"   长度: {len(text)}")
print(f"   大写: {text.upper()}")
print(f"   小写: {text.lower()}")

# 3. 列表操作
print("\n3. 列表操作:")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"   数字列表: {numbers}")
print(f"   列表长度: {len(numbers)}")
print(f"   前3个元素: {numbers[:3]}")
print(f"   后3个元素: {numbers[-3:]}")
print(f"   偶数: {[x for x in numbers if x % 2 == 0]}")
print(f"   奇数: {[x for x in numbers if x % 2 == 1]}")

# 4. 字典操作
print("\n4. 字典操作:")
student = {
    "name": "张三",
    "age": 20,
    "major": "计算机科学",
    "grades": {"数学": 95, "英语": 88, "编程": 92}
}
print(f"   学生信息: {student}")
print(f"   姓名: {student['name']}")
print(f"   年龄: {student['age']}")
print(f"   平均成绩: {sum(student['grades'].values()) / len(student['grades']):.1f}")

# 5. 函数定义
print("\n5. 函数定义:")
def calculate_stats(nums):
    """计算统计信息"""
    return {
        "总和": sum(nums),
        "平均值": sum(nums) / len(nums),
        "最大值": max(nums),
        "最小值": min(nums)
    }

stats = calculate_stats(numbers)
print(f"   统计信息: {stats}")

# 6. 使用pandas进行数据分析
print("\n6. 使用pandas进行数据分析:")
import pandas as pd
import numpy as np

# 创建示例数据
data = {
    '产品': ['A', 'B', 'C', 'D', 'E'],
    '销量': [120, 150, 80, 200, 90],
    '价格': [50, 75, 30, 100, 40],
    '类别': ['电子', '服装', '食品', '电子', '服装']
}
df = pd.DataFrame(data)
print("   数据框:")
print(df)

# 计算总销售额
df['销售额'] = df['销量'] * df['价格']
print(f"\n   总销售额: {df['销售额'].sum()}")
print(f"   平均销量: {df['销量'].mean():.1f}")
print(f"   平均价格: {df['价格'].mean():.1f}")

# 按类别分组
grouped = df.groupby('类别')['销售额'].sum()
print(f"\n   按类别销售额:")
print(grouped)

print("\n=== 脚本执行完成 ===")