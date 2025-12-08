#!/usr/bin/env python3
"""
Pytest tests for optimize_context_loading.py

Tests cover:
- Prime loading analysis
- Docs index coverage analysis
- Optimization suggestions generation
- Token savings calculation
- Report generation (Markdown and JSON)
- CLI main function

Target: >70% code coverage
"""

import pytest
import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
from io import StringIO

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from optimize_context_loading import (
    analyze_prime_loading,
    analyze_docs_index,
    suggest_optimizations,
    calculate_token_savings,
    generate_report,
    OptimizationType,
    Priority,
    Optimization,
    LoadingAnalysis,
    IndexCoverage
)


class TestPrimeLoadingAnalysis:
    """Test wf_03_prime.md loading analysis"""

    @patch('optimize_context_loading.Path')
    def test_analyze_prime_loading_success(self, mock_path):
        """Test successful analysis of wf_03_prime.md"""
        # Mock wf_03_prime.md exists
        mock_file = MagicMock()
        mock_file.exists.return_value = True
        mock_file.read_text.return_value = """
        Quick Start mode: 2,500 tokens
        Full Context: 6,000 tokens
        Total optimization: 31,291 tokens
        """
        mock_path.return_value = mock_file

        result = analyze_prime_loading()

        assert "modes" in result
        assert "quick_start" in result["modes"]
        assert "full_context" in result["modes"]
        assert result["total_commands"] == 16
        assert result["optimization_implemented"] is True

    @patch('optimize_context_loading.Path')
    def test_analyze_prime_loading_file_not_found(self, mock_path):
        """Test when wf_03_prime.md doesn't exist"""
        mock_file = MagicMock()
        mock_file.exists.return_value = False
        mock_path.return_value = mock_file

        result = analyze_prime_loading()

        assert "error" in result
        assert result["error"] == "wf_03_prime.md not found"
        assert "modes" in result
        assert result["modes"] == {}

    def test_loading_analysis_dataclass(self):
        """Test LoadingAnalysis dataclass structure"""
        analysis = LoadingAnalysis(
            mode="Quick Start",
            auto_loaded_files=["PROJECT_INDEX.md", "CONTEXT.md"],
            estimated_tokens=2500,
            lazy_loaded_categories=["docs/guides/", "docs/examples/"],
            potential_tokens=23000
        )

        assert analysis.mode == "Quick Start"
        assert len(analysis.auto_loaded_files) == 2
        assert analysis.estimated_tokens == 2500
        assert len(analysis.lazy_loaded_categories) == 2
        assert analysis.potential_tokens == 23000


class TestDocsIndexAnalysis:
    """Test docs_index.json coverage analysis"""

    @patch('optimize_context_loading.Path')
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_docs_index_success(self, mock_file, mock_path):
        """Test successful docs_index.json analysis"""
        # Mock docs_index.json
        mock_index_file = MagicMock()
        mock_index_file.exists.return_value = True

        # Mock docs directory
        mock_docs_dir = MagicMock()
        mock_docs_dir.exists.return_value = True

        # Mock rglob to return some markdown files
        mock_md_files = [
            MagicMock(relative_to=lambda x: Path("docs/guides/guide1.md")),
            MagicMock(relative_to=lambda x: Path("docs/guides/guide2.md")),
            MagicMock(relative_to=lambda x: Path("docs/examples/example1.md"))
        ]
        mock_docs_dir.rglob.return_value = mock_md_files

        def path_side_effect(arg):
            if arg == "docs_index.json":
                return mock_index_file
            elif arg == "docs":
                return mock_docs_dir
            return MagicMock()

        mock_path.side_effect = path_side_effect

        # Mock JSON data
        mock_file.return_value.read.return_value = json.dumps({
            "always_load": {"files": ["PROJECT_INDEX.md"]},
            "command_mappings": {
                "/wf_03_prime": {
                    "guides": ["docs/guides/guide1.md"],
                    "examples": [],
                    "references": []
                }
            },
            "category_mappings": {
                "guides": {"files": ["docs/guides/*.md"]}
            }
        })

        total, indexed, missing = analyze_docs_index()

        assert total == 3  # 3 mock files
        assert indexed >= 0  # At least some indexed
        assert isinstance(missing, list)

    @patch('optimize_context_loading.Path')
    def test_analyze_docs_index_not_found(self, mock_path):
        """Test when docs_index.json doesn't exist"""
        mock_file = MagicMock()
        mock_file.exists.return_value = False
        mock_path.return_value = mock_file

        total, indexed, missing = analyze_docs_index()

        assert total == 0
        assert indexed == 0
        assert "docs_index.json not found" in missing

    def test_index_coverage_dataclass(self):
        """Test IndexCoverage dataclass structure"""
        coverage = IndexCoverage(
            total_docs=100,
            indexed_docs=75,
            missing_docs=["doc1.md", "doc2.md"],
            coverage_percentage=75.0
        )

        assert coverage.total_docs == 100
        assert coverage.indexed_docs == 75
        assert len(coverage.missing_docs) == 2
        assert coverage.coverage_percentage == 75.0


