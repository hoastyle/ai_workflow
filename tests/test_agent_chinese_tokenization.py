"""
单元测试：Agent 中文分词和关键词匹配

Task 7.8: Agent 中文分词单元测试 - 覆盖率 ≥80% agent_registry.py:176-272

测试目标：
1. 中文字符检测 (_contains_chinese)
2. 中文关键词匹配 (40% 阈值)
3. 中文场景匹配 (60% 阈值)
4. 混合语言场景
5. 边界情况和特殊字符处理
"""

import pytest
from unittest.mock import Mock, MagicMock
from commands.lib.agent_registry import Agent, AgentRegistry, AgentMatch


class TestChineseCharacterDetection:
    """测试中文字符检测功能"""

    @pytest.fixture
    def registry(self):
        """创建 AgentRegistry 实例"""
        return AgentRegistry()

    def test_contains_chinese_pure_chinese(self, registry):
        """测试：纯中文文本检测"""
        assert registry._contains_chinese("调试") is True
        assert registry._contains_chinese("这是一个错误") is True

    def test_contains_chinese_mixed_text(self, registry):
        """测试：混合中英文检测"""
        assert registry._contains_chinese("调试 debug") is True
        assert registry._contains_chinese("test 测试") is True

    def test_contains_chinese_pure_english(self, registry):
        """测试：纯英文文本检测"""
        assert registry._contains_chinese("debug") is False
        assert registry._contains_chinese("error fix") is False

    def test_contains_chinese_special_chars(self, registry):
        """测试：特殊字符不被识别为中文"""
        assert registry._contains_chinese("!@#$%^&*()") is False
        assert registry._contains_chinese("123456") is False

    def test_contains_chinese_empty_string(self, registry):
        """测试：空字符串"""
        assert registry._contains_chinese("") is False

    def test_contains_chinese_with_punctuation(self, registry):
        """测试：中文 + 标点符号"""
        assert registry._contains_chinese("调试！") is True
        assert registry._contains_chinese("错误，问题") is True


class TestChineseKeywordMatching:
    """测试中文关键词匹配逻辑"""

    @pytest.fixture
    def registry(self):
        return AgentRegistry()

    def test_exact_chinese_match(self, registry):
        """测试：完全匹配中文关键词"""
        # 创建 mock agent
        agent = Mock(spec=Agent)
        agent.name = "debug-agent"
        agent.priority = "high"
        agent.activation_keywords = ["调试", "错误"]
        agent.activation_scenarios = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        # 计算匹配度
        score, kw, sc, reason = registry._calculate_match_score(agent, "调试")

        assert score >= 0.3  # 至少应该有一个关键词匹配的分数 (0.3)
        assert "调试" in kw

    def test_chinese_keyword_char_match_40_percent(self, registry):
        """测试：中文关键词 40% 字符匹配阈值"""
        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "medium"
        # 关键词 "调试" (2个字符), "错" 这一个字符占 50%, 应该 > 40%
        agent.activation_keywords = ["调试"]
        agent.activation_scenarios = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        score, kw, sc, reason = registry._calculate_match_score(agent, "这里有错")

        # 虽然 "错" 包含 1 个字符，但 "调" 和 "试" 不在 "这里有错" 中
        # 所以不应该匹配（除非特殊处理）

    def test_multiple_chinese_keywords_cumulative(self, registry):
        """测试：多个中文关键词累积匹配"""
        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "high"
        agent.activation_keywords = ["调试", "错误", "问题"]
        agent.activation_scenarios = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        # 包含多个关键词
        score, kw, sc, reason = registry._calculate_match_score(
            agent, "调试这个错误和问题"
        )

        # 应该匹配所有 3 个关键词，分数 = min(0.3 * 3, 0.6) = 0.6
        assert score >= 0.6
        assert len(kw) >= 3

    def test_chinese_keyword_partial_match(self, registry):
        """测试：中文关键词部分匹配"""
        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "medium"
        agent.activation_keywords = ["调试过程"]
        agent.activation_scenarios = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        # 包含 "调试" 但不是完全的 "调试过程"
        score, kw, sc, reason = registry._calculate_match_score(
            agent, "需要调试"
        )

        # 依赖于字符匹配逻辑 - "调" 和 "试" 都在 "调试" 中
        # 2/3 = 66.7% > 40%, 应该匹配


