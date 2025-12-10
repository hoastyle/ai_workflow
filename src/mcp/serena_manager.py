"""
Serena MCP 连接管理器 - 处理连接故障、重试和自动降级

解决问题：wf_03_prime 经常无法连接到 Serena MCP
- 自动检测连接状态
- 实施重试机制
- 自动降级到传统模式
- 提供连接诊断日志
"""

import time
import logging
import subprocess
import sys
from typing import Optional, Dict, Any
from pathlib import Path


logger = logging.getLogger(__name__)


class SerenaConnectionManager:
    """Serena MCP 连接管理器"""

    def __init__(self, timeout: int = 10, max_retries: int = 3):
        """
        初始化连接管理器

        Args:
            timeout: 单次连接尝试超时时间（秒）
            max_retries: 最大重试次数
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self._connection_status = None
        self._last_check_time = 0
        self._cache_ttl = 30  # 30秒缓存连接状态

    def is_available(self, use_cache: bool = True) -> bool:
        """
        检查 Serena MCP 是否可用

        Args:
            use_cache: 是否使用缓存的连接状态

        Returns:
            True 如果可用，False 如果不可用
        """
        current_time = time.time()

        # 使用缓存（30秒有效期）
        if use_cache and self._connection_status is not None:
            if current_time - self._last_check_time < self._cache_ttl:
                return self._connection_status

        # 检查连接
        available = self._check_connection()
        self._connection_status = available
        self._last_check_time = current_time

        return available

    def _check_connection(self) -> bool:
        """
        实际检查 Serena 连接

        Returns:
            True 如果可以连接，False 如果失败
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"检查 Serena 连接 (尝试 {attempt + 1}/{self.max_retries})")

                # 尝试启动 Serena MCP 进程并立即检查
                result = subprocess.run(
                    [
                        "uvx",
                        "--from",
                        "git+https://github.com/oraios/serena",
                        "serena",
                        "--version"
                    ],
                    capture_output=True,
                    timeout=self.timeout,
                    text=True
                )

                if result.returncode == 0:
                    logger.info("✅ Serena 连接成功")
                    return True
                else:
                    logger.warning(f"⚠️  Serena 返回错误: {result.stderr}")

            except subprocess.TimeoutExpired:
                logger.warning(f"⏱️  连接超时 (timeout={self.timeout}s)")

            except Exception as e:
                logger.error(f"❌ 连接错误: {str(e)}")

            # 重试前等待
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避：1s, 2s, 4s
                logger.info(f"等待 {wait_time}s 后重试...")
                time.sleep(wait_time)

        logger.error("❌ Serena 连接失败，所有重试都已耗尽")
        return False

    def get_fallback_mode(self) -> str:
        """
        获取降级模式

        Returns:
            降级模式：'traditional' (传统模式), 'lightweight' (轻量级模式)
        """
        if self.is_available():
            return "serena"  # 可用
        else:
            return "traditional"  # 降级到传统模式

    def reset_cache(self):
        """重置连接状态缓存"""
        self._connection_status = None
        self._last_check_time = 0


class WF03PrimeAdapter:
    """wf_03_prime 的 MCP 适配器"""

    def __init__(self):
        self.serena = SerenaConnectionManager(timeout=10, max_retries=2)
        self._mode = None

    def detect_mode(self) -> str:
        """
        检测应该使用哪种模式

        Returns:
            执行模式：
            - 'serena': 使用 Serena MCP（智能加载）
            - 'traditional': 使用传统模式（基础加载）
            - 'quick': 轻量级快速加载
        """
        # 如果 Serena 可用，使用智能模式
        if self.serena.is_available(use_cache=True):
            logger.info("📍 选择执行模式: Serena 智能加载")
            self._mode = "serena"
        else:
            logger.warning("⚠️  Serena 不可用，降级到传统模式")
            self._mode = "traditional"

        return self._mode

    def get_load_strategy(self) -> Dict[str, Any]:
        """
        根据模式返回加载策略

        Returns:
            加载策略配置
        """
        mode = self.detect_mode()

        strategies = {
            "serena": {
                "mode": "smart",
                "use_mcp": True,
                "enable_lsp": True,
                "timeout": 30,
                "features": ["semantic_search", "symbol_index", "cross_module_analysis"]
            },
            "traditional": {
                "mode": "traditional",
                "use_mcp": False,
                "enable_lsp": False,
                "timeout": 10,
                "features": ["basic_loading", "file_reading"]
            }
        }

        return strategies.get(mode, strategies["traditional"])

    def log_diagnostics(self):
        """输出诊断信息"""
        logger.info("=" * 60)
        logger.info("🔍 wf_03_prime MCP 诊断报告")
        logger.info("=" * 60)
        logger.info(f"Serena 连接状态: {self.serena.is_available()}")
        logger.info(f"执行模式: {self._mode or '未检测'}")
        logger.info(f"Timeout: {self.serena.timeout}s")
        logger.info(f"最大重试: {self.serena.max_retries}")
        logger.info("=" * 60)


# 全局适配器实例
_wf03_adapter = None


def get_wf03_adapter() -> WF03PrimeAdapter:
    """获取全局的 wf_03_prime 适配器"""
    global _wf03_adapter
    if _wf03_adapter is None:
        _wf03_adapter = WF03PrimeAdapter()
    return _wf03_adapter


def should_use_serena() -> bool:
    """判断是否应该使用 Serena MCP"""
    adapter = get_wf03_adapter()
    return adapter.serena.is_available()


def get_fallback_strategy() -> str:
    """获取降级策略"""
    adapter = get_wf03_adapter()
    mode = adapter.detect_mode()

    if mode == "serena":
        return "smart_loading"
    else:
        return "traditional_reading"


if __name__ == "__main__":
    # 测试连接
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    adapter = get_wf03_adapter()
    adapter.log_diagnostics()

    # 输出加载策略
    strategy = adapter.get_load_strategy()
    print("\n📊 加载策略:")
    for key, value in strategy.items():
        print(f"  {key}: {value}")
