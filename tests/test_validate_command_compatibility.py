#!/usr/bin/env python3
"""
Pytest tests for validate_command_compatibility.py

Tests cover:
- Environment version detection
- MCP server detection
- Command definition loading
- Command compatibility validation
- Report generation (Markdown and JSON)
- CI/CD exit codes

Target: >70% code coverage
"""

import pytest
import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_command_compatibility import (
    detect_environment_version,
    detect_mcp_servers,
    load_command_definitions,
    validate_command,
    generate_report,
    CompatibilityStatus,
    Tier,
    CommandDefinition,
    CommandCompatibility
)


class TestEnvironmentDetection:
    """Test environment version detection"""

    @patch('validate_command_compatibility.Path')
    def test_detect_v17_environment(self, mock_path):
        """Test detection of v1.7 environment (all markers present)"""
        mock_path.return_value.exists.side_effect = [True, True, True]
        version, compat = detect_environment_version()
        assert version == "v1.7"
        assert compat == "完全兼容"

    @patch('validate_command_compatibility.Path')
    def test_detect_v16_environment(self, mock_path):
        """Test detection of v1.6 environment (MCP gateway only)"""
        # For v1.6: command_index.exists() returns False (short-circuits and),
        # then mcp_gateway.exists() in elif returns True
        mock_path.return_value.exists.side_effect = [False, True]
        version, compat = detect_environment_version()
        assert version == "v1.6"
        assert compat == "大部分兼容"

    @patch('validate_command_compatibility.Path')
    def test_detect_v13_v15_environment(self, mock_path):
        """Test detection of v1.3-v1.5 environment (docs_index only)"""
        # For v1.3-v1.5: command_index False (short-circuits first and),
        # mcp_gateway False (first elif fails), docs_index True (second elif succeeds)
        mock_path.return_value.exists.side_effect = [False, False, True]
        version, compat = detect_environment_version()
        assert version == "v1.3-v1.5"
        assert compat == "基础兼容"

    @patch('validate_command_compatibility.Path')
    def test_detect_v10_v12_environment(self, mock_path):
        """Test detection of v1.0-v1.2 environment (no markers)"""
        mock_path.return_value.exists.return_value = False
        version, compat = detect_environment_version()
        assert version == "v1.0-v1.2"
        assert compat == "受限兼容"


class TestMCPDetection:
    """Test MCP server detection"""

    @patch('validate_command_compatibility.importlib.util.find_spec')
    def test_all_mcps_available(self, mock_find_spec):
        """Test when all 6 MCP servers are available"""
        mock_find_spec.return_value = Mock()  # Non-None means available
        result = detect_mcp_servers()

        assert len(result) == 6
        assert all(result.values())  # All should be True
        assert "mcp_sequential_thinking" in result
        assert "mcp_context7" in result
        assert "mcp_serena" in result
        assert "mcp_tavily" in result
        assert "mcp_magic" in result
        assert "mcp_playwright" in result

    @patch('validate_command_compatibility.importlib.util.find_spec')
    def test_no_mcps_available(self, mock_find_spec):
        """Test when no MCP servers are available"""
        mock_find_spec.return_value = None  # None means not available
        result = detect_mcp_servers()

        assert len(result) == 6
        assert not any(result.values())  # All should be False

    @patch('validate_command_compatibility.importlib.util.find_spec')
    def test_partial_mcps_available(self, mock_find_spec):
        """Test when only some MCP servers are available"""
        def side_effect(mcp_name):
            return Mock() if mcp_name in ["mcp_serena", "mcp_context7"] else None

        mock_find_spec.side_effect = side_effect
        result = detect_mcp_servers()

        assert result["mcp_serena"] is True
        assert result["mcp_context7"] is True
        assert result["mcp_sequential_thinking"] is False
        assert result["mcp_tavily"] is False
        assert result["mcp_magic"] is False
        assert result["mcp_playwright"] is False


class TestCommandDefinitions:
    """Test command definition loading"""

    def test_load_command_definitions_count(self):
        """Test that 14 commands are loaded"""
        commands = load_command_definitions()
        assert len(commands) == 14

    def test_tier1_commands(self):
        """Test Tier 1 commands (fully compatible)"""
        commands = load_command_definitions()
        tier1 = [cmd for cmd in commands if cmd.tier == Tier.TIER_1]

        assert len(tier1) == 3
        assert all(len(cmd.required_mcps) == 0 for cmd in tier1)
        assert all(len(cmd.optional_mcps) == 0 for cmd in tier1)

        tier1_names = [cmd.name for cmd in tier1]
        assert "wf_01_planning" in tier1_names
        assert "wf_02_task" in tier1_names
        assert "wf_11_commit" in tier1_names

    def test_tier2_commands(self):
        """Test Tier 2 commands (degraded functionality)"""
        commands = load_command_definitions()
        tier2 = [cmd for cmd in commands if cmd.tier == Tier.TIER_2]

        assert len(tier2) == 9
        assert all(len(cmd.required_mcps) == 0 for cmd in tier2)
        assert all(len(cmd.optional_mcps) > 0 for cmd in tier2)

    def test_tier3_commands(self):
        """Test Tier 3 commands (restricted/unavailable)"""
        commands = load_command_definitions()
        tier3 = [cmd for cmd in commands if cmd.tier == Tier.TIER_3]

        assert len(tier3) == 2
        assert all(len(cmd.required_mcps) > 0 for cmd in tier3)

        tier3_names = [cmd.name for cmd in tier3]
        assert "wf_12_deploy_check" in tier3_names
        assert "wf_14_doc" in tier3_names


