# agent-portfolio

8 周 Agent 实习冲刺计划的**起步仓库**（P0 第 0 天用）。
后面三个简历项目都可以放进这个仓库，形成一条可展示的提交历史。

## 已包含的配置

| 文件 | 作用 |
|---|---|
| `.vscode/settings.json` | 保存即格式化、指定 Ruff、开启 Pylance 类型检查 |
| `.vscode/extensions.json` | 推荐扩展清单，VS Code 会自动提示一键安装 |
| `.gitignore` | **确保 `.env`（API key）永远不会被提交** |
| `.env.example` | 密钥模板，复制成 `.env` 后填自己的 key |

## 起步三步（Windows PowerShell）

```powershell
# 1) 安装 uv（一个工具替代 pip + venv + 依赖锁定）
winget install --id=astral-sh.uv -e
# 装完关掉当前终端，重新开一个，让 PATH 生效

# 2) 进入本仓库，创建虚拟环境（用 3.12，避开系统 3.14 的库兼容问题）
cd C:\Users\kk\Desktop\dsh\agent-portfolio
uv venv --python 3.12

# 3) 装第一批依赖并验证
uv pip install httpx python-dotenv
uv run python -c "import sys, httpx, dotenv; print(sys.executable)"
```

> ⚠️ 本机 PowerShell 执行策略是 **Restricted**，所以**不要**运行 `.venv\Scripts\Activate.ps1`（会报错）。
> 用 `uv run python 脚本.py` 即可，它在虚拟环境里执行、无需激活。
> 如果想彻底解决（同时能让 npm.ps1、VS Code 自动激活也能用），可以执行一次：
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## 使用密钥的方式

```powershell
Copy-Item .env.example .env
notepad .env          # 填入真实 key
```

代码里：

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
print("读取成功" if api_key else "还没填 key")
```

## 自检清单（本机已实测，2026-09-17）

- [x] `uv` 已安装：0.12.15（`%USERPROFILE%\.local\bin\uv.exe`）
- [x] `.venv` 已创建：Python **3.12.14**（与系统 Python 3.14 隔离）
- [x] 依赖可导入：`httpx 0.28.1`、`python-dotenv 1.2.3`
- [x] `uv run python ...` 的解释器确实在 `.venv` 内
- [x] `git check-ignore .env` 命中规则 `.gitignore:4` —— **密钥不会被提交**
- [x] `.venv` 被忽略（规则 `.gitignore:18`）
- [x] 换行符统一为 LF（`git ls-files --eol` → `i/lf w/lf`），避免以后 Dockerfile 出问题
- [ ] VS Code 右下角解释器显示 `.venv`（需要在 GUI 里点一次）
- [ ] 写 `x: int = "abc"` 出现类型波浪线（需要在 GUI 里确认）

## 完成首次提交（还差这一步）

仓库已 `git init -b main`，文件已暂存（6 个），只差 Git 身份：

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的GitHub邮箱"
git commit -m "chore: 初始化 agent-portfolio（VS Code 配置 + 依赖 + 密钥忽略）"
```

> 不想暴露真实邮箱，可用 GitHub 的 noreply 地址：`你的用户名@users.noreply.github.com`
> 提交前再确认一次：`git status` 里**不应该出现 `.env`**
