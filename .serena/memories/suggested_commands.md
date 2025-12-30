# 建议的命令 (Suggested Commands)

## 安装和部署

### 安装知识库
```bash
# 基本安装
cd /home/hao/Workspace/MM/utility/ai_workflow
bash scripts/install_knowledge_base.sh

# 卸载知识库
bash scripts/uninstall_knowledge_base.sh

# 使用 Makefile 便捷入口
make install    # 安装
make uninstall  # 卸载
make test       # 测试
make help       # 帮助
```

## 文档管理

### Frontmatter 验证
```bash
# 验证单个文档
python scripts/frontmatter_utils.py validate <file_path>

# 批量验证
python scripts/frontmatter_utils.py validate-batch docs/

# 更新 last_updated 字段
python scripts/frontmatter_utils.py update-date <file_path>
```

### 文档读取保护
```bash
# 基本用法
python scripts/doc_guard.py --docs "KNOWLEDGE.md"

# 指定章节模式
python scripts/doc_guard.py \
  --docs "docs/guides/large_guide.md" \
  --sections '{"docs/guides/large_guide.md": ["Step 3", "MCP Integration"]}'

# 摘要模式
python scripts/doc_guard.py \
  --docs "best-practices/document-architecture.md" \
  --max-lines 50
```

## Git 操作

### 基本流程
```bash
# 查看状态
git status

# 查看差异
git diff
git diff --stat

# 添加和提交
git add <files>
git commit -m "[type] 描述"

# 查看历史
git log --oneline -10
git log --graph --oneline --all -20
```

### 分支管理
```bash
# 创建分支
git checkout -b feature/new-feature

# 切换分支
git checkout dev/master
git checkout master

# 合并分支
git merge feature/new-feature
```

### 版本发布
```bash
# 创建标签
git tag -a v1.2.0 -m "Version 1.2.0: Description"

# 查看标签
git tag -l
git tag -l -n5 v1.2.0  # 查看标签消息

# 推送标签
git push origin v1.2.0
git push origin --tags  # 推送所有标签
```

## 项目导航

### 查找文件
```bash
# 查找 Markdown 文件
find . -name "*.md" -type f

# 查找 Python 文件
find . -name "*.py" -type f

# 排除某些目录
find . -name "*.md" -not -path "./archive/*" -not -path "./.git/*"
```

### 搜索内容
```bash
# 搜索文本
grep -r "keyword" --include="*.md" .

# 搜索并显示行号
grep -rn "keyword" --include="*.md" .

# 搜索多个关键词
grep -r -E "keyword1|keyword2" --include="*.md" .
```

### 目录结构
```bash
# 查看目录树
tree -L 2 -I '__pycache__|*.pyc|.git'

# 查看文件大小
du -sh */
du -h --max-depth=1 | sort -hr

# 统计文件数量
find . -type f -name "*.md" | wc -l
find . -type f -name "*.py" | wc -l
```

## 文档统计

### 行数统计
```bash
# 单个文件
wc -l <file>

# 所有 Markdown 文件
find . -name "*.md" -not -path "./archive/*" -exec wc -l {} + | sort -nr

# Python 代码统计
find commands/lib -name "*.py" -exec wc -l {} + | tail -1
```

### 内容分析
```bash
# 查找所有 ADR
ls -1 docs/adr/*.md | wc -l

# 查找所有最佳实践文档
ls -1 best-practices/*.md | wc -l

# 查找所有工具
ls -1 commands/lib/*.py | wc -l
```

## 工具使用

### DocLoader (智能文档加载)
```python
from commands.lib.doc_loader import DocLoader

loader = DocLoader()

# 摘要模式
summary = loader.load_summary("KNOWLEDGE.md", max_lines=50)

# 章节模式
content = loader.load_sections(
    "best-practices/document-architecture.md",
    sections=["Step 3", "MCP Integration"]
)
```

### AgentCoordinator (多 Agent 协调)
```python
from commands.lib.agent_coordinator import AgentCoordinator

coord = AgentCoordinator()
result = coord.coordinate_agent(
    agent_name="architect",
    task="设计用户认证系统",
    context={"requirements": [...]}
)
```

## MCP 集成

### Serena 使用
```python
# 查找符号
from src.mcp.gateway import get_mcp_gateway

gateway = get_mcp_gateway()
if gateway.is_available("serena"):
    tool = gateway.get_tool("serena", "find_symbol")
    result = tool.call(name="MyClass")
```

### AIRIS MCP Gateway
```python
# 三步工作流
# 1. 发现工具
tools = await airis-find({query: "tavily"})

# 2. 查看参数
schema = await airis-schema({tool: "tavily:search"})

# 3. 执行工具
result = await airis-exec({
    tool: "tavily:search",
    arguments: {query: "...", max_results: 5}
})
```

## 快捷命令

```bash
# 快速查看项目结构
ls -la

# 快速查找文档
find . -name "*.md" | grep -v archive

# 快速搜索关键词
grep -r "keyword" --include="*.md" . | head -20

# 快速查看 Git 状态
git status && git log --oneline -5
```