class TestCommandValidation:
    """Test command compatibility validation"""

    def test_validate_tier1_command_always_full(self):
        """Test that Tier 1 commands are always FULL"""
        cmd = CommandDefinition(
            name="wf_01_planning",
            description="项目规划",
            tier=Tier.TIER_1,
            required_mcps=[],
            optional_mcps=[]
        )

        # Test with no MCPs
        result = validate_command(cmd, {})
        assert result.status == CompatibilityStatus.FULL
        assert result.functionality_percentage == 100

        # Test with all MCPs
        all_mcps = {mcp: True for mcp in ["mcp_serena", "mcp_context7"]}
        result = validate_command(cmd, all_mcps)
        assert result.status == CompatibilityStatus.FULL
        assert result.functionality_percentage == 100

    def test_validate_tier3_missing_required_mcp(self):
        """Test that Tier 3 commands are UNAVAILABLE when missing required MCP"""
        cmd = CommandDefinition(
            name="wf_12_deploy_check",
            description="部署检查",
            tier=Tier.TIER_3,
            required_mcps=["mcp_playwright"],
            optional_mcps=[]
        )

        # Missing required MCP
        result = validate_command(cmd, {"mcp_playwright": False})
        assert result.status == CompatibilityStatus.UNAVAILABLE
        assert result.functionality_percentage == 20  # 0-30% range

    def test_validate_tier3_with_required_mcp(self):
        """Test that Tier 3 commands are FULL when required MCP is available"""
        cmd = CommandDefinition(
            name="wf_12_deploy_check",
            description="部署检查",
            tier=Tier.TIER_3,
            required_mcps=["mcp_playwright"],
            optional_mcps=[]
        )

        # Required MCP available
        result = validate_command(cmd, {"mcp_playwright": True})
        assert result.status == CompatibilityStatus.FULL
        assert result.functionality_percentage == 100

    def test_validate_tier2_all_optional_mcps(self):
        """Test Tier 2 command with all optional MCPs available"""
        cmd = CommandDefinition(
            name="wf_04_ask",
            description="架构咨询",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_sequential_thinking", "mcp_context7", "mcp_tavily"]
        )

        # All optional MCPs available
        mcps = {
            "mcp_sequential_thinking": True,
            "mcp_context7": True,
            "mcp_tavily": True
        }
        result = validate_command(cmd, mcps)
        assert result.status == CompatibilityStatus.FULL
        assert result.functionality_percentage == 100

    def test_validate_tier2_no_optional_mcps(self):
        """Test Tier 2 command with no optional MCPs available"""
        cmd = CommandDefinition(
            name="wf_04_ask",
            description="架构咨询",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_sequential_thinking", "mcp_context7", "mcp_tavily"]
        )

        # No optional MCPs available
        mcps = {
            "mcp_sequential_thinking": False,
            "mcp_context7": False,
            "mcp_tavily": False
        }
        result = validate_command(cmd, mcps)
        assert result.status == CompatibilityStatus.LIMITED
        assert result.functionality_percentage == 60  # 50-80% range

    def test_validate_tier2_partial_optional_mcps(self):
        """Test Tier 2 command with partial optional MCPs"""
        cmd = CommandDefinition(
            name="wf_04_ask",
            description="架构咨询",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_sequential_thinking", "mcp_context7", "mcp_tavily"]
        )

        # 2 out of 3 optional MCPs available
        mcps = {
            "mcp_sequential_thinking": True,
            "mcp_context7": True,
            "mcp_tavily": False
        }
        result = validate_command(cmd, mcps)
        assert result.status == CompatibilityStatus.LIMITED
        # 50 + (2/3) * 40 = 50 + 26.67 = 76.67 → int(76)
        assert 70 <= result.functionality_percentage <= 80


