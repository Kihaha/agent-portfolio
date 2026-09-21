"""第 1 周练习的自动测试。**不要修改这个文件。**

运行方式（在 agent-portfolio 目录下）：

    uv run pytest exercises -v            # 跑全部
    uv run pytest exercises -v -k ex1     # 只跑练习 1
    uv run pytest exercises -v -x         # 遇到第一个失败就停

刚拿到时**全是红的**（NotImplementedError），这是正常的：
红 = 还没实现。目标是让它们一个个变绿。

每个练习通过后都建议 `git add` + `git commit` 一次——
面试官看的就是这种渐进式的提交历史。
"""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

import ex1_files as ex1
import ex2_api_json as ex2
import ex3_cli as ex3
import ex4_pydantic as ex4


# ============================================================
# 练习 1：文件处理
# ============================================================


def test_ex1_list_files(tmp_path):
    (tmp_path / "a.csv").write_text("hello", encoding="utf-8")
    (tmp_path / "b.txt").write_text("hi", encoding="utf-8")
    (tmp_path / "c.CSV").write_text("hello!", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "inner.csv").write_text("x", encoding="utf-8")

    names = [p.name for p in ex1.list_files(tmp_path)]
    assert names == ["a.csv", "b.txt", "c.CSV"], "要按文件名排序，排除子目录，且不递归"

    only_csv = [p.name for p in ex1.list_files(tmp_path, ".csv")]
    assert only_csv == ["a.csv"], "后缀过滤是大小写敏感的"


def test_ex1_list_files_missing_dir(tmp_path):
    with pytest.raises(FileNotFoundError):
        ex1.list_files(tmp_path / "not-exist")


def test_ex1_total_size(tmp_path):
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")  # 5 字节
    (tmp_path / "b.txt").write_text("hi", encoding="utf-8")     # 2 字节
    assert ex1.total_size(ex1.list_files(tmp_path)) == 7
    assert ex1.total_size([]) == 0


def test_ex1_group_by_suffix(tmp_path):
    for name in ["a.csv", "b.CSV", "c.txt", "noext"]:
        (tmp_path / name).write_text("x", encoding="utf-8")
    counts = ex1.group_by_suffix(ex1.list_files(tmp_path))
    assert counts[".csv"] == 2, "大小写不同的后缀要合并"
    assert counts[".txt"] == 1
    assert counts[""] == 1, "没有后缀的文件归到空字符串"


def test_ex1_main_runs(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.txt").write_text("hi", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    ex1.main()
    assert capsys.readouterr().out.strip() != "", "main 应该打印一些汇总信息"


# ============================================================
# 练习 2：API + JSON + 重试
# ============================================================


class _FlakyHandler(BaseHTTPRequestHandler):
    """前 fail_times 次请求返回 500，之后返回 200 + JSON。"""

    fail_times = 0
    requests = 0

    def do_GET(self):  # noqa: N802
        type(self).requests += 1
        if type(self).fail_times > 0:
            type(self).fail_times -= 1
            body = b"server error"
            self.send_response(500)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        body = json.dumps({"ok": True, "名字": "测试"}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


@pytest.fixture()
def json_server():
    _FlakyHandler.fail_times = 0
    _FlakyHandler.requests = 0
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), _FlakyHandler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        yield f"http://127.0.0.1:{httpd.server_address[1]}"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_ex2_retry_then_success(json_server):
    _FlakyHandler.fail_times = 2
    data = ex2.fetch_json(json_server, retries=3, backoff=0.01)
    assert data["ok"] is True
    assert _FlakyHandler.requests == 3, "失败 2 次 + 成功 1 次 = 共 3 次请求"


def test_ex2_all_failed_raises(json_server):
    _FlakyHandler.fail_times = 99
    with pytest.raises(ex2.FetchError):
        ex2.fetch_json(json_server, retries=2, backoff=0.01)
    assert _FlakyHandler.requests == 2, "retries=2 表示最多请求 2 次"


def test_ex2_save_and_load(tmp_path):
    path = tmp_path / "sub" / "data.json"  # 父目录不存在，应自动创建
    ex2.save_json({"名称": "测试", "值": 1}, path)
    raw = path.read_text(encoding="utf-8")
    assert "测试" in raw, "ensure_ascii=False 才能让中文可读"
    assert ex2.load_json(path) == {"名称": "测试", "值": 1}


# ============================================================
# 练习 3：命令行工具
# ============================================================


def test_ex3_parse_numbers():
    values, bad = ex3.parse_numbers("1, 2 3")
    assert values == [1.0, 2.0, 3.0]
    assert bad == []

    values, bad = ex3.parse_numbers("1, abc 3")
    assert values == [1.0, 3.0]
    assert bad == ["abc"]

    assert ex3.parse_numbers("") == ([], [])
    assert ex3.parse_numbers("   ") == ([], [])


def test_ex3_stats():
    s = ex3.stats([1.0, 2.0, 3.0, 4.0])
    assert s["count"] == 4
    assert s["sum"] == 10.0
    assert s["mean"] == 2.5
    assert s["min"] == 1.0
    assert s["max"] == 4.0

    empty = ex3.stats([])
    assert empty["count"] == 0
    assert empty["mean"] is None, "空列表不能除以零"


def test_ex3_main(capsys):
    assert ex3.main(["1 2 3", "--json"]) == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["count"] == 3

    assert ex3.main([]) == 2, "没有输入时返回 2"


# ============================================================
# 练习 4：pydantic 校验
# ============================================================


def test_ex4_parse_valid():
    msg = ex4.parse_message({"role": "user", "content": "你好"})
    assert msg.role == "user"
    assert msg.content == "你好"

    msgs = ex4.parse_messages(
        [{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}]
    )
    assert [m.role for m in msgs] == ["user", "assistant"]


def test_ex4_parse_invalid():
    with pytest.raises(ValueError):
        ex4.parse_message({"role": "boss", "content": "hi"})  # 非法 role
    with pytest.raises(ValueError):
        ex4.parse_message({"role": "user", "content": ""})  # 空内容
    with pytest.raises(ValueError):
        ex4.parse_message({"role": "user", "content": 123})  # 类型不对
    with pytest.raises(ValueError):
        ex4.parse_messages([{"role": "user", "content": "ok"}, {"role": "user"}])  # 缺字段


def test_ex4_demo_validation_error():
    text = ex4.demo_validation_error()
    assert isinstance(text, str)
    assert "content" in text or "role" in text, "错误信息里应该指出出问题的字段"
