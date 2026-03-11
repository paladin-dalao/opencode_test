 Python 工具脚本与 OpenCode GitHub Actions 示例仓库
> 说明：未特别标注的内容均直接来自本仓库代码或配置；带“（推测）”字样的为基于现有信息的合理推断。
 项目简介
本仓库是一个 **小型 Python 工具脚本 + OpenCode GitHub Actions 示例** 仓库，主要包含两部分：
1. **本地 Python 工具脚本**
   - `toolkit.py`：一个集成了日志、文件与目录操作、时间与日期处理、HTTP 请求、JSON/CSV 读写、正则匹配、系统信息等常用功能的工具脚本，并内置简单测试示例。
   - `hello.py`：一个 “Hello World” 示例脚本，目前代码中存在缩进错误，用于演示或练习修复基础语法问题。
2. **GitHub Actions 工作流（OpenCode 集成示例）**
   - `.github/workflows/opencode.yml`：通过特殊评论指令触发的 OpenCode 工作流。
   - `.github/workflows/issue_opencode.yml`：在 Issue 创建时尝试自动修复问题并创建 PR 的工作流。
   - `.github/workflows/review_opencode.yml`：在 Pull Request 生命周期中自动触发的代码评审工作流。
所有 OpenCode 相关工作流均依赖 `DASHSCOPE_API_KEY` GitHub Secret，用于在 GitHub Actions 中调用 `anomalyco/opencode/github@latest` Action 及对应模型。
---
 功能特性
 1. Python 工具脚本功能（`toolkit.py`）
文件：`toolkit.py`
工具脚本使用的标准库与第三方库：
- 标准库：`os`, `sys`, `json`, `time`, `datetime`, `csv`, `re`, `shutil`, `logging`
- 第三方库：`requests`（在文件头部文档字符串中明确说明需提前安装）
主要功能函数：
1. **日志配置（logging）**
   - `setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger`
     - 配置同时输出到 **日志文件** 和 **控制台** 的 Logger。
     - 避免重复添加处理器（如果同名 logger 已经有 handlers 则直接返回）。
     - 默认在当前工作目录下创建/写入 `toolkit.log` 日志文件：
              logger = setup_logger("python_toolkit", "toolkit.log")
       
2. 文件 / 目录操作（os、shutil）
   - create_dir(dir_path: str) -> bool
     - 递归创建多级目录（os.makedirs(..., exist_ok=True)）。
     - 成功或失败均记录日志，返回 True 或 False。
   - copy_file(src_path: str, dst_path: str) -> bool
     - 复制文件（shutil.copy2，保留文件元数据）。
     - 成功或失败均记录日志，返回布尔结果。
   - list_files(dir_path: str, ext: str = None) -> list
     - 列出指定目录下的文件。
     - 可选按扩展名过滤（例如 .txt）。
     - 返回文件路径列表，并记录日志。
3. 时间 / 日期处理（time、datetime）
   - get_current_time(format: str = "%Y-%m-%d %H:%M:%S") -> str
     - 以指定格式返回当前时间字符串。
     - 发生异常时记录错误日志，返回空字符串。
   - timestamp_to_datetime(timestamp: float, format: str = "%Y-%m-%d %H:%M:%S") -> str
     - 将秒级时间戳转换为格式化日期时间字符串。
     - 异常时记录错误日志，返回空字符串。
4. 网络请求（requests）
   - http_get(url: str, params: dict = None, headers: dict = None) -> dict
     - 发送 HTTP GET 请求，超时时间 10 秒。
     - 返回结构：
              {
           "status_code": <int>,
           "data": <解析后的 JSON 或原始文本>,
           "error": <错误信息字符串或空字符串>
       }
            - 优先尝试解析 JSON，失败则返回 response.text。
   - http_post(url: str, data: dict = None, json_data: dict = None, headers: dict = None) -> dict
     - 发送 HTTP POST 请求，支持 form 表单（data）或 JSON（json_data）。
     - 返回结构与 http_get 一致。
     - 同样优先解析 JSON，失败则返回文本。
