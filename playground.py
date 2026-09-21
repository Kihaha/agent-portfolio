"""第 1 周 playground：边看边敲的地方

用法（在 agent-portfolio 目录下）：
    uv run python playground.py

规矩（很重要）：
  1. 每看一段，**先在注释里写下你猜的输出**，再运行对照
  2. 猜错了是好事 —— 那正是你要学的地方，把正确答案记下来
  3. 想试别的写法就在这个文件里改，改坏了没关系，它本来就是拿来试错的
  4. 这里写得好不好看不重要，**动手了才算数**

（这个文件不在验收范围内，随便改）
"""

# ============================================================
# 1. 变量与基础类型
# ============================================================
print("=== 1. 变量与基础类型 ===")

name = "kk"           # str   字符串
age = 24              # int   整数
height = 1.75         # float 小数
is_student = True     # bool  布尔
nothing = None        # NoneType 空值（表示"没有值"）

# 猜猜这行会输出什么？
print(name, age, height, is_student, nothing)

# type() 用来问"这是什么类型"，是排错时最常用的函数之一
print(type(name), type(age), type(height), type(is_student), type(nothing))

# 小实验：变量可以改类型吗？（Python 是动态类型）
age = "二十四"
print("改过之后 age 的类型:", type(age))


# ============================================================
# 2. f-string（最常用的字符串拼接方式）
# ============================================================
print("\n=== 2. f-string ===")

user = "小明"
count = 3
price = 12.5

print(f"你好 {user}，你有 {count} 件商品")          # 直接插变量
print(f"总共 {count * price} 元")                    # 里面可以写表达式
print(f"总共 {count * price:.2f} 元")                # .2f = 保留 2 位小数
print(f"{user} 的余额是 {1000:,} 元")                # , = 千分位分隔
print(f"调试常用写法: {count=} {price=}")            # = 会连变量名一起打印

# 猜：如果忘了写 f 前缀，会输出什么？
print("没有 f 前缀: {user}")


# ============================================================
# 3. 数字运算（这里有坑）
# ============================================================
print("\n=== 3. 数字运算 ===")

print(7 + 3, 7 - 3, 7 * 3)
print("除法 / 结果永远是小数:", 6 / 3, 7 / 2)
print("整除 // 向下取整  :", 7 // 2, -7 // 2)
print("取余 %            :", 7 % 2, 10 % 3)
print("幂 **             :", 2 ** 10)
print("浮点数精度问题     :", 0.1 + 0.2)          # 经典坑，猜猜结果

print("字符串重复         :", "ab" * 3)
print("数字转字符串拼接   :", "第" + str(1) + "名")


# ============================================================
# 4. 字符串常用操作
# ============================================================
print("\n=== 4. 字符串操作 ===")

s = "  Hello, Python  "
print("原始      :", repr(s))          # repr 能看见空格
print("去空白    :", repr(s.strip()))
print("转小写    :", s.strip().lower())
print("替换      :", s.replace("Python", "Agent"))
print("切分      :", "a,b,c".split(","))
print("长度      :", len(s))

text = "0123456789"
print("切片 [2:5] :", text[2:5])       # 含头不含尾
print("切片 [:3]  :", text[:3])
print("切片 [-3:] :", text[-3:])
print("反转       :", text[::-1])


# ============================================================
# 5. 布尔与条件判断
# ============================================================
print("\n=== 5. 条件判断 ===")

score = 78

if score >= 90:
    print("优秀")
elif score >= 75:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# 猜：下面这句会打印什么？（空字符串、0、空列表都算"假"）
for value in ["", "abc", 0, 1, [], [0], None]:
    print(f"  bool({value!r}) = {bool(value)}")

# and / or 的"短路"：左边能决定结果时，右边不执行
print("\n短路测试:", True or print("这句不会执行"), False and print("这句也不会"))


# ============================================================
# 6. 循环
# ============================================================
print("\n=== 6. 循环 ===")

print("for + range:", end=" ")
for i in range(3):
    print(i, end=" ")
print()

print("range(2, 5)  :", list(range(2, 5)))
print("range(0, 10, 3):", list(range(0, 10, 3)))

# enumerate：同时拿到下标和值（比 range(len(x)) 好得多）
fruits = ["苹果", "香蕉", "橘子"]
for index, fruit in enumerate(fruits):
    print(f"  {index}: {fruit}")

# zip：同时遍历两个列表
prices = [5, 3, 8]
for fruit, price in zip(fruits, prices):
    print(f"  {fruit} 卖 {price} 元")

# while + break / continue
print("\nwhile 找第一个能被 7 整除的数:", end=" ")
n = 1
while True:
    if n % 7 == 0:
        print(n)
        break
    n += 1

print("跳过偶数:", end=" ")
for i in range(6):
    if i % 2 == 0:
        continue
    print(i, end=" ")
print()


# ============================================================
# 7. 容器入门（Day 2 会系统学，这里先感受）
# ============================================================
print("\n=== 7. 列表与字典 ===")

nums = [3, 1, 4, 1, 5]
print("列表          :", nums)
print("长度 / 最大值 :", len(nums), max(nums))
print("追加          :", nums + [9, 2, 6])
print("排序（新列表）:", sorted(nums))
print("原列表没变    :", nums)

user_info = {"name": "kk", "city": "北京", "age": 24}
print("字典          :", user_info)
print("取一个字段    :", user_info["name"])
print("安全取值      :", user_info.get("email", "没有这个字段"))
print("所有键        :", list(user_info.keys()))
for key, value in user_info.items():
    print(f"  {key} -> {value}")


# ============================================================
# 8. 故意报错：学会读 traceback
# ============================================================
print("\n=== 8. 读报错（这段一定会报错，是故意的）===")

try:
    result = "10" + 5           # 字符串 + 数字 → TypeError
except TypeError as exc:
    print("捕获到错误类型:", type(exc).__name__)
    print("错误信息      :", exc)

print("\n读 traceback 的方法：从**最后一行**往回读。")
print("最后一行是'什么错'，往上一行是'在哪一行'。")
