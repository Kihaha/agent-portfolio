# 第 1 周：Python 速成冲刺（35 小时）

> 对应计划 `两个月学习计划.md` 的 **P1 · 第 1 周**。
> 目标不是"学会 Python"，而是**能写出工程代码**——本周结束时你要能独立写一个带异常处理和重试的 API 调用脚本。

## 本周验收标准（唯一一条，别扩大）

- [ ] `uv run pytest exercises -v` **全部通过（4 个练习、14 项检查）**
- [ ] 能对着 `test_api.py` 逐行讲清楚：它在做什么、为什么这么写
- [ ] 4 个练习提交到 GitHub（第 2 个 commit）

## 本周**不要**做的事（很重要）

- ❌ 不学算法题、不刷 LeetCode
- ❌ 不学机器学习理论、不看 Transformer
- ❌ 不追求 Python 高级特性（元类、装饰器进阶、异步原理都留到后面）
- ❌ 不要"看完教程再动手"——**每学 30 分钟必须写代码**

---

## 七天安排（每天约 5 小时）

每天固定动作：
1. **30 分钟**：复习昨天 + 看一眼昨天的卡点笔记
2. **2 小时**：学新知识（边看边敲，禁止只看不写）
3. **2 小时**：写练习代码，**当天必须有能运行的产出**
4. **30 分钟**：写学习日志（今天做了什么 / 卡在哪 / 明天第一件事）

### Day 1 — Python 基础（一）+ 练习 1 起步
| 时段 | 内容 |
|---|---|
| 0.5h | 环境自检：`uv run python -c "import sys; print(sys.executable)"` 确认在 `.venv` 里；VS Code 打开项目、确认右下角解释器 |
| 2h | 变量与类型、字符串与 f-string、数字、布尔、None、`input`/`print` |
| 1.5h | 条件（if/elif/else）、循环（for/while/range/enumerate/zip）、`break`/`continue` |
| 1h | 练习 1 的 `list_files` + `total_size` |
| 产出 | ex1 的一半函数通过测试 |

### Day 2 — Python 基础（二）+ 练习 1 完成
| 时段 | 内容 |
|---|---|
| 1.5h | 列表 / 字典 / 集合 / 元组；增删改查、切片、常用方法 |
| 1.5h | 函数：默认参数、关键字参数、`*args`/`**kwargs`、返回值、作用域；`from __future__ import annotations` |
| 1h | 异常：`try`/`except`/`else`/`finally`、`raise`、自定义异常类 |
| 1h | 完成 ex1 的 `group_by_suffix` + `main` |
| 产出 | **ex1 全部通过** |

### Day 3 — 文件、JSON 与模块
| 时段 | 内容 |
|---|---|
| 1.5h | `pathlib.Path`、`open`/`with`、读写文本、编码（为什么永远写 `encoding="utf-8"`） |
| 1.5h | JSON：`json.load`/`dump`/`loads`/`dumps`、`ensure_ascii=False`、`indent=2` |
| 1h | 模块与包、`if __name__ == "__main__"` 的意义、虚拟环境到底隔离了什么 |
| 1h | 练习 2 的 `save_json` + `load_json` |
| 产出 | ex2 的 JSON 部分通过 |

### Day 4 — HTTP 与重试（第一次碰真实世界）
| 时段 | 内容 |
|---|---|
| 1.5h | HTTP 基础：方法、状态码（200/401/429/500 分别什么意思）、请求头、`httpx` 用法 |
| 1.5h | 超时、异常层次、**重试与退避**、为什么要自定义异常 |
| 2h | 完成 ex2 的 `fetch_json` + `main` |
| 产出 | **ex2 全部通过**，并能真实跑通 `uv run python exercises/ex2_api_json.py` |

### Day 5 — 类型注解 + pydantic（本周最重要）
| 时段 | 内容 |
|---|---|
| 1.5h | 类型注解语法：`str \| None`、`list[dict[str, Any]]`、`Literal`、`Any`；注解不检查、但工具会检查 |
| 2h | pydantic：`BaseModel`、`Field`、`model_validate`、`ValidationError`；为什么"数据进来先校验" |
| 1.5h | 完成 ex4 |
| 产出 | **ex4 全部通过**。这一天学的东西第 2 周开始天天用 |

### Day 6 — 命令行工具 + 代码组织
| 时段 | 内容 |
|---|---|
| 1.5h | `argparse`：位置参数、`--可选参数`、默认值、`--help`、返回退出码 |
| 1.5h | 代码组织：把"纯计算"和"输入输出"分开（纯函数好测试） |
| 2h | 完成 ex3 |
| 产出 | **ex3 全部通过**，并能在终端真的用起来 |

### Day 7 — 收口：日志、配置、提交
| 时段 | 内容 |
|---|---|
| 1h | `logging` 基础：为什么生产代码不用 `print`；日志级别 |
| 1h | 环境变量与 `.env`：`load_dotenv()`、为什么密钥绝不写进代码 |
| 2h | 整理代码 → `git add` → `git commit` → `git push`，并在 README 里补一段练习说明 |
| 1h | 自测：写下"我现在能解释清楚的 10 个 Python 概念"，讲不出来的补一下 |
| 产出 | **GitHub 上出现第 2 个提交** |

---

## 怎么用这套练习

```powershell
cd C:\Users\kk\Desktop\dsh\agent-portfolio

# 看当前进度（一开始会全红，这是正常的，红=还没实现）
uv run pytest exercises -v

# 只跑某一个练习
uv run pytest exercises -v -k ex1

# 练习 2 写完后，真实跑一次
uv run python exercises/ex2_api_json.py
```

每个练习文件里都写了 **要求 + 提示 + 示例**，就在函数的 docstring 里。**不要看答案，先自己写**；卡住 30 分钟再来问。

## 卡住的时候怎么问（省时间的关键）

问我的时候带上这三样，比"我卡住了"有效 10 倍：

1. **完整报错信息**（最后 15 行就够）
2. **你写的代码**（贴函数，不用贴整个文件）
3. **你的猜测**（"我觉得是 xxx 的问题"）

## 参考资源

按 `agent-intern\02-学习资源清单.md` 的**模块 1（Python 工程化）**走：

- Python 官方中文教程（虚拟环境那章）
- uv 官方文档
- pydantic 官方文档（Day 5 用）
- FastAPI 中文文档（Day 4 之后当手册翻，第 2 周正式学）

## 周末自测（不看笔记回答）

1. `list` 和 `tuple` 的区别是什么？什么时候用哪个？
2. `try/except/else/finally` 里的 `else` 什么时候执行？
3. 为什么读文件要写 `encoding="utf-8"`？
4. `if __name__ == "__main__":` 有什么用？
5. 虚拟环境解决了什么问题？
6. 类型注解写了之后，Python 运行时真的会检查吗？
7. pydantic 校验失败抛的是什么异常？
8. 为什么要给失败重试加"退避"（等待时间递增）？
9. `ensure_ascii=False` 是干什么的？
10. `git add` / `git commit` / `git push` 分别在做什么？

答不上来的，就是明天要补的。
