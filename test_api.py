"""P0 验收脚本：确认你能成功调用一次大模型 API。

用法（在 agent-portfolio 目录下执行）：
    uv run python test_api.py

它会按顺序自动尝试：
    1) .env 里的 DeepSeek        （DEEPSEEK_API_KEY）
    2) 本地 Ollama               （http://127.0.0.1:11434/v1，免费、无需联网）
    3) .env 里的通义千问          （DASHSCOPE_API_KEY）
    4) .env 里的智谱 GLM         （ZHIPU_API_KEY）

全部失败时会直接打印下一步该做什么。
注意：本脚本故意只用 httpx 发原始 HTTP 请求，这样你能看清
"OpenAI 兼容接口" 的真实形状——后面换成 openai SDK 时，参数是一一对应的。
"""

from __future__ import annotations

import os
import sys

import httpx
from dotenv import load_dotenv

# 各家服务商的 OpenAI 兼容地址、模型名、以及 key 所在的环境变量名
PROVIDERS = [
    {
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
        "key_env": "DEEPSEEK_API_KEY",
    },
    {
        "name": "Ollama 本地模型（免费）",
        "base_url": "http://127.0.0.1:11434/v1",
        "model": "qwen3:1.7b",
        "key_env": None,
    },
    {
        "name": "通义千问（阿里云百炼）",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
        "key_env": "DASHSCOPE_API_KEY",
    },
    {
        "name": "智谱 GLM",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-4-flash",
        "key_env": "ZHIPU_API_KEY",
    },
]

PROMPT = "用一句话介绍你自己，并说明你是哪个模型。"


def ask(provider: dict) -> str | None:
    """向一个服务商发一次请求；成功返回回复文本，失败返回 None。"""
    key_env = provider["key_env"]
    api_key = os.getenv(key_env) if key_env else None
    if key_env and not api_key:
        print(f"[跳过] {provider['name']}：.env 里还没填 {key_env}")
        return None

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": provider["model"],
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 0.7,
        "stream": False,
    }

    print(f"[尝试] {provider['name']}  (模型: {provider['model']})")
    try:
        resp = httpx.post(
            f"{provider['base_url']}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
    except Exception as exc:  # 网络层失败：连不上、超时
        print(f"[失败] 连不上：{exc}\n")
        return None

    if resp.status_code != 200:
        print(f"[失败] HTTP {resp.status_code}：{resp.text[:300]}\n")
        return None

    data = resp.json()
    text = data["choices"][0]["message"]["content"]
    usage = data.get("usage") or {}
    print(f"[成功] {provider['name']}")
    print(f"  回复：{text}")
    if usage:
        print(
            f"  用量：prompt_tokens={usage.get('prompt_tokens')} "
            f"completion_tokens={usage.get('completion_tokens')}"
        )
    print()
    return text


def main() -> int:
    load_dotenv()  # 读取同目录下的 .env

    for provider in PROVIDERS:
        if ask(provider):
            print("=" * 62)
            print("P0 验收通过：你已经成功调用一次大模型 API ✅")
            return 0

    print("=" * 62)
    print("所有服务商都没调通，按下面任意一条处理即可：")
    print()
    print("【方案 A】用 DeepSeek（推荐，便宜、国内直连）")
    print("  1. 打开 platform.deepseek.com 注册并充值（10 元够用很久）")
    print("  2. 在「API keys」里创建一个 key")
    print("  3. 填进 .env：  DEEPSEEK_API_KEY=sk-你的key")
    print("  4. 重新运行：  uv run python test_api.py")
    print()
    print("【方案 B】先用免费的本地模型（不花钱、断网也能跑）")
    print("  1. winget install --id Ollama.Ollama -e")
    print("  2. ollama pull qwen3:1.7b        （约 1.5GB）")
    print("  3. 重新运行：  uv run python test_api.py")
    print()
    print("提示：key 只能填进 .env，不要写进代码、也不要发给任何人。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
