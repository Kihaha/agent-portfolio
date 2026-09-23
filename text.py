with open("chinese.txt", "w") as f:
    f.write("你好\n")
    f.write("鼠标")
with open("chinese.txt") as a:
    for i, line in enumerate(a, start=1):
        print(f"{i}.{line.strip()}")