5. 数据解析（json、csv、re）
   - read_json(file_path: str) -> dict
     - 读取 JSON 文件并返回字典（失败时返回空字典）。
   - write_json(file_path: str, data: dict, indent: int = 4) -> bool
     - 将字典写入 JSON 文件。
     - 使用 UTF-8 编码与自定义缩进空格数。
   - read_csv(file_path: str, delimiter: str = ",") -> list
     - 使用 csv.DictReader 读取 CSV 文件。
     - 返回由行字典组成的列表。
   - regex_match(pattern: str, text: str) -> list
     - 使用 re.findall 执行正则匹配。
     - 返回匹配结果列表，并在日志中记录匹配数量。
6. 系统信息（sys、os）
   - get_system_info() -> dict
     - 返回系统基础信息字典，包括：
       - python_version
       - platform
       - current_dir
       - cpu_count
       - env_path（环境变量 PATH）
7. 内置测试代码（仅在直接运行时）
   当直接执行 toolkit.py（python toolkit.py 或 ./toolkit.py）时，会执行：
      if __name__ == "__main__":
       print("=== 测试工具文件功能 ===")
       logger.info("开始测试工具文件")
       print("当前时间：", get_current_time())
       create_dir("test_dir")
       sys_info = get_system_info()
       print("Python 版本：", sys_info["python_version"])
       response = http_get("https://www.baidu.com")
       print("百度请求状态码：", response["status_code"])
       logger.info("工具文件测试完成")
   
   这会在本地：
   - 打印当前时间和 Python 版本。
   - 创建 test_dir 目录。
   - 向 https://www.baidu.com 发起 GET 请求，并打印状态码（需要外网访问百度）。
   - 在 toolkit.log 中记录执行过程。
2. 示例脚本（hello.py）
文件：hello.py
当前内容节选：
# 定义一个变量存储要输出的内容
message = "Hello World! 👋"
# 打印变量中的内容
    print(message)
# 也可以打印多个内容，用逗号分隔，会自动用空格隔开
print("Hello", "Python!")
- 作用（设计意图）：演示最基础的 Python 输出语句与变量打印（推测）。
- 现状（事实）：第 4 行 print(message) 多了一个缩进，但前面并没有 if、for 等代码块，会导致运行时报 IndentationError，因此当前文件无法直接运行。
修复方向（文字提示）：
- 使第 4 行与第 1 行左对齐，去掉多余缩进，例如改为：
    # 定义一个变量存储要输出的内容
  message = "Hello World! 👋"
  # 打印变量中的内容
  print(message)
  # 也可以打印多个内容，用逗号分隔，会自动用空格隔开
  print("Hello", "Python!")
  
---
目录结构
仓库根目录（简化展示）：
.
├── toolkit.py                # Python 常用工具脚本，集成多种实用函数并含自测入口
├── hello.py                  # 简单 Hello World 示例脚本（当前存在缩进错误）
├── .git/                     # Git 仓库元数据目录（由 Git 自动维护）
└── .github/
    └── workflows/
        ├── opencode.yml         # 通过评论指令触发 OpenCode 的工作流
        ├── issue_opencode.yml   # 新 Issue 打开时自动尝试修复并创建 PR 的工作流
        └── review_opencode.yml  # PR 打开/更新时执行自动代码评审的工作流
> 当前项目中未发现 requirements.txt、pyproject.toml 等依赖声明文件，依赖需手动安装或由使用者自行补充相关配置文件。
---
快速开始
1. 环境准备
1. Python 版本
   - toolkit.py 顶部 Shebang：#!/usr/bin/env python3  
     说明需要使用 Python 3 运行。
   - 推荐使用 Python 3.8+ 以获得更好的兼容性（推测，依据类型注解与常见实践）。
