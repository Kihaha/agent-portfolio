"""练习 2：调用 API + 存 JSON + 失败重试

这是本周的核心练习——第 2 周你调大模型 API 用的是**完全一样的模式**：
发请求 → 判断结果 → 失败重试 → 存下来 → 读回来。

怎么写：
  1. 先写 save_json / load_json（简单）
  2. 再写 fetch_json（核心：重试逻辑）
  3. 最后写 main，并真实跑一次：
         uv run python exercises/ex2_api_json.py
  4. 跑测试：uv run pytest exercises -v -k ex2
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv


class FetchError(Exception):
    """请求重试多次后仍然失败时抛出的自定义异常。

    为什么不用 Exception？——调用方可以只捕获 FetchError，
    而不会误吞掉自己代码里的其他 bug。
    """


def fetch_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    retries: int = 3,
    timeout: float = 10.0,
    backoff: float = 0.5,
) -> dict:
    """GET 一个 URL，返回解析后的 JSON（顶层必须是 dict）。

    要求：
      - 最多请求 retries 次（retries=3 → 最多 3 次）
      - 每次失败后等待时间递增：backoff, backoff*2, backoff*4 ...（用 time.sleep）
      - 以下情况都算"这一次失败"，要重试：
          * 网络异常（httpx.HTTPError 及其子类）
          * HTTP 状态码不是 200
          * 响应不是合法 JSON，或 JSON 顶层不是 dict
      - 全部尝试都失败 → raise FetchError，消息里包含「尝试了几次」和最后一次的错误
      - 成功 → 直接返回 dict

    提示：
      - httpx.get(url, timeout=timeout)
      - resp.raise_for_status() 会在 4xx/5xx 时抛异常，用它可以把两种情况合并
      - 用 for 循环 + 一个 last_error 变量保存最后一次异常
      - 最后 raise FetchError(f"...") from last_error，保留原因链
    """
    last_error = None
    for i in range(retries):
        try:
            r = httpx.get(url, headers=headers, timeout=timeout)
            r.raise_for_status()
            b = r.json()
            if not isinstance(b, dict):
                raise ValueError(f"顶层不是 dict，而是 {type(b).__name__}")
            return b
        except (httpx.HTTPError, ValueError) as e:
            print("失败:", type(e).__name__, "|", e)
            if i < retries - 1:
                time.sleep(backoff * 2**i)

            last_error = e
    raise FetchError(f"尝试了{retries}次，最后的错误为{last_error}") from last_error


def save_json(data: dict, path: str | Path) -> None:
    """把 dict 写进 JSON 文件。

    要求：
      - 父目录不存在时自动创建
      - 中文**不要**被转义成 \\uXXXX（json.dump 的 ensure_ascii=False）
      - 缩进 2 空格，方便人看
      - 打开文件时显式写 encoding="utf-8"

    提示：Path(path).parent.mkdir(parents=True, exist_ok=True)
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="UTF-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path: str | Path) -> dict:
    """读取 JSON 文件并返回 dict。"""
    p = Path(path)
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    return data


def main() -> None:
    """真实调用一次 DeepSeek 的模型列表接口，存盘后再读回来打印。

    接口：https://api.deepseek.com/models
    需要请求头：{"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"}

    步骤：
      1. load_dotenv() 读取 .env 里的 key；没有 key 就打印提示并返回
      2. 调 fetch_json 拿到 {"object": "list", "data": [...]}
      3. 用 save_json 存到 data/models.json
      4. 用 load_json 读回来，打印里面每个模型的 id

    提示：
      - fetch_json 目前不支持自定义请求头 —— 请自己给 fetch_json 加一个
        headers: dict[str, str] | None = None 参数（这是正常的接口演进）
      - 打印时只打印 id 列表就够了，别把整个响应刷屏
    """
    load_dotenv()
    key = os.getenv("DEEPSEEK_API_KEY")
    path = "data/models.json"
    if not key:
        print("key不存在，返回")
        return
    json_out = fetch_json(
        url="https://api.deepseek.com/models", headers={"Authorization": f"Bearer {key}"}
    )
    save_json(json_out, path)
    data = load_json(path)
    for i in data["data"]:
        print(i["id"])


if __name__ == "__main__":
    main()
