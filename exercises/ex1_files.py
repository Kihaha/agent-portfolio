"""练习 1：批量文件处理

目标：把 Python 的「循环 + 路径 + 异常」真正用起来。

怎么写：
  1. 打开本文件，从 list_files 开始，把 raise NotImplementedError 换成真正的实现
  2. 每写完一个函数就存盘，然后跑测试：
         uv run pytest exercises -v -k ex1
  3. 红 → 黄 → 绿。全绿就说明这个练习过了

要求、提示、示例都写在每个函数的 docstring 里，先自己写，卡 30 分钟再来问。
"""

from __future__ import annotations

from pathlib import Path


def list_files(directory: str | Path, suffix: str = "") -> list[Path]:
    """列出目录下的文件（不递归），按文件名排序。

    要求：
      - directory 不存在、或不是一个目录 → raise FileNotFoundError，消息里包含这个路径
      - suffix 为空字符串时，返回全部文件
      - suffix 非空时，只返回文件名以它结尾的文件（**大小写敏感**）
      - 结果按文件名的字典序排序
      - 子目录不算文件，要排除掉

    提示：
      - 用 pathlib.Path(directory)
      - Path.iterdir() 会同时返回目录和文件，需要用 p.is_file() 过滤
      - 排序：sorted(..., key=lambda p: p.name)

    示例：
      list_files("data", ".csv")
      # [PosixPath('data/a.csv'), PosixPath('data/b.csv')]
    """
    raise NotImplementedError("TODO: 实现 list_files")


def total_size(paths: list[Path]) -> int:
    """返回这些文件的总字节数；空列表返回 0。

    提示：Path.stat().st_size
    """
    raise NotImplementedError("TODO: 实现 total_size")


def group_by_suffix(paths: list[Path]) -> dict[str, int]:
    """按后缀统计文件数量，例如 {".csv": 2, ".txt": 1}。

    要求：
      - 没有后缀的文件归到 "" 这一类
      - 后缀统一转小写（".CSV" 和 ".csv" 算同一类）
      - 只统计出现过的后缀（没出现的不要在结果里）

    提示：Path.suffix；用 counts[key] = counts.get(key, 0) + 1
    """
    raise NotImplementedError("TODO: 实现 group_by_suffix")


def main() -> None:
    """打印当前目录下所有文件的汇总：文件总数、总大小、按后缀分布。

    提示：
      - 用 list_files(".") 拿文件，再调用上面两个函数
      - 用 f-string 打印，例如：print(f"文件数: {len(files)}")
      - 总大小建议换算成 KB 显示（字节数 / 1024，保留 2 位小数）
    """
    raise NotImplementedError("TODO: 实现 main")


if __name__ == "__main__":
    main()
