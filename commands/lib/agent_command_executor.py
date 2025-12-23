"""
Agent Command Executor - 命令执行器

负责实际执行 Agent 推荐的命令。

核心功能:
- 验证 Agent 推荐命令的有效性
- 准备执行环境（加载 MCP 工具）
- 执行命令并捕获结果
- 记录执行历史和性能指标
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
import subprocess
import time
import json
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """执行结果数据结构"""

    # 执行状态: "success", "failure", "timeout", "error"
    status: str

    # Agent 推荐的命令
    command: str

    # 执行输出
    output: str = ""

    # 错误信息
    error: str = ""

    # 执行时间 (秒)
    execution_time: float = 0.0

    # 退出码
    exit_code: int = 0

    # Agent 信息
    agent_id: str = ""
    agent_name: str = ""

    # 匹配度评分
    match_score: float = 0.0

    # 用户原始命令
    user_command: str = ""

    # 执行开始时间
    start_time: str = ""

    # 执行结束时间
    end_time: str = ""

    # 使用的 MCP 工具
    mcp_tools_used: List[str] = field(default_factory=list)

    # 是否影响了最终行为
    affected_behavior: bool = False

    # 其他元数据
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentCommandExecutor:
    """Agent 命令执行器"""

    # 执行超时（秒）
    DEFAULT_TIMEOUT = 30

    # 最大输出大小（字节）
    MAX_OUTPUT_SIZE = 100000

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        """
        初始化执行器

        Args:
            timeout: 执行超时时间（秒）
        """
        self.timeout = timeout
        self.execution_history: List[Dict] = []

    def execute_agent_command(
        self,
        agent: Any,  # Agent 对象
        command: str,
        user_command: str = "",
        match_score: float = 0.0,
        context: Dict = None,
    ) -> ExecutionResult:
        """
        执行 Agent 推荐的命令

        Args:
            agent: Agent 对象
            command: 要执行的命令
            user_command: 用户原始命令
            match_score: Agent 匹配度评分
            context: 执行上下文

        Returns:
            ExecutionResult: 执行结果
        """
        context = context or {}
        start_time = datetime.now()

        try:
            # Step 1: 验证命令有效性
            if not command or not isinstance(command, str):
                return self._create_result(
                    status="error",
                    command=command,
                    error="Invalid command: empty or non-string",
                    agent=agent,
                    user_command=user_command,
                    match_score=match_score,
                    start_time=start_time,
                )

            # Step 2: 准备执行环境
            env_result = self._prepare_environment(agent, context)
            if not env_result:
                return self._create_result(
                    status="error",
                    command=command,
                    error="Failed to prepare execution environment",
                    agent=agent,
                    user_command=user_command,
                    match_score=match_score,
                    start_time=start_time,
                )

            # Step 3: 执行命令
            exec_result = self._execute_command(command, context)

            # Step 4: 后处理执行结果
            return self._post_process_result(
                exec_result,
                agent=agent,
                user_command=user_command,
                match_score=match_score,
                start_time=start_time,
                context=context,
                command=command,
            )

        except Exception as e:
            logger.error(f"执行 Agent 命令时出错: {e}")
            return self._create_result(
                status="error",
                command=command,
                error=str(e),
                agent=agent,
                user_command=user_command,
                match_score=match_score,
                start_time=start_time,
            )

    def _prepare_environment(self, agent: Any, context: Dict) -> bool:
        """
        准备执行环境

        Args:
            agent: Agent 对象
            context: 执行上下文

        Returns:
            是否准备成功
        """
        try:
            # 提取 MCP 工具需求
            mcp_tools = context.get("mcp_tools", [])

            # 如果有 MCP 工具需求，进行初始化
            if mcp_tools:
                return self._load_mcp_tools(mcp_tools)

            return True

        except Exception as e:
            logger.error(f"准备执行环境失败: {e}")
            return False

    def _load_mcp_tools(self, tools: List[str]) -> bool:
        """
        加载 MCP 工具

        Args:
            tools: 工具列表

        Returns:
            是否加载成功
        """
        try:
            # 简化实现：仅验证工具名称有效
            valid_tools = {"serena", "context7", "tavily", "sequential-thinking"}
            loaded_tools = []

            for tool in tools:
                if tool in valid_tools:
                    loaded_tools.append(tool)
                    logger.debug(f"加载 MCP 工具: {tool}")

            return len(loaded_tools) > 0 or len(tools) == 0

        except Exception as e:
            logger.error(f"加载 MCP 工具失败: {e}")
            return False

    def _execute_command(self, command: str, context: Dict) -> Tuple[str, str, int, float]:
        """
        执行命令

        Args:
            command: 要执行的命令
            context: 执行上下文

        Returns:
            (输出, 错误, 退出码, 执行时间)
        """
        start = time.time()

        try:
            # 用 subprocess 执行命令
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )

            execution_time = time.time() - start

            # 限制输出大小
            output = result.stdout[: self.MAX_OUTPUT_SIZE]
            error = result.stderr[: self.MAX_OUTPUT_SIZE]

            return output, error, result.returncode, execution_time

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start
            error = f"命令执行超时 ({self.timeout}秒)"
            return "", error, -1, execution_time

        except Exception as e:
            execution_time = time.time() - start
            error = f"执行异常: {str(e)}"
            return "", error, -1, execution_time

    def _post_process_result(
        self,
        exec_result: Tuple[str, str, int, float],
        agent: Any,
        user_command: str,
        match_score: float,
        start_time: datetime,
        context: Dict,
        command: str = "",
    ) -> ExecutionResult:
        """
        后处理执行结果

        Args:
            exec_result: 执行结果元组
            agent: Agent 对象
            user_command: 用户命令
            match_score: 匹配度
            start_time: 开始时间
            context: 执行上下文
            command: 执行的命令

        Returns:
            处理后的 ExecutionResult
        """
        output, error, exit_code, execution_time = exec_result

        # 判断执行状态
        if error and "超时" in error:
            status = "timeout"
        elif exit_code != 0:
            status = "failure"
        else:
            status = "success"

        # 使用传入的命令或上下文中的命令
        final_command = command or context.get("agent_command", "")

        result = ExecutionResult(
            status=status,
            command=final_command,
            output=output,
            error=error,
            execution_time=execution_time,
            exit_code=exit_code,
            agent_id=getattr(agent, "name", "unknown"),
            agent_name=getattr(agent, "role", "Unknown Agent"),
            match_score=match_score,
            user_command=user_command,
            start_time=start_time.isoformat(),
            end_time=datetime.now().isoformat(),
            mcp_tools_used=context.get("mcp_tools", []),
            affected_behavior=status == "success",
        )

        # 记录执行历史
        self._record_execution(result)

        return result

    def _create_result(
        self,
        status: str,
        command: str,
        error: str = "",
        agent: Any = None,
        user_command: str = "",
        match_score: float = 0.0,
        start_time: datetime = None,
    ) -> ExecutionResult:
        """
        创建 ExecutionResult 对象

        Args:
            status: 执行状态
            command: 命令
            error: 错误信息
            agent: Agent 对象
            user_command: 用户命令
            match_score: 匹配度
            start_time: 开始时间

        Returns:
            ExecutionResult
        """
        start_time = start_time or datetime.now()
        end_time = datetime.now()

        return ExecutionResult(
            status=status,
            command=command,
            error=error,
            execution_time=(end_time - start_time).total_seconds(),
            agent_id=getattr(agent, "name", "unknown") if agent else "unknown",
            agent_name=getattr(agent, "role", "Unknown Agent") if agent else "Unknown Agent",
            match_score=match_score,
            user_command=user_command,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            affected_behavior=False,
        )

    def _record_execution(self, result: ExecutionResult) -> None:
        """
        记录执行历史

        Args:
            result: 执行结果
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "status": result.status,
            "command": result.command,
            "agent_id": result.agent_id,
            "match_score": result.match_score,
            "execution_time": result.execution_time,
            "affected_behavior": result.affected_behavior,
        }

        self.execution_history.append(record)

        # 保持历史记录在合理大小（最多 1000 条）
        if len(self.execution_history) > 1000:
            self.execution_history = self.execution_history[-500:]

    def get_execution_history(self) -> List[Dict]:
        """
        获取执行历史

        Returns:
            执行历史记录列表
        """
        return self.execution_history.copy()

    def get_execution_statistics(self) -> Dict[str, Any]:
        """
        获取执行统计信息

        Returns:
            统计信息字典
        """
        if not self.execution_history:
            return {
                "total_executions": 0,
                "success_count": 0,
                "failure_count": 0,
                "timeout_count": 0,
                "error_count": 0,
                "success_rate": 0.0,
                "average_execution_time": 0.0,
            }

        total = len(self.execution_history)
        success_count = sum(1 for r in self.execution_history if r["status"] == "success")
        failure_count = sum(1 for r in self.execution_history if r["status"] == "failure")
        timeout_count = sum(1 for r in self.execution_history if r["status"] == "timeout")
        error_count = sum(1 for r in self.execution_history if r["status"] == "error")

        avg_time = sum(r["execution_time"] for r in self.execution_history) / total

        return {
            "total_executions": total,
            "success_count": success_count,
            "failure_count": failure_count,
            "timeout_count": timeout_count,
            "error_count": error_count,
            "success_rate": success_count / total if total > 0 else 0.0,
            "average_execution_time": avg_time,
        }

    def clear_history(self) -> None:
        """清空执行历史"""
        self.execution_history.clear()
