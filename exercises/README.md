# 第 1 周练习

4 个练习，对应 `WEEK1.md` 的七天安排。**每个练习文件里都写了要求、提示和示例**，先自己写。

## 顺序（不要打乱）

| 练习 | 文件 | 练什么 | 建议在哪天完成 |
|---|---|---|---|
| 1 | `ex1_files.py` | 循环、`pathlib`、异常 | Day 1-2 |
| 2 | `ex2_api_json.py` | HTTP、重试、JSON 读写 | Day 3-4 |
| 3 | `ex3_cli.py` | `argparse`、纯函数与 IO 分离 | Day 6 |
| 4 | `ex4_pydantic.py` | 类型注解、pydantic 校验 | Day 5（最重要） |

## 怎么跑

```powershell
cd C:\Users\kk\Desktop\dsh\agent-portfolio

uv run pytest exercises -v            # 全部（一开始全红是正常的）
uv run pytest exercises -v -k ex1     # 只跑练习 1
uv run pytest exercises -v -x         # 第一个失败就停

uv run python exercises/ex2_api_json.py   # 练习 2 写完后真实跑一次
```

## 规则

1. **不要改 `test_exercises.py`**。它是验收标准；如果你觉得测试写错了，来问我。
2. **看报错的下半部分**。Python 的报错要从最后一行往回读：最后一行是"什么错"，往上是"在哪一行"。
3. **卡住 30 分钟就停**，把这三样发给我：完整报错（最后 15 行）+ 你写的函数 + 你的猜测。
4. **每通过一个练习就提交一次**：
   ```powershell
   git add .
   git commit -m "第1周: 完成练习1 文件处理"
   git push
   ```
   面试官看的就是这种"一步一步"的提交历史，别攒到最后一次性推。

## 通过标准

```
14 passed
```

4 个练习一共 14 项检查（ex1 五项、ex2/ex3/ex4 各三项）。全绿 = 第 1 周核心目标达成。
