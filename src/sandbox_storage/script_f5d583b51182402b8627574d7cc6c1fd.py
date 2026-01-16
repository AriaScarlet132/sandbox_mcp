print("=== 简单Python脚本验证 ===")
print("Python环境测试开始...")

# 测试基本Python功能
print("1. 基本运算测试:")
a = 10
b = 20
print(f"   {a} + {b} = {a + b}")
print(f"   {a} * {b} = {a * b}")

print("\n2. 列表操作测试:")
numbers = [1, 2, 3, 4, 5]
print(f"   原始列表: {numbers}")
print(f"   列表求和: {sum(numbers)}")
print(f"   列表长度: {len(numbers)}")

print("\n3. 字符串操作测试:")
text = "Hello, Data Analyst!"
print(f"   原始字符串: {text}")
print(f"   大写: {text.upper()}")
print(f"   小写: {text.lower()}")

print("\n4. 字典操作测试:")
data = {"name": "Test", "value": 100, "active": True}
print(f"   字典内容: {data}")
print(f"   键列表: {list(data.keys())}")

print("\n5. 循环测试:")
print("   数字1-5的平方:")
for i in range(1, 6):
    print(f"   {i}² = {i**2}")

print("\n=== 测试完成 ===")
print("Python环境运行正常！")