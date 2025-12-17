#!/usr/bin/env python3
"""
修复 Step 0.1 Agent 激活代码中的 ModuleNotFoundError

问题：在安装目录（~/.claude/commands/）外执行命令时，
     `from commands.lib.agent_coordinator import ...` 导入失败

解决：在 python -c 代码开头添加 sys.path 注入逻辑
"""

import re
from pathlib import Path

# 需要修复的命令文件列表
COMMANDS = [
    "wf_02_task.md",
    "wf_04_ask.md",
    "wf_05_code.md",
    "wf_06_debug.md",
    "wf_07_test.md",
    "wf_08_review.md",
    "wf_09_refactor.md",
]

# 修复模板：添加到 python -c 开头的代码
PATH_INJECTION = """import sys
import os

# 动态添加安装目录到 Python 路径（支持在任意目录执行命令）
install_dir = os.path.expanduser('~/.claude/commands')
if install_dir not in sys.path and os.path.exists(install_dir):
    sys.path.insert(0, install_dir)

"""


def fix_step_0_1(file_path: Path) -> bool:
    """修复单个命令文件的 Step 0.1 代码"""

    content = file_path.read_text(encoding='utf-8')

    # 正则匹配 Step 0.1 中的 python -c 代码块
    # 格式：```bash\npython -c "\n<code>\n"\n```
    pattern = re.compile(
        r'(```bash\npython -c "\n)'  # 开头
        r'(from commands\.lib\.agent_coordinator.*?)'  # 现有代码（不含 sys.path 注入）
        r'("\n```)',  # 结尾
        re.DOTALL
    )

    # 检查是否已经修复过（避免重复注入）
    if 'sys.path.insert(0, install_dir)' in content:
        print(f"  ⏭️  {file_path.name} - 已修复，跳过")
        return False

    # 替换：在 from commands 之前注入 sys.path 代码
    def replacer(match):
        return match.group(1) + PATH_INJECTION + match.group(2) + match.group(3)

    new_content, count = pattern.subn(replacer, content)

    if count == 0:
        print(f"  ⚠️  {file_path.name} - 未找到匹配的代码块")
        return False

    # 写回文件
    file_path.write_text(new_content, encoding='utf-8')
    print(f"  ✅ {file_path.name} - 修复成功（替换 {count} 处）")
    return True


def main():
    """批量修复所有命令文件"""

    # 获取源码目录（脚本位于 scripts/ 子目录）
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    print(f"📂 源码目录: {repo_root}")
    print(f"\n🔧 开始修复 {len(COMMANDS)} 个命令文件的 Step 0.1...\n")

    fixed_count = 0

    for cmd_file in COMMANDS:
        file_path = repo_root / cmd_file

        if not file_path.exists():
            print(f"  ❌ {cmd_file} - 文件不存在")
            continue

        if fix_step_0_1(file_path):
            fixed_count += 1

    print(f"\n{'='*70}")
    print(f"✅ 修复完成：{fixed_count}/{len(COMMANDS)} 个文件已更新")
    print(f"{'='*70}")
    print("\n📌 下一步：")
    print("  1. 用户手动同步到安装目录：rsync 或 cp")
    print("  2. 验证修复：在任意项目目录执行命令测试")


if __name__ == "__main__":
    main()
