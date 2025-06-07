# main.py
import os
import json
import pickle

import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

from config.system_config import SystemConfig
from llm.llm_client import OpenRouterClient
from agents.portfolio_manager import PortfolioManagerAgent
from agents.sub_strategy_agent import SubStrategyAgent
from agents.composite_strategy_agent import CompositeStrategyAgent
from agents.optimization_agent import OptimizationAgent
from agents.performance_judge_agent import PerformanceJudgeAgent
from agents.base_agent import Message, MessageType



class MultiAgentPortfolioSystem:
    """多智能体投资组合管理系统"""

    def __init__(self, config: SystemConfig, factor_calculator, backtest_system):
        self.config = config
        self.llm_client = OpenRouterClient(config)

        # 初始化所有智能体
        self.agents = {
            "PMAgent": PortfolioManagerAgent(
                "PMAgent", self.llm_client, config
            ),
            "SubStrategyAgent": SubStrategyAgent(
                "SubStrategyAgent", self.llm_client, config,
                factor_calculator, backtest_system
            ),
            "CompositeStrategyAgent": CompositeStrategyAgent(
                "CompositeStrategyAgent", self.llm_client, config
            ),
            "OptimizationAgent": OptimizationAgent(
                "OptimizationAgent", self.llm_client, config
            ),
            "PerformanceJudgeAgent": PerformanceJudgeAgent(
                "PerformanceJudgeAgent", self.llm_client, config,
                backtest_system
            )
        }

        self.message_queue: List[Message] = []
        self.conversation_id = str(datetime.now().timestamp())
        self.results = {}

        logger.info("Multi-Agent Portfolio System initialized")

    def process_investor_mandate(self,
                                 investor_perspectives: str,
                                 symbols: List[str],
                                 market_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """处理投资者指令"""
        logger.info("Processing investor mandate...")

        # 创建初始消息
        initial_message = Message.create(
            sender="System",
            receiver="PMAgent",
            type=MessageType.STRATEGY_MANDATE,
            content={
                "perspectives": investor_perspectives,
                "symbols": symbols,
                "market_data": market_data or {}
            },
            conversation_id=self.conversation_id
        )

        # 添加到消息队列
        self.message_queue.append(initial_message)

        # 处理消息队列
        self._process_message_queue()

        # 返回最终结果
        return self.results

    def _process_message_queue(self):
        """处理消息队列"""
        max_iterations = 100  # 防止无限循环
        iteration = 0

        while self.message_queue and iteration < max_iterations:
            iteration += 1
            message = self.message_queue.pop(0)

            # 如果接收者是系统，保存结果
            if message.receiver == "System":
                self._handle_system_message(message)
                continue

            # 找到接收者智能体
            receiver_agent = self.agents.get(message.receiver)
            if receiver_agent:
                logger.info(f"Delivering message from {message.sender} to {message.receiver}")
                response = receiver_agent.receive_message(message)

                # 如果有响应，添加到队列
                if response:
                    self.message_queue.append(response)
            else:
                logger.error(f"Unknown receiver: {message.receiver}")

    def _handle_system_message(self, message: Message):
        """处理发送给系统的消息"""
        if message.type == MessageType.INFO:
            content = message.content
            if content.get("status") == "completed":
                self.results = {
                    "status": "success",
                    "final_strategy": content.get("final_strategy", {}),
                    "evaluation": content.get("evaluation", {}),
                    "iterations": content.get("iterations", 0),
                    "history": content.get("history", []),
                    "timestamp": datetime.now().isoformat()
                }
                logger.info("Strategy development completed successfully")
        elif message.type == MessageType.ERROR:
            self.results = {
                "status": "error",
                "error": message.content.get("error", "Unknown error"),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"Strategy development failed: {message.content.get('error')}")

    def save_results(self, filename: str):
        """保存结果到文件"""
        output_path = os.path.join(self.config.output_path, filename)
        os.makedirs(self.config.output_path, exist_ok=True)

        with open(output_path, 'wb') as f:
            pickle.dump(self.results, f)

        logger.info(f"Results saved to {output_path}")


# 使用示例
if __name__ == "__main__":
    from experiment import factor_to_strategy  # 导入因子计算模块
    from backtest import WeightBacktest  # 导入回测模块

    # 配置系统
    config = SystemConfig(
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
        models={
            "pm_agent": "anthropic/claude-3-haiku",
            "sub_strategy_agent": "anthropic/claude-sonnet-4",
            "composite_agent": "anthropic/claude-3-haiku",
            "optimization_agent": "anthropic/claude-3-haiku",
            "performance_agent": "anthropic/claude-3-haiku"
        }
    )

    # 初始化因子计算器和回测系统
    factor_calculator = factor_to_strategy(d='spot')  # 因子计算器实例

    # 创建系统
    system = MultiAgentPortfolioSystem(
        config=config,
        factor_calculator=factor_calculator,
        backtest_system=WeightBacktest
    )

    # 定义投资者需求
    investor_perspectives = """
    I hope to construct a quantitative investment for the US market, with the following specific requirements:  
    1. Target annualized return exceeding 15%.  
    2. Maximum drawdown controlled within 10%.  
    3. Sharpe ratio greater than 1.5.  
    4. Investment universe includes S&P 500 constituents.  
    5. Consider the current macro environment of potential Federal Reserve interest rate cuts.  
    6. Expect the strategy to perform stably across different market conditions.
    """

    # 投资标的
    symbols = ['GOOGL']

    # 市场数据（可选）
    market_data = {

    }

    # 运行系统
    results = system.process_investor_mandate(
        investor_perspectives=investor_perspectives,
        symbols=symbols,
        market_data=market_data
    )

    # 保存结果
    system.save_results(f"strategy_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl")


    # 打印结果摘要
    if results.get("status") == "success":
        print("\n=== 策略开发成功 ===")
        print(f"迭代次数: {results.get('iterations', 0)}")
        print(f"最终评分: {results.get('evaluation', {}).get('summary', {}).get('overall_score', 0)}")
        print(f"主要优势: {results.get('evaluation', {}).get('summary', {}).get('key_strengths', [])}")
        print(f"建议: {results.get('evaluation', {}).get('summary', {}).get('recommendation', '')}")
    else:
        print(f"\n=== 策略开发失败 ===")
        print(f"错误: {results.get('error', 'Unknown error')}")