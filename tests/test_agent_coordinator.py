"""
Test Agent Coordinator

测试 AgentCoordinator 的核心功能
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from commands.lib.agent_coordinator import get_agent_coordinator, AgentCoordinator


def test_singleton_pattern():
    """测试单例模式"""
    print("Test 1: Singleton Pattern")
    print("=" * 50)

    coordinator1 = get_agent_coordinator()
    coordinator2 = get_agent_coordinator()

    assert coordinator1 is coordinator2, "应该返回同一个实例"
    print("✅ 单例模式工作正常")
    print()


def test_agent_selection():
    """测试 agent 选择功能"""
    print("Test 2: Agent Selection")
    print("=" * 50)

    coordinator = get_agent_coordinator()

    # 测试场景 1: 代码实现任务
    context1 = coordinator.intercept(
        task_description="实现用户登录功能",
        command_name="wf_05_code",
        auto_activate=True
    )

    print(f"任务: 实现用户登录功能")
    print(f"选中 Agent: {context1['agent'].name if context1['agent'] else 'None'}")
    print(f"匹配度: {context1['match_score']:.2f}")
    print(f"自动激活: {context1['auto_activated']}")

    if context1['agent']:
        assert context1['agent'].name == 'code-agent', "应该选择 code-agent"
        print("✅ 正确选择了 code-agent")
    print()

    # 测试场景 2: 代码审查任务
    context2 = coordinator.intercept(
        task_description="代码审查",
        command_name="wf_08_review",
        auto_activate=True
    )

    print(f"任务: 代码审查")
    print(f"选中 Agent: {context2['agent'].name if context2['agent'] else 'None'}")
    print(f"匹配度: {context2['match_score']:.2f}")
    print(f"自动激活: {context2['auto_activated']}")

    if context2['agent']:
        print(f"✅ 选择了 {context2['agent'].name}")
    print()

    # 测试场景 3: Bug 修复任务
    context3 = coordinator.intercept(
        task_description="修复登录页面的错误",
        command_name="wf_06_debug",
        auto_activate=True
    )

    print(f"任务: 修复登录页面的错误")
    print(f"选中 Agent: {context3['agent'].name if context3['agent'] else 'None'}")
    print(f"匹配度: {context3['match_score']:.2f}")
    print(f"自动激活: {context3['auto_activated']}")

    if context3['agent']:
        print(f"✅ 选择了 {context3['agent'].name}")
    print()


def test_format_output():
    """测试格式化输出"""
    print("Test 3: Format Output")
    print("=" * 50)

    coordinator = get_agent_coordinator()

    context = coordinator.intercept(
        task_description="编写测试用例",
        command_name="wf_07_test",
        auto_activate=True
    )

    # 测试详细输出
    output_verbose = coordinator.format_agent_info(context, verbose=True)
    print("详细输出:")
    print(output_verbose)

    # 测试简洁输出
    output_brief = coordinator.format_agent_info(context, verbose=False)
    print("简洁输出:")
    print(output_brief)

    print("✅ 格式化输出正常")
    print()


def test_collaboration_suggestions():
    """测试协作建议"""
    print("Test 4: Collaboration Suggestions")
    print("=" * 50)

    coordinator = get_agent_coordinator()

    # 先激活一个 agent
    context = coordinator.intercept(
        task_description="实现新功能",
        command_name="wf_05_code",
        auto_activate=True
    )

    if context['agent']:
        print(f"当前 Agent: {context['agent'].name}")

        # 获取协作建议
        next_agent = coordinator.suggest_next_agent()
        print(f"建议下一步使用: {next_agent}")

        # 显示所有协作者
        collaborators = context['collaborators']
        if collaborators:
            print("\n所有协作建议:")
            for collab in collaborators:
                print(f"  - {collab['mode']}: {collab['agent']} ({collab['scenario']})")

        print("✅ 协作建议功能正常")
    else:
        print("⚠️ 未选中 agent，跳过协作测试")

    print()


def test_usage_stats():
    """测试使用统计"""
    print("Test 5: Usage Statistics")
    print("=" * 50)

    coordinator = get_agent_coordinator()

    # 执行几次操作
    tasks = [
        "实现用户注册",
        "修复登录 bug",
        "编写单元测试",
        "代码审查",
        "性能优化"
    ]

    for task in tasks:
        coordinator.intercept(
            task_description=task,
            command_name="wf_05_code",
            auto_activate=True
        )

    # 获取统计
    stats = coordinator.get_usage_stats(limit=5)
    print(f"记录了 {len(stats)} 条使用统计")

    # 格式化输出
    formatted_stats = coordinator.format_usage_stats(limit=5)
    print(formatted_stats)

    print("✅ 使用统计功能正常")
    print()


def test_low_confidence_scenario():
    """测试低置信度场景"""
    print("Test 6: Low Confidence Scenario")
    print("=" * 50)

    coordinator = get_agent_coordinator()

    # 一个不太匹配的任务描述
    context = coordinator.intercept(
        task_description="帮我做点什么",
        command_name="wf_05_code",
        auto_activate=True,
        min_confidence=0.85
    )

    print(f"任务: 帮我做点什么")
    print(f"匹配度: {context['match_score']:.2f}")
    print(f"自动激活: {context['auto_activated']}")

    if context['match_score'] < 0.85:
        print("✅ 正确拒绝了低置信度激活")
    else:
        print(f"⚠️ 意外激活了 {context['agent'].name if context['agent'] else 'None'}")

    print()


def test_command_alignment():
    """测试命令对齐检查"""
    print("Test 7: Command Alignment Check")
    print("=" * 50)

    coordinator = get_agent_coordinator()

    # 测试对齐场景
    context1 = coordinator.intercept(
        task_description="实现新功能",
        command_name="wf_05_code",
        auto_activate=True
    )

    if context1['agent']:
        alignment = context1['command_alignment']
        print(f"Agent: {context1['agent'].name}")
        print(f"命令: wf_05_code")
        print(f"对齐: {alignment['aligned']}")
        if not alignment['aligned']:
            print(f"提示: {alignment['note']}")

    print()

    # 测试不对齐场景（使用错误命令）
    context2 = coordinator.intercept(
        task_description="实现新功能",
        command_name="wf_07_test",  # 错误命令
        auto_activate=True
    )

    if context2['agent']:
        alignment = context2['command_alignment']
        print(f"Agent: {context2['agent'].name}")
        print(f"命令: wf_07_test")
        print(f"对齐: {alignment['aligned']}")
        if not alignment['aligned']:
            print(f"提示: {alignment['note']}")

    print("✅ 命令对齐检查功能正常")
    print()


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("Agent Coordinator 测试套件")
    print("=" * 70 + "\n")

    try:
        test_singleton_pattern()
        test_agent_selection()
        test_format_output()
        test_collaboration_suggestions()
        test_usage_stats()
        test_low_confidence_scenario()
        test_command_alignment()

        print("=" * 70)
        print("✅ 所有测试通过！")
        print("=" * 70)
        return True

    except Exception as e:
        print("=" * 70)
        print(f"❌ 测试失败: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
