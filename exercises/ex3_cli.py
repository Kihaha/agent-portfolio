"""练习 3：命令行小工具（argparse + 纯函数）

目标：学会把「计算逻辑」和「命令行外壳」分开。
这是"随手写的脚本"和"工程代码"的分界线——纯函数好测试、好复用，
以后 Agent 项目里的工具函数都是这个写法。

怎么写：
  1. 先写 parse_numbers（纯函数，好测）
  2. 再写 stats（纯函数）
  3. 最后写 main（只负责读参数、调用、打印）
  4. 测试：uv run pytest exercises -v -k ex3
  5. 真实使用：uv run python exercises/ex3_cli.py "1 2 3 4" --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_numbers(text: str) -> tuple[list[float], list[str]]:
    """把一串文本解析成数字，返回 (合法数字列表, 非法片段列表)。

    要求：
      - 分隔符既支持空白符也支持逗号："1, 2 3" → [1.0, 2.0, 3.0]
      - 空字符串、纯空白 → ([], [])
      - 转不成 float 的片段原样放进第二个列表："1, abc 3" → ([1.0, 3.0], ["abc"])
      - 合法数字统一转成 float

    提示：
      - text.replace(",", " ").split() 一次搞定两种分隔符
      - 用 try / except ValueError 包住 float(item)
    """
    values: list[float] = []
    bad: list[str] = []

    # 逗号先换成空格，两种分隔符就统一成一种，一次 split() 全部切开
    for item in text.replace(",", " ").split():
        try:
            values.append(float(item))
        except ValueError:
            # 转不动就原样记下来；不抛异常——因为"有几个片段看不懂"是预期内的输入，
            # 不是程序 bug，交给 main 决定怎么告诉用户
            bad.append(item)

    return values, bad


def stats(values: list[float]) -> dict[str, float | int | None]:
    """返回统计结果，键固定为：count、sum、mean、min、max。

    要求：
      - values 为空时：count=0，其余四个都是 None（不要抛异常、不要除以零）
      - mean 保留 2 位小数：round(x, 2)
      - min/max 用内置函数

    提示：空列表要单独判断，这是"边界条件"，面试也爱问

    """
    # 边界条件先处理：空列表不能进下面的除法，否则 ZeroDivisionError
    if not values:
        return {"count": 0, "sum": None, "mean": None, "min": None, "max": None}

    total = sum(values)
    return {
        "count": len(values),
        "sum": total,
        "mean": round(total / len(values), 2),
        "min": min(values),
        "max": max(values),
    }


def main(argv: list[str] | None = None) -> int:
    """命令行入口，返回退出码（0=成功，2=没有输入）。

    要求：
      - 位置参数 numbers（字符串，可以省略）
      - 可选参数 --file / -f：从文件里读内容
      - 可选参数 --json：以 JSON 输出；不加则输出人类可读的多行文本
      - 既没给 numbers 也没给 --file → 打印用法提示，返回 2
      - 有非法片段时，把非法片段打印到 **stderr**（不影响正常输出）
      - 返回 0 表示成功

    提示：
      - parser = argparse.ArgumentParser(description="统计一串数字")
      - parser.add_argument("numbers", nargs="?", default="")
      - parser.add_argument("--file", "-f")
      - parser.add_argument("--json", action="store_true")
      - args = parser.parse_args(argv)     # argv 传 None 时 argparse 自动读 sys.argv
      - print(..., file=sys.stderr)

    """
    parser = argparse.ArgumentParser(description="统计一串数字")
    parser.add_argument("numbers", nargs="?", default="")
    parser.add_argument("--file", "-f")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    # main 只做三件事：拿输入 → 调纯函数 → 打印。计算逻辑全在上面两个函数里
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = args.numbers
        if not text.strip():
            # 用法提示进 stderr，退出码 2 让 shell 和 CI 能判断"这次没干活"
            parser.print_usage(sys.stderr)
            print("错误：请提供一串数字，或用 --file 指定文件", file=sys.stderr)
            return 2

    values, bad = parse_numbers(text)
    if bad:
        # 只提醒，不污染 stdout —— 不然 --json 的输出就没法被程序解析了
        print(f"已忽略非法片段: {', '.join(bad)}", file=sys.stderr)

    result = stats(values)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"个数: {result['count']}")
        print(f"总和: {result['sum']}")
        print(f"平均: {result['mean']}")
        print(f"最小: {result['min']}")
        print(f"最大: {result['max']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
