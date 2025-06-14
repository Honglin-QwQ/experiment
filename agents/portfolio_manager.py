
import json
import re
from typing import Dict, Any, Optional, List
import pandas as pd
from dataclasses import dataclass
from loguru import logger
from agents.base_agent import BaseAgent, Message, MessageType
from config.system_config import SystemConfig, MarketType
from config.system_config import PromptTemplates
from llm.llm_client import OpenRouterClient, parse_json_response


@dataclass
class StructuredStrategyMandate:
    """结构化策略指令"""
    target_metrics: Dict[str, Any]
    risk_constraints: Dict[str, Any]
    universe: str
    investment_horizon: str
    additional_requirements: List[str]
    market_type: MarketType


class PortfolioManagerAgent(BaseAgent):
    """投资组合经理智能体"""

    def __init__(self, name: str, llm_client: OpenRouterClient, config: SystemConfig):
        super().__init__(name, llm_client, config)
        self.current_ssm: Optional[StructuredStrategyMandate] = None
        self.iteration_count = 0
        self.max_iterations = 3
        self.strategy_history: List[Dict[str, Any]] = []

    def get_system_prompt(self) -> str:
        """获取PM的系统提示词"""
        return PromptTemplates.pm_system_prompt()

    def process_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.type == MessageType.STRATEGY_MANDATE:
            return self._handle_investor_mandate(message)
        elif message.type == MessageType.SUB_STRATEGY_RESULT:
            return self._handle_sub_strategy_result(message)
        elif message.type == MessageType.COMPOSITE_RESULT:
            return self._handle_composite_result(message)
        elif message.type == MessageType.OPTIMIZATION_RESULT:
            return self._handle_optimization_result(message)
        elif message.type == MessageType.EVALUATION_RESULT:
            return self._handle_evaluation_result(message)
        return None

    def _handle_investor_mandate(self, message: Message) -> Message:
        """处理投资者指令"""
        investor_perspectives = message.content.get("perspectives", "")
        market_data = message.content.get("market_data", {})
        symbols = message.content.get("symbols", [])

        # 使用LLM解析投资者需求
        prompt = f"""
        Please analyze the following investor perspectives and convert them into a Structured Strategy Mandate (SSM).

        Investor Perspectives:
        {investor_perspectives}

        Available Symbols: {symbols}

        Current Market Conditions:
        {json.dumps(market_data, indent=2)}

        Please provide the SSM in the following JSON format (in English):
        {{
            "target_metrics": {{
                "annualized_return": {{"operator": ">", "value": 0.15}},
                "sharpe_ratio": {{"operator": ">", "value": 1.5}},
                "max_drawdown": {{"operator": "<", "value": 0.10}}
            }},
            "risk_constraints": {{
                "volatility": {{"operator": "<", "value": 0.20}},
                "correlation_with_benchmark": {{"operator": "<", "value": 0.8}}
            }},
            "universe": "US_EQUITIES or A_SHARES or FUTURES or CRYPTO",
            "investment_horizon": "short-term or medium-term or long-term",
            "market_type": "US_EQUITIES or A_SHARES or FUTURES or CRYPTO",
            "additional_requirements": ["requirement1", "requirement2"]
        }}
        CRITICAL: Please ensure the JSON response is complete and properly closed with all necessary closing braces. Do not truncate the response.
        
        """

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            model=self.config.models["pm_agent"],
            conversation_id=message.conversation_id
        )

        # ssm_dict = self.llm_client.parse_json_response(response.content)
        ssm_dict = parse_json_response(response.content)


        # 创建SSM对象
        self.current_ssm = StructuredStrategyMandate(
            target_metrics=ssm_dict.get("target_metrics", {}),
            risk_constraints=ssm_dict.get("risk_constraints", {}),
            universe=ssm_dict.get("universe", "US_EQUITIES"),
            investment_horizon=ssm_dict.get("investment_horizon", "medium-term"),
            additional_requirements=ssm_dict.get("additional_requirements", []),
            market_type=MarketType(ssm_dict.get("market_type", "US_EQUITIES"))
        )

        # 保存到状态
        self.state["ssm"] = self.current_ssm
        self.state["symbols"] = symbols
        self.iteration_count = 0

        logger.info(f"Created SSM: {self.current_ssm}")

        # 发送子策略请求
        return self.send_message(
            receiver="SubStrategyAgent",
            type=MessageType.SUB_STRATEGY_REQUEST,
            content={
                "ssm": ssm_dict,
                "symbols": symbols,
                "market_type": self.current_ssm.market_type.value,
                "iteration": self.iteration_count
            }
        )

    def _handle_sub_strategy_result(self, message: Message) -> Message:
        """处理子策略结果"""
        sub_strategies = message.content.get("sub_strategies", {})
        factor_returns = message.content.get("factor_returns", pd.DataFrame())
        factor_metrics = message.content.get("factor_metrics", pd.DataFrame())

        # 保存到状态
        self.state["sub_strategies"] = sub_strategies
        self.state["factor_returns"] = factor_returns
        self.state["factor_metrics"] = factor_metrics

        # 生成复合策略请求
        prompt = f"""
        Based on the SSM and the generated sub-strategies, please provide guidance for the Composite Strategy Agent.

        SSM Summary:
        - Target Return: {self.current_ssm.target_metrics.get('annualized_return', {})}
        - Risk Constraints: {self.current_ssm.risk_constraints}
        - Market Type: {self.current_ssm.market_type.value}

        Number of Sub-strategies Generated: {len(sub_strategies)}

        Please specify:
        1. Stability filtering criteria (e.g., minimum Sharpe ratio, maximum drawdown threshold)
        2. Ranking metrics and their weights for multi-criteria scoring
        3. Correlation threshold for diversification
        4. Minimum number of strategies to select

        Format as JSON:
        {{
            "stability_filters": {{
                "min_sharpe": 0.5,
                "max_drawdown": 0.15,
                "min_win_rate": 0.45
            }},
            "ranking_weights": {{
                "sharpe": 0.3,
                "calmar": 0.2,
                "annual_return": 0.3,
                "win_rate": 0.2
            }},
            "correlation_threshold": 0.7,
            "min_strategies": 5,
            "max_strategies": 20
        }}
        """

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            model=self.config.models["pm_agent"],
            conversation_id=message.conversation_id
        )

        # composite_config = self.llm_client.parse_json_response(response.content)
        composite_config = parse_json_response(response.content)

        return self.send_message(
            receiver="CompositeStrategyAgent",
            type=MessageType.COMPOSITE_REQUEST,
            content={
                "factor_returns": factor_returns.to_dict() if isinstance(factor_returns,
                                                                         pd.DataFrame) else factor_returns,
                "factor_metrics": factor_metrics.to_dict() if isinstance(factor_metrics,
                                                                         pd.DataFrame) else factor_metrics,
                "config": composite_config,
                "ssm": self.state["ssm"].__dict__ if hasattr(self.state["ssm"], '__dict__') else self.state["ssm"]
            }
        )

    def _handle_composite_result(self, message: Message) -> Message:
        """处理复合策略结果"""
        selected_strategies = message.content.get("selected_strategies", {})
        filtered_factor_returns = message.content.get("filtered_factor_returns", pd.DataFrame())

        self.state["selected_strategies"] = selected_strategies
        self.state["filtered_factor_returns"] = filtered_factor_returns

        # 生成优化请求
        prompt = f"""
        Based on the selected strategies and SSM requirements, provide optimization guidance.

        SSM Requirements:
        - Target Metrics: {self.current_ssm.target_metrics}
        - Risk Constraints: {self.current_ssm.risk_constraints}
        - Market Type: {self.current_ssm.market_type.value}

        Number of Selected Strategy Groups: {len(selected_strategies)}

        Please recommend:
        1. Optimization models to use (e.g., MaxSharpe, MinCVaR, RiskParity)
        2. Any specific constraints for the optimization
        3. Whether to use shrinkage estimators

        Format as JSON:
        {{
            "optimization_models": ["MaxSharpe", "RiskParity", "NCO"],
            "use_shrinkage": true,
            "additional_constraints": {{
                "min_weight": 0,
                "max_weight": 0.3,
                "leverage": 1.0
            }},
            "risk_measure": "VARIANCE"
        }}
        """

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            model=self.config.models["pm_agent"],
            conversation_id=message.conversation_id
        )

        # optimization_config = self.llm_client.parse_json_response(response.content)
        optimization_config = parse_json_response(response.content)

        return self.send_message(
            receiver="OptimizationAgent",
            type=MessageType.OPTIMIZATION_REQUEST,
            content={
                "selected_strategies": selected_strategies,
                "factor_returns": filtered_factor_returns.to_dict() if isinstance(filtered_factor_returns,
                                                                                  pd.DataFrame) else filtered_factor_returns,
                "config": optimization_config,
                "ssm": self.state["ssm"].__dict__ if hasattr(self.state["ssm"], '__dict__') else self.state["ssm"]
            }
        )

    def _handle_optimization_result(self, message: Message) -> Message:
        """处理优化结果"""
        optimization_results = message.content.get("results", {})
        best_strategy = message.content.get("best_strategy", {})

        self.state["optimization_results"] = optimization_results
        self.state["best_strategy"] = best_strategy

        # 请求性能评估
        return self.send_message(
            receiver="PerformanceJudgeAgent",
            type=MessageType.EVALUATION_REQUEST,
            content={
                "strategy": best_strategy,
                "ssm": self.state["ssm"].__dict__ if hasattr(self.state["ssm"], '__dict__') else self.state["ssm"],
                "symbols": self.state.get("symbols", [])
            }
        )

    def _handle_evaluation_result(self, message: Message) -> Message:
        """处理评估结果"""
        evaluation = message.content.get("evaluation", {})
        meets_requirements = message.content.get("meets_requirements", False)
        defects = message.content.get("defects", [])

        self.iteration_count += 1

        # 保存策略历史
        self.strategy_history.append({
            "iteration": self.iteration_count,
            "evaluation": evaluation,
            "meets_requirements": meets_requirements,
            "defects": defects
        })

        if meets_requirements or self.iteration_count >= self.max_iterations:
            # 策略满足要求或达到最大迭代次数
            logger.info(f"Strategy development completed after {self.iteration_count} iterations")

            return self.send_message(
                receiver="System",
                type=MessageType.INFO,
                content={
                    "status": "completed",
                    "final_strategy": self.state.get("best_strategy", {}),
                    "evaluation": evaluation,
                    "iterations": self.iteration_count,
                    "history": self.strategy_history
                }
            )
        else:
            # 需要改进策略
            return self._refine_strategy(defects, evaluation,self.state["ssm"].__dict__ if hasattr(self.state["ssm"], '__dict__') else self.state["ssm"])
    def load_factor_rules(self,content):
        """
        加载因子筛选规则的JSON内容
        """
        try:
            # 预处理JSON字符串
            json_match = re.search(r'\{[\s\S]*\}', content)
            if not json_match:
                raise ValueError("未找到有效的JSON内容")

            json_content = json_match.group()
            # 1. 将元组表示 (...) 替换为数组表示 [...]

            # 将JSON字符串转换为Python字典
            rules_dict = json.loads(json_content)



            # 将"false"字符串转换回Python的False
            def convert_false_strings(obj):
                if isinstance(obj, dict):
                    return {k: convert_false_strings(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_false_strings(x) for x in obj]
                elif obj == "false":
                    return False
                elif obj == "true":
                    return True
                return obj

            rules_dict = convert_false_strings(rules_dict)

            return rules_dict
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
        except Exception as e:
            print(f"发生错误: {e}")
            return None
    def _refine_strategy(self, defects: List[str], evaluation: Dict[str, Any],ssm) -> Message:
        """根据缺陷改进策略"""
        prompt = f"""
        The current strategy does not meet all requirements. Please analyze the defects and suggest refinements.

        Defects identified:
        {json.dumps(defects, indent=2)}

        Current Performance:
        {json.dumps(evaluation, indent=2)}
        
        Market Type:
        {self.current_ssm.market_type}

        Target Requirements:
        {json.dumps(self.current_ssm.target_metrics, indent=2)}

        Based on the defects analysis, please provide one refinement instructions for the appropriate agent:

        **For SubStrategyAgent (Normalization Method Selection):**
        - If performance shows negative weights in A-share market: Choose long-only methods (long_only_zscore, long_only_softmax)
        - If returns are below target: Use more aggressive methods (zscore, rank_s) for higher volatility
        - If drawdown exceeds limits: Use conservative methods (zscore_maxmin, max_min) for stability
        - If factor distribution is skewed: Consider rank-based methods (rank_balanced, rank_s)

        **For CompositeStrategyAgent (Factor Filtering Rules):**
        - If drawdown is excessive: Increase weight on low-drawdown sub-strategies, add Maximum Drawdown as primary filter
        - If returns are insufficient: Prioritize high-return sub-strategies, emphasize Annualized Return and Sharpe Ratio filters
        - If volatility is too high: Focus on Calmar Ratio and Downside Volatility metrics
        - If win rate is low: Emphasize Daily Win Rate and Trading Win Rate in filtering

        Please provide refinement instructions as JSON:
        {{
            "target_agent": "SubStrategyAgent" | "CompositeStrategyAgent",
            "refinement_type": "normalization_optimization" | "filtering_optimization",
            "instructions": {{
                // For SubStrategyAgent:
                "preferred_methods": ["method1", "method2"],  // Based on market constraints and performance gaps
                "avoid_methods": ["method3"],  // Methods causing issues (e.g., negative weights in A-shares)
                "risk_preference": "conservative" | "balanced" | "aggressive",  // Based on drawdown vs return trade-off
                "market_constraints": "A-shares require positive weights" | "Short selling allowed",

                // For CompositeStrategyAgent:
                "priority_metrics": ["metric1", "metric2"],  // Metrics to emphasize based on defects
                "weight_adjustments": {{
                    "high_return_strategies": 0.6,  // If returns are low
                    "low_drawdown_strategies": 0.7   // If drawdown is high
                }},
            }}
        }}

        Analysis Guidelines:
        1. Identify the primary defect (return shortfall vs risk excess vs market constraint violation)
        2. Select the most relevant agent to address the core issue
        3. Provide specific, actionable instructions based on the defect pattern
        4. Consider market characteristics (A-shares vs US/crypto/futures) for normalization choices
        5. Balance risk-return trade-offs in filtering rule adjustments
        """

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            model=self.config.models["pm_agent"]
        )

        # refinement = self.llm_client.parse_json_response(response.content)
        print(response.content)
        refinement = self.load_factor_rules(response.content)

        target_agent = refinement.get("target_agent", "SubStrategyAgent")

        # 根据目标智能体发送改进请求
        if target_agent == "SubStrategyAgent":
            return self.send_message(
                receiver="SubStrategyAgent",
                type=MessageType.SUB_STRATEGY_REQUEST,
                content={
                    "ssm": self.state["ssm"].__dict__ if hasattr(self.state["ssm"], '__dict__') else self.state["ssm"],
                    "symbols": self.state.get("symbols", []),
                    "market_type": self.current_ssm.market_type.value,
                    "iteration": self.iteration_count,
                    "refinement": refinement.get("instructions", {})
                }
            )
        elif target_agent == "CompositeStrategyAgent":
            return self.send_message(
                receiver="CompositeStrategyAgent",
                type=MessageType.COMPOSITE_REQUEST,
                content={
                    "factor_returns": self.state.get("factor_returns", pd.DataFrame()).to_dict(),
                    "factor_metrics": self.state.get("factor_metrics", pd.DataFrame()).to_dict(),
                    "refinement": refinement.get("instructions", {}),
                    "ssm": self.state["ssm"].__dict__ if hasattr(self.state["ssm"], '__dict__') else self.state["ssm"]
                }
            )
        else:  # OptimizationAgent
            return self.send_message(
                receiver="OptimizationAgent",
                type=MessageType.OPTIMIZATION_REQUEST,
                content={
                    "selected_strategies": self.state.get("selected_strategies", {}),
                    "factor_returns": self.state.get("filtered_factor_returns", pd.DataFrame()).to_dict(),
                    "config": refinement.get("instructions", {}),
                    "ssm": self.state["ssm"].__dict__ if hasattr(self.state["ssm"], '__dict__') else self.state["ssm"]
                }
            )
