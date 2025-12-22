#!/bin/bash

# ============================================
# 文档大小检查脚本
# ============================================
# 版本: v1.0
# 创建日期: 2025-12-21
# 用途: 检查文档行数是否超过限制，发出警告和存档建议
#
# 使用方法:
#   ./scripts/check_doc_size.sh                    # 检查所有文档
#   ./scripts/check_doc_size.sh docs/management/TASK.md  # 检查指定文档
#
# 退出码:
#   0 - 所有文档都在限制内
#   1 - 有文档超过限制

set -euo pipefail

# ============================================
# 配置和全局变量
# ============================================

# 脚本目录和项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 配置文件路径（支持两个位置）
CONFIG_FILE_LOCAL="$PROJECT_ROOT/doc_limits.yaml"
CONFIG_FILE_GLOBAL="$HOME/.claude/commands/doc_limits.yaml"

# 选择可用的配置文件
if [ -f "$CONFIG_FILE_LOCAL" ]; then
    CONFIG_FILE="$CONFIG_FILE_LOCAL"
elif [ -f "$CONFIG_FILE_GLOBAL" ]; then
    CONFIG_FILE="$CONFIG_FILE_GLOBAL"
else
    echo "❌ 错误: 找不到配置文件"
    echo "   预期位置:"
    echo "     - $CONFIG_FILE_LOCAL"
    echo "     - $CONFIG_FILE_GLOBAL"
    exit 1
fi

# 颜色定义
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# 统计变量
TOTAL_CHECKED=0
WARNINGS=0
VIOLATIONS=0

# ============================================
# 辅助函数
# ============================================

# 简单的 YAML 解析函数（仅支持我们需要的格式）
parse_yaml_value() {
    local file=$1
    local key=$2

    # 提取键值对（支持带引号和不带引号的值）
    grep "^  \"$key\":" "$file" 2>/dev/null | sed 's/^  "[^"]*": *//;s/"//g' || echo ""
}

parse_yaml_nested() {
    local file=$1
    local section=$2
    local key=$3

    # 提取嵌套配置（简化版）
    awk "/$section:/{flag=1; next} /^[a-z_]+:/{flag=0} flag && /$key:/{print; exit}" "$file" | sed 's/.*: *//'
}

# 获取文件行数
get_line_count() {
    local file=$1

    if [ ! -f "$file" ]; then
        echo "0"
        return
    fi

    wc -l < "$file" 2>/dev/null || echo "0"
}

# 计算百分比
calculate_percentage() {
    local current=$1
    local limit=$2

    if [ "$limit" -eq 0 ]; then
        echo "0"
        return
    fi

    # 使用 bc 或 awk 计算百分比
    if command -v bc >/dev/null 2>&1; then
        echo "scale=1; $current * 100 / $limit" | bc
    else
        awk -v curr="$current" -v lim="$limit" 'BEGIN {printf "%.1f", curr * 100 / lim}'
    fi
}

# 获取文件基本名（不带路径和扩展名）
get_basename() {
    local file=$1
    basename "$file" .md
}

# ============================================
# 核心检查函数
# ============================================