class TestOptimizationSuggestions:
    """Test optimization suggestions generation"""

    def test_suggest_optimizations_low_coverage(self):
        """Test suggestions when coverage is low (<90%)"""
        loading_analysis = {
            "modes": {
                "quick_start": {
                    "estimated_tokens": 2500,
                    "auto_loaded_files": ["PROJECT_INDEX.md"]
                }
            }
        }
        coverage = IndexCoverage(
            total_docs=100,
            indexed_docs=50,
            missing_docs=["doc1.md", "doc2.md", "doc3.md"],
            coverage_percentage=50.0
        )

        optimizations = suggest_optimizations(loading_analysis, coverage)

        # With quick_start tokens at 2500 (<3000), REDUCE_AUTO_LOAD is not generated
        # So we get: IMPROVE_INDEXING + LAZY_LOADING + CACHING_STRATEGY = 3 types
        assert len(optimizations) == 3

        # Check that IMPROVE_INDEXING suggestion exists (due to low coverage)
        indexing_opts = [opt for opt in optimizations if opt.type == OptimizationType.IMPROVE_INDEXING]
        assert len(indexing_opts) == 1
        assert indexing_opts[0].priority == Priority.HIGH

    def test_suggest_optimizations_high_coverage(self):
        """Test suggestions when coverage is high (>=90%)"""
        loading_analysis = {
            "modes": {
                "quick_start": {
                    "estimated_tokens": 2000,
                    "auto_loaded_files": ["PROJECT_INDEX.md"]
                }
            }
        }
        coverage = IndexCoverage(
            total_docs=100,
            indexed_docs=95,
            missing_docs=["doc1.md"],
            coverage_percentage=95.0
        )

        optimizations = suggest_optimizations(loading_analysis, coverage)

        # Should not include IMPROVE_INDEXING due to high coverage
        indexing_opts = [opt for opt in optimizations if opt.type == OptimizationType.IMPROVE_INDEXING]
        assert len(indexing_opts) == 0

    def test_suggest_optimizations_high_quick_start_tokens(self):
        """Test suggestions when Quick Start tokens are high"""
        loading_analysis = {
            "modes": {
                "quick_start": {
                    "estimated_tokens": 5000,  # > 3000
                    "auto_loaded_files": ["PROJECT_INDEX.md", "CONTEXT.md"]
                }
            }
        }
        coverage = IndexCoverage(
            total_docs=100,
            indexed_docs=95,
            missing_docs=[],
            coverage_percentage=95.0
        )

        optimizations = suggest_optimizations(loading_analysis, coverage)

        # Should include REDUCE_AUTO_LOAD due to high tokens
        reduce_opts = [opt for opt in optimizations if opt.type == OptimizationType.REDUCE_AUTO_LOAD]
        assert len(reduce_opts) == 1
        assert reduce_opts[0].priority == Priority.MEDIUM

    def test_optimization_dataclass(self):
        """Test Optimization dataclass structure"""
        opt = Optimization(
            type=OptimizationType.LAZY_LOADING,
            priority=Priority.HIGH,
            description="Test optimization",
            estimated_savings=5000,
            implementation_effort="中",
            details=["Detail 1", "Detail 2"]
        )

        assert opt.type == OptimizationType.LAZY_LOADING
        assert opt.priority == Priority.HIGH
        assert opt.estimated_savings == 5000
        assert len(opt.details) == 2