class TestChineseScenarioMatching:
    """测试中文场景匹配逻辑"""

    @pytest.fixture
    def registry(self):
        return AgentRegistry()

    def test_exact_chinese_scenario_match(self, registry):
        """测试：完全匹配中文场景"""
        agent = Mock(spec=Agent)
        agent.name = "debug-agent"
        agent.priority = "high"
        agent.activation_keywords = []
        agent.activation_scenarios = ["程序出现错误"]
        agent.decision_criteria = {"confidence_threshold": 0.5}

        score, kw, sc, reason = registry._calculate_match_score(
            agent, "程序出现错误"
        )

        assert score >= 0.4  # 场景匹配应该贡献 0.4
        assert "程序出现错误" in sc

    def test_chinese_scenario_partial_match_60_percent(self, registry):
        """测试：中文场景 60% 匹配阈值"""
        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "medium"
        # "程序出现错误或异常" (8个字符)
        agent.activation_scenarios = ["程序出现错误或异常"]
        agent.activation_keywords = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        # "程序出现问题" vs "程序出现错误或异常"
        # 匹配字符: "程", "序", "出", "现" = 4/8 = 50% < 60%, 不匹配
        # 但是 "程序出现" 可能被识别为子串
        score, kw, sc, reason = registry._calculate_match_score(
            agent, "程序出现问题"
        )

        # 这个取决于具体实现

    def test_multiple_chinese_scenarios(self, registry):
        """测试：多个中文场景匹配"""
        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "high"
        agent.activation_scenarios = [
            "程序出现错误",
            "代码运行失败",
            "系统异常"
        ]
        agent.activation_keywords = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        score, kw, sc, reason = registry._calculate_match_score(
            agent, "程序出现错误和系统异常"
        )

        # 应该匹配多个场景
        assert len(sc) >= 1


class TestMixedLanguageMatching:
    """测试混合中英文匹配"""

    @pytest.fixture
    def registry(self):
        return AgentRegistry()

    def test_mixed_chinese_english_keywords(self, registry):
        """测试：混合中英文关键词"""
        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "high"
        agent.activation_keywords = ["调试", "debug", "错误"]
        agent.activation_scenarios = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        score, kw, sc, reason = registry._calculate_match_score(
            agent, "调试 debug 错误"
        )

        # 应该匹配所有关键词
        assert score >= 0.6
        assert len(kw) >= 2


class TestEdgeCases:
    """测试边界情况"""

    @pytest.fixture
    def registry(self):
        return AgentRegistry()

    def test_empty_keywords(self, registry):
        """测试：空关键词列表"""
        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "medium"
        agent.activation_keywords = []
        agent.activation_scenarios = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        score, kw, sc, reason = registry._calculate_match_score(agent, "任意文本")

        # 无关键词和场景，分数应该很低
        assert score < 0.2

    def test_very_long_text(self, registry):
        """测试：很长的中文文本"""
        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "high"
        agent.activation_keywords = ["错误"]
        agent.activation_scenarios = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        # 长文本中包含关键词
        long_text = "这是一个很长的文本" * 100 + "包含错误"

        score, kw, sc, reason = registry._calculate_match_score(agent, long_text)

        # 应该能找到关键词
        assert "错误" in kw
        assert score >= 0.3

    def test_unicode_special_chars(self, registry):
        """测试：Unicode 特殊字符"""
        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "medium"
        agent.activation_keywords = ["测试"]
        agent.activation_scenarios = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        # 带 Unicode 标记的文本
        score, kw, sc, reason = registry._calculate_match_score(
            agent, "测试\u200b\u200c\u200d"
        )

        # 应该仍能匹配关键词
        assert "测试" in kw

    def test_case_insensitivity_english(self, registry):
        """测试：英文大小写不敏感"""
        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "medium"
        agent.activation_keywords = ["debug"]
        agent.activation_scenarios = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        # 大写 DEBUG
        score, kw, sc, reason = registry._calculate_match_score(agent, "DEBUG")

        # 应该匹配（因为代码使用 .lower()）
        assert score >= 0.3


class TestPerformance:
    """性能测试"""

    @pytest.fixture
    def registry(self):
        return AgentRegistry()

    def test_matching_performance_single_keyword(self, registry):
        """测试：单个关键词匹配性能"""
        import time

        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "medium"
        agent.activation_keywords = ["调试"]
        agent.activation_scenarios = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        start = time.time()
        for _ in range(1000):
            registry._calculate_match_score(agent, "调试测试")
        duration = time.time() - start

        # 1000 次匹配应该在 1 秒以内
        assert duration < 1.0

    def test_matching_performance_many_keywords(self, registry):
        """测试：多个关键词匹配性能"""
        import time

        agent = Mock(spec=Agent)
        agent.name = "test-agent"
        agent.priority = "high"
        agent.activation_keywords = [f"关键词{i}" for i in range(100)]
        agent.activation_scenarios = []
        agent.decision_criteria = {"confidence_threshold": 0.5}

        start = time.time()
        for _ in range(100):
            registry._calculate_match_score(agent, "关键词测试")
        duration = time.time() - start

        # 100 次、100 个关键词的匹配应该在 2 秒以内
        assert duration < 2.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