2. 安装依赖
   项目中唯一使用的第三方库为 requests（在 toolkit.py 文档字符串中有明确说明）。
   使用 pip 安装示例：
      # 使用系统默认 Python
   pip install requests
   # 或者显式指定 Python 3
   python3 -m pip install requests
   
   > 由于仓库中没有 requirements.txt，如果后续新增依赖，建议自行创建并维护（当前尚未提供）。
2. 本地运行 toolkit.py
在仓库根目录下执行：
方式一：使用 Python 直接运行
cd /path/to/this/repo
python3 toolkit.py
# 或者
python toolkit.py  # 视本地 python 指向版本而定
预期行为（基于 __main__ 测试代码）：
- 终端中打印：
  - === 测试工具文件功能 ===
  - 当前时间
  - Python 版本
  - 百度请求的 HTTP 状态码
- 当前目录下生成：
  - test_dir/ 目录
  - toolkit.log 日志文件（包含详细日志记录）
> 若本机无法访问 https://www.baidu.com，http_get 调用可能失败并在日志中记录错误，此时状态码可能保持为 0，error 字段中则包含异常信息。
方式二：赋予执行权限后作为脚本运行（类 Unix 系统）
cd /path/to/this/repo
chmod +x toolkit.py
./toolkit.py
行为与方式一相同。
3. 运行或修复 hello.py
当前直接运行会触发缩进错误：
cd /path/to/this/repo
python3 hello.py
# 将报 IndentationError
修复方向（示意而非补丁）：
- 删除第 4 行前面的缩进，使 print(message) 左对齐到行首，保证与 message = ... 等处于同一缩进层级。
修复后即可正常打印：
Hello World! 👋
Hello Python!
---
CI / GitHub Actions
所有工作流文件位于：.github/workflows/
并均使用 anomalyco/opencode/github@latest Action 与模型 alibaba-cn/deepseek-r1，同时声明环境变量：
env:
  DASHSCOPE_API_KEY: ${{ secrets.DASHSCOPE_API_KEY }}
这表明：
- 必须在 GitHub 仓库中配置名为 DASHSCOPE_API_KEY 的 Repository Secret。
- 该 Secret 被用于在工作流中调用 OpenCode 所依赖的后端服务进行推理（推测，依据 Action 名称与环境变量命名）。
1. opencode.yml — 评论触发的助手
文件：.github/workflows/opencode.yml
触发条件（on）：
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
并通过 if 条件过滤，仅在评论内容满足以下任一条件时触发：
- 评论中包含 ' /oc' 或以 '/oc' 开头
- 评论中包含 ' /opencode' 或以 '/opencode' 开头
示例触发方式（在 Issue 或 PR 的评论中）：
- /oc 帮我看看这个函数有没有问题？
- /opencode 请解释一下这个 CI 配置
工作流行为：
- 使用 actions/checkout@v6 拉取代码。
- 调用 anomalyco/opencode/github@latest，使用模型 alibaba-cn/deepseek-r1。
- 具体对评论做出的行为（例如回复评论、修改代码等）由该 Action 内部逻辑决定（推测，不在本仓库中体现）。
2. issue_opencode.yml — 新 Issue 自动处理与修复示例
文件：.github/workflows/issue_opencode.yml
触发条件：
on:
  issues:
    types: [opened]
即 新 Issue 被创建 时自动执行。
核心配置：
- 使用 actions/checkout@v4 检出仓库。
- 权限设置：
  - contents: write
  - pull-requests: write
  - issues: write
  - id-token: write
- 调用 anomalyco/opencode/github@latest Action，并附带一段详细的 prompt，要求模型：
  - 阅读和总结 Issue。
  - 搜索仓库相关代码。
  - 如果 Issue 描述的是 bug 或改进点：
    - 实现修复。
    - 更新或新增测试（如果需要）。
    - 提交代码。
    - 创建 Pull Request。
  - 如果无法自动修复：
    - 在 Issue 下发表评论，给出建议或提出问题。
