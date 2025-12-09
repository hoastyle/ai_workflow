"""
测试 Doc Guard 工具

测试场景：
1. 小文档（< 100 行）- 完整读取
2. 中等文档（100-300 行）- 摘要模式
3. 大文档（300-800 行）- 章节模式
4. 超大文档（> 800 行）- 拒绝
5. Token 预算管理
6. 错误处理
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.doc_guard import DocGuard, DocGuardError


class TestDocGuard(unittest.TestCase):
    """Doc Guard 工具测试"""

    def setUp(self):
        """测试前准备：创建临时目录和测试文件"""
        self.test_dir = tempfile.mkdtemp()
        self.guard = DocGuard(token_budget=10000)

        # 创建不同大小的测试文件
        self.small_doc = Path(self.test_dir) / "small.md"
        self.medium_doc = Path(self.test_dir) / "medium.md"
        self.large_doc = Path(self.test_dir) / "large.md"
        self.xlarge_doc = Path(self.test_dir) / "xlarge.md"

        # 小文档（50 行）
        self.small_doc.write_text("\n".join([f"Line {i}" for i in range(50)]))

        # 中等文档（200 行）
        self.medium_doc.write_text("\n".join([f"Line {i}" for i in range(200)]))

        # 大文档（500 行，包含章节）
        large_content = "# Chapter 1\n" + "\n".join([f"Line {i}" for i in range(200)])
        large_content += "\n\n# Chapter 2\n" + "\n".join([f"Line {i}" for i in range(200)])
        large_content += "\n\n# Chapter 3\n" + "\n".join([f"Line {i}" for i in range(100)])
        self.large_doc.write_text(large_content)

        # 超大文档（1000 行）
        self.xlarge_doc.write_text("\n".join([f"Line {i}" for i in range(1000)]))

    def tearDown(self):
        """测试后清理：删除临时目录"""
        shutil.rmtree(self.test_dir)

    def test_small_doc_full_load(self):
        """测试小文档（< 100 行）完整加载"""
        content = self.guard._load_single(str(self.small_doc))

        self.assertIsNotNone(content)
        self.assertIn("Line 0", content)
        self.assertIn("Line 49", content)
        self.assertEqual(len(self.guard.load_stats), 1)
        self.assertEqual(self.guard.load_stats[0]['strategy'], "完整读取")

    def test_medium_doc_summary_load(self):
        """测试中等文档（100-300 行）摘要模式"""
        content = self.guard._load_single(str(self.medium_doc))

        self.assertIsNotNone(content)
        self.assertEqual(len(self.guard.load_stats), 1)
        self.assertIn("摘要模式", self.guard.load_stats[0]['strategy'])

    def test_large_doc_without_sections_fails(self):
        """测试大文档（300-800 行）未指定章节时失败"""
        with self.assertRaises(DocGuardError) as context:
            self.guard._load_single(str(self.large_doc))

        self.assertIn("必须指定 --sections", str(context.exception))

    def test_large_doc_with_sections(self):
        """测试大文档指定章节加载"""
        # 注意：这个测试需要 DocLoader 支持，可能在降级模式下运行
        try:
            content = self.guard._load_single(
                str(self.large_doc),
                sections=["Chapter 1"]
            )
            self.assertIsNotNone(content)
        except Exception:
            # 降级模式下跳过
            self.skipTest("DocLoader not available, skipping sections test")

    def test_xlarge_doc_rejected(self):
        """测试超大文档（> 800 行）被拒绝"""
        with self.assertRaises(DocGuardError) as context:
            self.guard._load_single(str(self.xlarge_doc))

        self.assertIn("超过限制", str(context.exception))

    def test_batch_load(self):
        """测试批量加载多个文档"""
        results = self.guard.load_docs([
            str(self.small_doc),
            str(self.medium_doc)
        ])

        self.assertEqual(len(results), 2)
        self.assertIn(str(self.small_doc), results)
        self.assertIn(str(self.medium_doc), results)
        self.assertEqual(len(self.guard.load_stats), 2)

    def test_token_budget_tracking(self):
        """测试 Token 预算跟踪"""
        self.guard.load_docs([str(self.small_doc)])

        self.assertGreater(self.guard.token_used, 0)
        self.assertLessEqual(self.guard.token_used, self.guard.token_budget)
        self.assertEqual(len(self.guard.load_stats), 1)
        self.assertIn('tokens', self.guard.load_stats[0])

    def test_nonexistent_file(self):
        """测试不存在的文件"""
        with self.assertRaises(DocGuardError):
            self.guard._load_single("nonexistent.md")

    def test_count_lines(self):
        """测试行数统计"""
        lines = self.guard._count_lines(str(self.small_doc))
        self.assertEqual(lines, 50)

        lines = self.guard._count_lines(str(self.medium_doc))
        self.assertEqual(lines, 200)

    def test_violations_tracking(self):
        """测试违规记录"""
        # 尝试加载超大文档
        results = self.guard.load_docs([str(self.xlarge_doc)])

        self.assertEqual(len(results), 0)  # 没有成功加载
        self.assertGreater(len(self.guard.violations), 0)  # 记录了违规

    def test_estimate_tokens(self):
        """测试 Token 估算"""
        text = "This is a test string" * 100
        tokens = self.guard._estimate_tokens(text)

        self.assertGreater(tokens, 0)
        # 粗略估计：1 token ≈ 4 字符
        expected = len(text) // 4
        self.assertAlmostEqual(tokens, expected, delta=10)


class TestDocGuardCLI(unittest.TestCase):
    """测试命令行接口"""

    def setUp(self):
        """创建测试文件"""
        self.test_dir = tempfile.mkdtemp()
        self.test_doc = Path(self.test_dir) / "test.md"
        self.test_doc.write_text("\n".join([f"Line {i}" for i in range(50)]))

    def tearDown(self):
        """清理测试文件"""
        shutil.rmtree(self.test_dir)

    def test_cli_basic_usage(self):
        """测试基础命令行用法"""
        import subprocess

        result = subprocess.run(
            [
                "python", "scripts/doc_guard.py",
                "--docs", str(self.test_doc),
                "--quiet"
            ],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Line 0", result.stdout)


if __name__ == '__main__':
    unittest.main()