check_document() {
    local doc_path=$1
    local limit=$2

    # 转换为绝对路径
    local abs_path="$PROJECT_ROOT/$doc_path"

    # 检查文件是否存在
    if [ ! -f "$abs_path" ]; then
        echo -e "${YELLOW}⚠️  $doc_path 不存在，跳过检查${NC}"
        return 0
    fi

    # 获取当前行数
    local current_lines
    current_lines=$(get_line_count "$abs_path")

    # 计算百分比
    local percentage
    percentage=$(calculate_percentage "$current_lines" "$limit")

    # 计算阈值
    local warning_threshold
    warning_threshold=$(parse_yaml_nested "$CONFIG_FILE" "archive_triggers" "warning_threshold")
    warning_threshold=${warning_threshold:-0.7}

    local auto_threshold
    auto_threshold=$(parse_yaml_nested "$CONFIG_FILE" "archive_triggers" "auto_threshold")
    auto_threshold=${auto_threshold:-0.8}

    # 计算警告和自动触发行数
    local warning_lines
    warning_lines=$(awk -v lim="$limit" -v thresh="$warning_threshold" 'BEGIN {printf "%.0f", lim * thresh}')

    local auto_lines
    auto_lines=$(awk -v lim="$limit" -v thresh="$auto_threshold" 'BEGIN {printf "%.0f", lim * thresh}')

    TOTAL_CHECKED=$((TOTAL_CHECKED + 1))

    # 判断状态
    if [ "$current_lines" -gt "$limit" ]; then
        # 超过限制
        echo -e "${RED}🔴 $doc_path 超过限制 ($current_lines/$limit 行, ${percentage}%)${NC}"
        echo -e "   ${RED}建议: 立即运行 /wf_13_doc_maintain archive $(get_basename "$doc_path")${NC}"
        VIOLATIONS=$((VIOLATIONS + 1))
        return 1

    elif [ "$current_lines" -gt "$auto_lines" ]; then
        # 超过 80% 阈值
        echo -e "${RED}⚠️  $doc_path 接近限制 ($current_lines/$limit 行, ${percentage}%)${NC}"
        echo -e "   ${RED}建议: 运行 /wf_13_doc_maintain archive $(get_basename "$doc_path")${NC}"
        WARNINGS=$((WARNINGS + 1))
        return 1

    elif [ "$current_lines" -gt "$warning_lines" ]; then
        # 超过 70% 阈值
        echo -e "${YELLOW}⚡ $doc_path 需要注意 ($current_lines/$limit 行, ${percentage}%)${NC}"
        echo -e "   ${YELLOW}提示: 接近警告阈值，可以开始规划存档${NC}"
        WARNINGS=$((WARNINGS + 1))

    else
        # 正常范围
        echo -e "${GREEN}✅ $doc_path 正常 ($current_lines/$limit 行, ${percentage}%)${NC}"
    fi

    return 0
}

# ============================================
# 主函数
# ============================================

main() {
    echo "======================================"
    echo "📏 文档大小检查工具"
    echo "======================================"
    echo ""
    echo "配置文件: $CONFIG_FILE"
    echo "项目根目录: $PROJECT_ROOT"
    echo ""

    # 检查配置文件是否可读
    if [ ! -r "$CONFIG_FILE" ]; then
        echo -e "${RED}❌ 错误: 无法读取配置文件: $CONFIG_FILE${NC}"
        exit 1
    fi

    # 如果提供了参数，只检查指定文档
    if [ $# -gt 0 ]; then
        local doc_file=$1
        local limit
        limit=$(parse_yaml_value "$CONFIG_FILE" "$doc_file")

        if [ -z "$limit" ]; then
            echo -e "${RED}❌ 错误: 配置文件中未找到 $doc_file 的限制定义${NC}"
            exit 1
        fi

        echo "检查文档: $doc_file (限制: $limit 行)"
        echo "--------------------------------------"
        check_document "$doc_file" "$limit"

    else
        # 检查所有配置的文档
        echo "检查所有配置的文档..."
        echo "--------------------------------------"
        echo ""

        # 读取配置文件中的所有文档限制
        while IFS= read -r line; do
            # 跳过注释和空行
            [[ "$line" =~ ^[[:space:]]*# ]] && continue
            [[ -z "$line" ]] && continue

            # 提取文档路径和限制
            if [[ "$line" =~ ^[[:space:]]+\"([^\"]+)\":[[:space:]]*([0-9]+) ]]; then
                local doc_path="${BASH_REMATCH[1]}"
                local limit="${BASH_REMATCH[2]}"

                check_document "$doc_path" "$limit" || true
                echo ""
            fi
        done < <(sed -n '/^document_limits:/,/^[a-z]/p' "$CONFIG_FILE")
    fi

    # 输出统计结果
    echo "======================================"
    echo "📊 检查统计"
    echo "======================================"
    echo "总检查文档数: $TOTAL_CHECKED"
    echo "警告数量: $WARNINGS"
    echo "超限数量: $VIOLATIONS"
    echo ""

    if [ "$VIOLATIONS" -gt 0 ]; then
        echo -e "${RED}❌ 检查失败: 有 $VIOLATIONS 个文档超过限制${NC}"
        exit 1
    elif [ "$WARNINGS" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  警告: 有 $WARNINGS 个文档接近限制${NC}"
        exit 0
    else
        echo -e "${GREEN}✅ 所有文档都在限制范围内${NC}"
        exit 0
    fi
}

# 运行主函数
main "$@"