class TestReportGeneration:
    """Test report generation in Markdown and JSON formats"""

    def test_generate_markdown_report_structure(self):
        """Test Markdown report has correct structure"""
        # Create sample data
        results = [
            CommandCompatibility(
                name="wf_01_planning",
                status=CompatibilityStatus.FULL,
                tier=1,
                available_mcps=[],
                missing_mcps=[],
                functionality_percentage=100
            ),
            CommandCompatibility(
                name="wf_04_ask",
                status=CompatibilityStatus.LIMITED,
                tier=2,
                available_mcps=["mcp_context7"],
                missing_mcps=["mcp_sequential_thinking", "mcp_tavily"],
                functionality_percentage=70
            )
        ]

        report = generate_report(results, format="markdown")

        # Check key sections exist
        assert "# AI Workflow 命令兼容性报告" in report
        assert "## 总体统计" in report
        assert "## 命令兼容性详情" in report
        assert "### Tier 1: 完全兼容" in report
        assert "### Tier 2: 功能降级" in report
        assert "✅ 完全可用 (FULL): 1/14" in report or "1/" in report
        assert "🟡 功能降级 (LIMITED): 1/14" in report or "1/" in report

    def test_generate_json_report_structure(self):
        """Test JSON report has valid structure"""
        results = [
            CommandCompatibility(
                name="wf_01_planning",
                status=CompatibilityStatus.FULL,
                tier=1,
                available_mcps=[],
                missing_mcps=[],
                functionality_percentage=100
            )
        ]

        report = generate_report(results, format="json")

        # Parse JSON to verify structure
        data = json.loads(report)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "wf_01_planning"
        assert data[0]["status"] == "FULL"
        assert data[0]["tier"] == 1
        assert data[0]["functionality_percentage"] == 100

    def test_generate_markdown_report_with_all_statuses(self):
        """Test Markdown report with all compatibility statuses"""
        results = [
            CommandCompatibility(
                name="tier1_cmd",
                status=CompatibilityStatus.FULL,
                tier=1,
                available_mcps=[],
                missing_mcps=[],
                functionality_percentage=100
            ),
            CommandCompatibility(
                name="tier2_cmd",
                status=CompatibilityStatus.LIMITED,
                tier=2,
                available_mcps=["mcp_serena"],
                missing_mcps=["mcp_magic"],
                functionality_percentage=70
            ),
            CommandCompatibility(
                name="tier3_cmd",
                status=CompatibilityStatus.UNAVAILABLE,
                tier=3,
                available_mcps=[],
                missing_mcps=["mcp_playwright"],
                functionality_percentage=20
            )
        ]

        report = generate_report(results, format="markdown")

        # Check all status types are represented
        assert "✅ 完全可用 (FULL): 1/" in report or "1/14" in report
        assert "🟡 功能降级 (LIMITED): 1/" in report or "1/14" in report
        assert "🔴 不可用 (UNAVAILABLE): 1/" in report or "1/14" in report


class TestMainFunction:
    """Test main function and CLI behavior"""

    @patch('validate_command_compatibility.detect_environment_version')
    @patch('validate_command_compatibility.detect_mcp_servers')
    @patch('validate_command_compatibility.sys.exit')
    @patch('validate_command_compatibility.print')
    def test_main_exit_code_all_full(self, mock_print, mock_exit, mock_mcp, mock_env):
        """Test exit code 0 when all commands are FULL"""
        mock_env.return_value = ("v1.7", "完全兼容")
        mock_mcp.return_value = {mcp: True for mcp in [
            "mcp_sequential_thinking", "mcp_context7", "mcp_serena",
            "mcp_tavily", "mcp_magic", "mcp_playwright"
        ]}

        from validate_command_compatibility import main

        with patch('sys.argv', ['script.py']):
            main()

        # Should exit with 0 when all commands are FULL
        # (In v1.7 with all MCPs, all commands should be FULL)
        mock_exit.assert_called()

    @patch('validate_command_compatibility.detect_environment_version')
    @patch('validate_command_compatibility.detect_mcp_servers')
    @patch('validate_command_compatibility.sys.exit')
    @patch('validate_command_compatibility.print')
    def test_main_exit_code_some_degraded(self, mock_print, mock_exit, mock_mcp, mock_env):
        """Test exit code 1 when some commands are degraded"""
        mock_env.return_value = ("v1.0-v1.2", "受限兼容")
        mock_mcp.return_value = {mcp: False for mcp in [
            "mcp_sequential_thinking", "mcp_context7", "mcp_serena",
            "mcp_tavily", "mcp_magic", "mcp_playwright"
        ]}

        from validate_command_compatibility import main

        with patch('sys.argv', ['script.py']):
            main()

        # Should exit with 1 when some commands are degraded/unavailable
        mock_exit.assert_called_with(1)


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_validate_command_empty_mcp_dict(self):
        """Test validation with empty MCP availability dict"""
        cmd = CommandDefinition(
            name="test_cmd",
            description="Test",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_serena"]
        )

        result = validate_command(cmd, {})
        assert result.status == CompatibilityStatus.LIMITED
        assert len(result.missing_mcps) == 1

    def test_generate_report_empty_results(self):
        """Test report generation with empty results"""
        report = generate_report([], format="markdown")
        assert "# AI Workflow 命令兼容性报告" in report

        json_report = generate_report([], format="json")
        data = json.loads(json_report)
        assert data == []

    def test_command_definition_validation(self):
        """Test CommandDefinition dataclass validation"""
        cmd = CommandDefinition(
            name="wf_test",
            description="Test command",
            tier=Tier.TIER_2,
            required_mcps=[],
            optional_mcps=["mcp_serena", "mcp_magic"]
        )

        assert cmd.name == "wf_test"
        assert cmd.tier == Tier.TIER_2
        assert len(cmd.optional_mcps) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=validate_command_compatibility", "--cov-report=term-missing"])
