"""练习 4：类型注解 + pydantic（本周最重要）

为什么这个最重要？
  Agent 工程里到处是"不可信的数据"：模型返回的 JSON、工具调用的参数、
  第三方 API 的响应。如果不校验就直接用，脏数据会一路传染到很深的地方，
  最后报一个跟真正原因毫无关系的错。pydantic 就是那道关卡。
  第 2 周开始，你写的每个模型接口、每个工具定义都会用到它。

怎么写：
  1. 模型（Message / ToolCall）已经写好了，**先读懂它**
  2. 实现 parse_message（用 model_validate，把 ValidationError 转成 ValueError）
  3. 实现 parse_messages（批量 + 指出第几条出错）
  4. 实现 demo_validation_error（亲眼看看校验错误长什么样）
  5. 测试：uv run pytest exercises -v -k ex4
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    """一条对话消息。

    role 只允许这四种取值；content 不能是空字符串。
    注意：这些约束在**创建对象时**就会生效，不是文档式的约定。
    """

    role: Literal["system", "user", "assistant", "tool"]
    content: str = Field(min_length=1)


class ToolCall(BaseModel):
    """模型请求调用一个工具。"""

    name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)
    call_id: str | None = None


def parse_message(raw: dict[str, Any]) -> Message:
    """把原始 dict 校验成 Message 对象。

    要求：
      - 用 Message.model_validate(raw)
      - 如果抛出 pydantic.ValidationError，把它转成 ValueError 再抛出去，
        消息里要包含原始的报错文本：raise ValueError(f"...{exc}") from exc

    为什么要转换？
      上层代码只需要处理一种异常类型（ValueError），而且消息可读。
      这也叫"在边界处把第三方异常翻译成自己的异常"。
    """
    raise NotImplementedError("TODO: 实现 parse_message")


def parse_messages(raw_list: list[dict[str, Any]]) -> list[Message]:
    """批量校验消息列表。

    要求：
      - 全部合法 → 返回 Message 列表（顺序不变）
      - 只要有一条不合法 → raise ValueError，消息里要说明是**第几条**（下标从 0 开始）
        例如："第 1 条消息不合法: ..."

    提示：用 enumerate 拿到下标；第 i 条出错时 message 里带上 i
    """
    raise NotImplementedError("TODO: 实现 parse_messages")


def demo_validation_error() -> str:
    """演示校验的价值：故意造一条坏数据，捕获 ValidationError，返回它的字符串形式。

    要求：
      - 用 Message.model_validate({"role": "user", "content": ""}) 触发错误
      - 捕获 pydantic.ValidationError，返回 str(exc)

    看完输出你就明白：错误信息会明确告诉你"哪个字段、为什么不行"，
    这比"运行到后面某处突然 TypeError"好太多。
    """
    raise NotImplementedError("TODO: 实现 demo_validation_error")


if __name__ == "__main__":
    print(demo_validation_error())
