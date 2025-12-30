# 代码风格和约定 (Code Style & Conventions)

## Python 代码风格

### 基本原则
- 遵循 PEP 8 标准
- 使用 type hints (Python 3.8+ 语法)
- 添加 docstrings 到所有公共函数和类

### 命名约定
- 类名: PascalCase (DocLoader, AgentCoordinator)
- 函数/方法: snake_case (load_summary, get_mcp_gateway)
- 常量: UPPER_SNAKE_CASE
- 私有属性: _leading_underscore

### 文档字符串
```python
def function_name(param1: str, param2: int) -> dict:
    """
    简要说明函数功能。
    
    Args:
        param1: 参数 1 说明
        param2: 参数 2 说明
    
    Returns:
        返回值说明
    """
    pass
```

### 文件结构
```python
#!/usr/bin/env python3
"""
模块级文档字符串
"""

# 导入顺序：标准库 → 第三方库 → 本地模块
import os
import sys

from typing import List, Dict

from .local_module import something

# 常量定义
DEFAULT_TIMEOUT = 30

# 类定义
class ClassName:
    pass

# 函数定义
def function_name():
    pass
```

## Bash 脚本风格

### 基本原则
- 使用 `set -e` (遇到错误立即退出)
- 添加注释说明复杂逻辑
- 使用颜色输出提升可读性

### 标准模板
```bash
#!/bin/bash
set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

# 函数定义
function print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

function print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# 帮助信息
if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0 [options]"
    exit 0
fi

# 主逻辑
```

## Markdown 文档风格

### Frontmatter (必需)
```markdown
---
title: "文档标题"
description: "一句话描述"
type: "技术设计 | 架构决策 | 最佳实践"
status: "草稿 | 完成"
priority: "高 | 中 | 低"
created_date: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
related_documents: []
related_code: []
---
```

### 标题层级
- # (H1): 文档主标题（每个文件只有一个）
- ## (H2): 主要章节
- ### (H3): 子章节
- #### (H4): 细分内容

### 链接格式
- 使用相对路径: `[text](../path/to/file.md)`
- 不使用绝对路径

### 代码块
\`\`\`python
# 指定语言
code here
\`\`\`

## Git 提交规范

### 提交信息格式
```
[type] 简短描述 (不超过 50 字)

详细描述（可选）：
- 变更点 1
- 变更点 2

相关问题: #123
```

### Type 类型
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关
- `release`: 版本发布

## 文件组织

### 目录命名
- 使用小写和短横线: `best-practices/`, `mcp-integration/`
- 避免空格和特殊字符

### 文件命名
- Markdown: 小写和短横线 `document-architecture.md`
- Python: 小写和下划线 `doc_loader.py`
- Bash: 小写和下划线 `install_knowledge_base.sh`

## 最佳实践

1. **代码注释**: 使用英文
2. **文档内容**: 使用中文
3. **函数长度**: 单个函数 < 50 行
4. **文件长度**: Python 模块 < 500 行，文档 < 500 行
5. **错误处理**: 总是包含 try-except 块
6. **日志输出**: 使用清晰的级别 (INFO, WARNING, ERROR)