class TestTokenSavingsCalculation:
    """Test token savings calculation"""

    def test_calculate_token_savings_multiple_types(self):
        """Test calculation with multiple optimization types"""
        optimizations = [
            Optimization(
                type=OptimizationType.IMPROVE_INDEXING,
                priority=Priority.HIGH,
                description="Test 1",
                estimated_savings=3000,
                implementation_effort="中",
                details=[]
            ),
            Optimization(
                type=OptimizationType.LAZY_LOADING,
                priority=Priority.HIGH,
                description="Test 2",
                estimated_savings=5000,
                implementation_effort="中",
                details=[]
            ),
            Optimization(
                type=OptimizationType.CACHING_STRATEGY,
                priority=Priority.LOW,
                description="Test 3",
                estimated_savings=3000,
                implementation_effort="高",
                details=[]
            )
        ]

        result = calculate_token_savings(optimizations)

        assert result["total_savings"] == 11000  # 3000 + 5000 + 3000
        assert result["optimization_count"] == 3
        assert "by_type" in result
        assert "by_priority" in result

        # Check type breakdown
        assert result["by_type"]["改进索引覆盖"]["savings"] == 3000
        assert result["by_type"]["延迟加载优化"]["savings"] == 5000
        assert result["by_type"]["缓存策略"]["savings"] == 3000

        # Check priority breakdown
        assert result["by_priority"]["高"]["count"] == 2
        assert result["by_priority"]["高"]["savings"] == 8000  # 3000 + 5000
        assert result["by_priority"]["低"]["count"] == 1
        assert result["by_priority"]["低"]["savings"] == 3000

    def test_calculate_token_savings_empty_list(self):
        """Test calculation with empty optimization list"""
        result = calculate_token_savings([])

        assert result["total_savings"] == 0
        assert result["optimization_count"] == 0
        assert result["by_type"] == {}
        assert result["by_priority"] == {}


class TestReportGeneration:
    """Test report generation in Markdown and JSON formats"""

    def test_generate_markdown_report_structure(self):
        """Test Markdown report has correct structure"""
        loading_analysis = {
            "modes": {
                "quick_start": {
                    "mode": "Quick Start",
                    "auto_loaded_files": ["PROJECT_INDEX.md", "CONTEXT.md"],
                    "estimated_tokens": 2500,
                    "lazy_loaded_categories": ["docs/guides/"]
                }
            }
        }
        coverage = IndexCoverage(
            total_docs=100,
            indexed_docs=75,
            missing_docs=["doc1.md", "doc2.md"],
            coverage_percentage=75.0
        )
        optimizations = [
            Optimization(
                type=OptimizationType.IMPROVE_INDEXING,
                priority=Priority.HIGH,
                description="Test optimization",
                estimated_savings=5000,
                implementation_effort="中",
                details=["Detail 1", "Detail 2"]
            )
        ]
        savings = calculate_token_savings(optimizations)

        report = generate_report(loading_analysis, coverage, optimizations, savings, format="markdown")

        # Check key sections exist
        assert "# AI Workflow 上下文加载优化报告" in report
        assert "## 📊 当前加载分析" in report
        assert "## 🎯 索引覆盖率分析" in report
        assert "## 💡 优化建议" in report
        assert "## 📈 节省统计" in report
        assert "**总预估节省**: 5,000 tokens" in report

    def test_generate_json_report_structure(self):
        """Test JSON report has valid structure"""
        loading_analysis = {
            "modes": {
                "quick_start": {
                    "estimated_tokens": 2500
                }
            }
        }
        coverage = IndexCoverage(
            total_docs=100,
            indexed_docs=75,
            missing_docs=["doc1.md"],
            coverage_percentage=75.0
        )
        optimizations = [
            Optimization(
                type=OptimizationType.LAZY_LOADING,
                priority=Priority.HIGH,
                description="Test",
                estimated_savings=3000,
                implementation_effort="低",
                details=[]
            )
        ]
        savings = calculate_token_savings(optimizations)

        report = generate_report(loading_analysis, coverage, optimizations, savings, format="json")

        # Parse JSON to verify structure
        data = json.loads(report)
        assert "loading_analysis" in data
        assert "coverage" in data
        assert "optimizations" in data
        assert "savings" in data

        # Verify optimization data
        assert len(data["optimizations"]) == 1
        assert data["optimizations"][0]["type"] == "延迟加载优化"
        assert data["optimizations"][0]["priority"] == "高"
        assert data["optimizations"][0]["estimated_savings"] == 3000

    def test_generate_markdown_report_with_missing_docs(self):
        """Test Markdown report includes missing docs section"""
        loading_analysis = {"modes": {}}
        coverage = IndexCoverage(
            total_docs=20,
            indexed_docs=10,
            missing_docs=[f"doc{i}.md" for i in range(15)],  # 15 missing docs
            coverage_percentage=50.0
        )
        optimizations = []
        savings = {"total_savings": 0, "optimization_count": 0, "by_type": {}, "by_priority": {}}

        report = generate_report(loading_analysis, coverage, optimizations, savings, format="markdown")

        assert "缺失文档示例" in report
        # Should only show first 10 missing docs
        assert report.count("- doc") == 10  # Shows 10 examples