这使得该工作流可作为 自动 Issue triage 与修复示例 使用（推测：实际效果视 OpenCode 能力与仓库内容而定）。
3. review_opencode.yml — PR 自动代码评审
文件：.github/workflows/review_opencode.yml
触发条件：
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
即在以下 PR 事件发生时执行：
- 新建 PR（opened）
- 推送新提交到 PR（synchronize）
- 重新打开 PR（reopened）
- 将 Draft PR 标记为“Ready for review”（ready_for_review）
工作流行为：
- 使用 actions/checkout@v4 检出仓库。
- 调用 anomalyco/opencode/github@latest，模型为 alibaba-cn/deepseek-r1。
- prompt 明确要求模型对当前 PR 执行代码评审，重点关注：
  - 代码质量与可读性
  - 潜在 bug 或边界情况
  - 安全性问题
  - 性能问题
  - 提出改进建议
评审结果通常会以评论或 Review 形式回到 PR（推测，具体行为由 Action 实现）。
---
技术栈与依赖
1. 编程语言
   - Python 3（toolkit.py 中使用 #!/usr/bin/env python3 Shebang，且存在类型注解与 f-string 等 Python 3 特性）。
2. Python 依赖
   - 标准库：os, sys, json, time, datetime, csv, re, shutil, logging
   - 第三方库：requests（必须手动安装，仓库中无自动依赖声明文件）
3. CI / GitHub Actions
   - actions/checkout：
     - @v4（在 issue_opencode.yml 与 review_opencode.yml 中使用）
     - @v6（在 opencode.yml 中使用）
   - OpenCode 集成：
     - uses: anomalyco/opencode/github@latest
     - 模型：alibaba-cn/deepseek-r1
   - Secret：
     - DASHSCOPE_API_KEY：通过 secrets.DASHSCOPE_API_KEY 注入到环境变量，用于鉴权访问 OpenCode 背后的服务（推测）。
---
注意事项
1. Python 与依赖
   - 确保本地安装的是 Python 3，并已安装 requests。
   - 仓库未提供 requirements.txt，如需在团队中共享依赖管理，建议手动补充该文件（当前为使用者自定义内容）。
2. 网络访问
   - 本地运行 toolkit.py 自测代码时，会请求 https://www.baidu.com：
     - 无法访问外网或被防火墙限制时，http_get 可能失败，response["status_code"] 可能保持为 0，并在日志中记录异常。
   - GitHub Actions 在运行 OpenCode 相关步骤时，也需要访问外部服务（推测，至少需要访问 OpenCode 所在的 API 服务端）。
3. 日志与文件生成
   - 运行 toolkit.py 时会在当前工作目录自动生成：
     - toolkit.log：日志文件。
     - test_dir/：用于文件操作示例的测试目录。
   - 如在 CI 或有限权限环境下运行，需要确认对这些路径具有写权限。
4. GitHub Secrets 配置
   - 所有 OpenCode 相关工作流都依赖 DASHSCOPE_API_KEY：
     - 若未配置该 Secret，相关工作流将无法成功调用模型，通常会在 Action 日志中报错。
   - 配置方式（仅文字说明）：
     - 在 GitHub 仓库页面 → Settings → Secrets and variables → Actions → 新建 Repository Secret：
       - Name：DASHSCOPE_API_KEY
       - Value：从对应服务控制台获取的 API Key（推测，通常来自 DashScope 或 OpenCode 提供方）。
5. 示例脚本状态
   - hello.py 当前存在缩进错误，直接运行会失败。
   - 若在 CI 中执行该脚本，需先修复缩进问题或避免调用。
---
后续扩展建议（推测）
以下为基于当前仓库内容的扩展建议，非现有事实：
- 为 toolkit.py 新增更完整的命令行接口（如使用 argparse），方便从命令行调用单个子功能（如仅执行 HTTP 请求或文件复制）。
- 增加简单的测试用例（例如使用 pytest）并在 GitHub Actions 中增加对应的测试工作流。
- 提供 requirements.txt 或 pyproject.toml，明确依赖版本，提升可复现性。
- 在 README 中补充更多 OpenCode 使用示例，例如实际评论触发指令与交互截图（在后续实际使用中补充）。
---
