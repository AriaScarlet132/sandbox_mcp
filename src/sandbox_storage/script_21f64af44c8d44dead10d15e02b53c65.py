print("=== Python脚本验证 ===")
print("1. 基本运算:")
a = 10
b = 20
print(f"a = {a}, b = {b}")
print(f"a + b = {a + b}")
print(f"a * b = {a * b}")
print(f"b / a = {b / a}")

print("\n2. 字符串操作:")
text = "Hello World"
print(f"原始: {text}")
print(f"大写: {text.upper()}")
print(f"小写: {text.lower()}")
print(f"长度: {len(text)}")

print("\n3. 列表操作:")
numbers = [1, 2, 3, 4, 5]
print(f"列表: {numbers}")
print(f"总和: {sum(numbers)}")
print(f"平均值: {sum(numbers)/len(numbers)}")

print("\n4. 循环:")
print("1-5的平方:")
for i in range(1, 6):
    print(f"  {i}^2 = {i**2}")

print("\n5. 条件判断:")
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "D"
print(f"分数: {score}, 等级: {grade}")

print("\n6. 字典:")
person = {"name": "张三", "age": 25, "city": "北京"}
print(f"个人信息: {person}")
print(f"姓名: {person['name']}")

print("\n=== 验证完成 ===")