class TestMainFunction:
    """Test main function and CLI behavior"""

    @patch('optimize_context_loading.analyze_prime_loading')
    @patch('optimize_context_loading.analyze_docs_index')
    @patch('optimize_context_loading.sys.exit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_markdown_output(self, mock_stdout, mock_exit, mock_docs, mock_prime):
        """Test main function with markdown output"""
        mock_prime.return_value = {"modes": {}}
        mock_docs.return_value = (100, 75, ["doc1.md"])

        from optimize_context_loading import main

        with patch('sys.argv', ['script.py']):
            main()

        output = mock_stdout.getvalue()
        assert "# AI Workflow 上下文加载优化报告" in output
        mock_exit.assert_called_with(0)

    @patch('optimize_context_loading.analyze_prime_loading')
    @patch('optimize_context_loading.analyze_docs_index')
    @patch('optimize_context_loading.sys.exit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_json_output(self, mock_stdout, mock_exit, mock_docs, mock_prime):
        """Test main function with JSON output"""
        mock_prime.return_value = {"modes": {}}
        mock_docs.return_value = (100, 75, [])

        from optimize_context_loading import main

        with patch('sys.argv', ['script.py', '--format', 'json']):
            main()

        output = mock_stdout.getvalue()
        # Verify it's valid JSON
        data = json.loads(output)
        assert "loading_analysis" in data
        assert "coverage" in data
        mock_exit.assert_called_with(0)

    @patch('optimize_context_loading.analyze_prime_loading')
    @patch('optimize_context_loading.analyze_docs_index')
    @patch('optimize_context_loading.sys.exit')
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_verbose_mode(self, mock_stderr, mock_exit, mock_docs, mock_prime):
        """Test main function with verbose output"""
        mock_prime.return_value = {"modes": {}}
        mock_docs.return_value = (100, 75, [])

        from optimize_context_loading import main

        with patch('sys.argv', ['script.py', '--verbose']):
            main()

        stderr_output = mock_stderr.getvalue()
        assert "分析 wf_03_prime.md 加载逻辑" in stderr_output
        assert "分析 docs_index.json 覆盖率" in stderr_output
        assert "生成优化建议" in stderr_output


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_optimization_with_all_enum_types(self):
        """Test that all OptimizationType values work"""
        for opt_type in OptimizationType:
            opt = Optimization(
                type=opt_type,
                priority=Priority.MEDIUM,
                description="Test",
                estimated_savings=1000,
                implementation_effort="低",
                details=[]
            )
            assert opt.type == opt_type

    def test_optimization_with_all_priority_levels(self):
        """Test that all Priority values work"""
        for priority in Priority:
            opt = Optimization(
                type=OptimizationType.LAZY_LOADING,
                priority=priority,
                description="Test",
                estimated_savings=1000,
                implementation_effort="低",
                details=[]
            )
            assert opt.priority == priority

    def test_suggest_optimizations_with_no_modes(self):
        """Test optimization suggestions with empty loading analysis"""
        loading_analysis = {"modes": {}}
        coverage = IndexCoverage(
            total_docs=0,
            indexed_docs=0,
            missing_docs=[],
            coverage_percentage=0.0
        )

        optimizations = suggest_optimizations(loading_analysis, coverage)

        # Should still generate some optimizations
        assert len(optimizations) >= 2  # At least lazy loading and caching


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=optimize_context_loading", "--cov-report=term-missing"])
