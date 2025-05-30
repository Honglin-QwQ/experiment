# agents/performance_judge_agent.py
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from loguru import logger
import json
from agents.base_agent import BaseAgent, Message, MessageType

from config.system_config import SystemConfig
from config.system_config import PromptTemplates
from llm.llm_client import OpenRouterClient, parse_json_response


class PerformanceJudgeAgent(BaseAgent):
    """性能评判智能体 - 负责策略评估和反馈"""

    def __init__(self, name: str, llm_client: OpenRouterClient, config: SystemConfig,
                 backtest_system):
        super().__init__(name, llm_client, config)
        self.backtest_system = backtest_system
        self.defect_categories = {
            "EXCESSIVE_DRAWDOWN": "Maximum drawdown exceeds limit",
            "LOW_SHARPE": "Sharpe ratio is too low",
            "INSUFFICIENT_RETURN": "Return did not meet target",
            "HIGH_VOLATILITY": "Volatility is too high",
            "POOR_WIN_RATE": "Win rate is too low",
            "FACTOR_DECAY": "Factor decay",
            "HIGH_TURNOVER": "Turnover rate is too high",
            "CORRELATION_RISK": "Correlation risk",
            "TAIL_RISK": "Tail risk"
        }

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return PromptTemplates.performance_system_prompt()

    def process_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.type == MessageType.EVALUATION_REQUEST:
            return self._handle_evaluation_request(message)
        return None

    def _handle_evaluation_request(self, message: Message) -> Message:
        """处理评估请求"""
        try:
            strategy = message.content.get("strategy", {})
            ssm = message.content.get("ssm", {})
            symbols = message.content.get("symbols", [])

            # 执行全面评估
            logger.info("Performing comprehensive evaluation...")

            # 1. 基础性能评估
            # performance_metrics = self._evaluate_basic_performance(strategy, symbols)
            performance_metrics = self._evaluate_basic_performance(strategy)

            # 2. 压力测试
            stress_test_results = self._perform_stress_testing(strategy, ssm)

            # 3. SSM合规性检查
            compliance_check = self._check_ssm_compliance(performance_metrics, ssm)

            # 4. 识别缺陷
            defects = self._identify_defects(
                performance_metrics,
                stress_test_results,
                compliance_check,
                ssm
            )

            # 5. 生成评估报告
            evaluation_report = self._generate_evaluation_report(
                performance_metrics,
                stress_test_results,
                compliance_check,
                defects
            )

            # 6. 判断是否满足要求
            meets_requirements = len(defects) == 0 and compliance_check["overall_compliance"]

            return self.send_message(
                receiver=message.sender,
                type=MessageType.EVALUATION_RESULT,
                content={
                    "evaluation": evaluation_report,
                    "meets_requirements": meets_requirements,
                    "defects": defects,
                    "performance_metrics": performance_metrics,
                    "stress_test_results": stress_test_results,
                    "compliance_check": compliance_check
                }
            )

        except Exception as e:
            logger.error(f"Error in performance evaluation: {str(e)}")
            return self.send_message(
                receiver=message.sender,
                type=MessageType.ERROR,
                content={"error": str(e)}
            )

    # def _evaluate_basic_performance(self, strategy: Dict[str, Any],
    #                                 symbols: List[str]) -> Dict[str, Any]:
    #     """评估基础性能"""
    #     # 获取策略权重和回报
    #     weights = strategy.get("weights", pd.DataFrame())
    #     portfolio = strategy.get("portfolio", None)
    #
    #     if isinstance(weights, dict):
    #         weights = pd.DataFrame(weights)
    #
    #     # 准备回测数据
    #     if not weights.empty and symbols:
    #         # 这里需要根据实际的数据格式调整
    #         backtest_results = self._run_comprehensive_backtest(weights, symbols)
    #     else:
    #         # 使用提供的portfolio对象
    #         backtest_results = self._extract_portfolio_metrics(portfolio)
    #
    #     return backtest_results
    def _evaluate_basic_performance(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """评估基础性能"""
        # 获取策略权重和回报
        performance = strategy.get("performance")
        portfolio = strategy.get("portfolio", None)

        # 准备回测数据
        if not performance:
            backtest_results=performance
        else:
            # 使用提供的portfolio对象
            backtest_results = self._extract_portfolio_metrics(portfolio)

        return backtest_results

    def _perform_stress_testing(self, strategy: Dict[str, Any],
                                ssm: Dict[str, Any]) -> Dict[str, Any]:
        """执行压力测试"""
        prompt = f"""
        Based on the strategy and market conditions, design stress test scenarios.

        Strategy Type: {strategy.get('strategy_name', 'Unknown')}
        Market Type: {ssm.get('market_type', 'US_EQUITIES')}

        Please suggest 3-5 stress test scenarios that are relevant, including:
        1. Historical crisis scenarios (e.g., 2008 financial crisis, COVID-19 crash)
        2. Hypothetical extreme scenarios (e.g., sudden rate hikes, liquidity crisis)
        3. Factor-specific shocks relevant to the strategy

        For each scenario, specify:
        - Name and description
        - Expected market movements (e.g., equity -30%, volatility +200%)
        - Duration (in days)
        - Specific risks to test

        Format as JSON, in English:
        {{
            "scenarios": [
                {{
                    "name": "scenario_name",
                    "description": "description",
                    "market_shocks": {{"asset_class": "percentage_change"}},
                    "volatility_multiplier": 2.0,
                    "duration_days": 30,
                    "test_focus": ["risk1", "risk2"]
                }}
            ]
        }}
        """

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            model=self.config.models["performance_agent"],
            temperature=self.config.llm_config["temperature"]
        )

        # scenarios = self.llm_client.parse_json_response(response.content)
        scenarios = parse_json_response(response.content)

        # 执行压力测试
        stress_results = {}

        for scenario in scenarios.get("scenarios", []):
            # 这里简化处理，实际应该根据场景调整数据并重新计算
            scenario_result = {
                "scenario_name": scenario["name"],
                "estimated_loss": np.random.uniform(0.05, 0.25),  # 示例
                "recovery_time": np.random.randint(30, 180),  # 示例
                "risk_metrics": {
                    "var_95": np.random.uniform(0.02, 0.08),
                    "cvar_95": np.random.uniform(0.05, 0.15),
                    "max_drawdown": np.random.uniform(0.10, 0.40)
                }
            }
            stress_results[scenario["name"]] = scenario_result

        return stress_results

    def _check_ssm_compliance(self, performance_metrics: Dict[str, Any],
                              ssm: Dict[str, Any]) -> Dict[str, Any]:
        """检查SSM合规性"""
        compliance_results = {
            "target_metrics": {},
            "risk_constraints": {},
            "overall_compliance": True
        }

        # 检查目标指标
        target_metrics = ssm.get("target_metrics", {})
        for metric, requirement in target_metrics.items():
            operator = requirement.get("operator", ">=")
            target_value = requirement.get("value", 0)

            # 映射指标名称
            metric_mapping = {
                "annualized_return": "Annual Return",
                "sharpe_ratio": "Sharpe Ratio",
                "max_drawdown": "Maximum Drawdown"
            }

            actual_metric = metric_mapping.get(metric, metric)
            actual_value = performance_metrics.get(actual_metric, 0)

            # 检查是否满足要求
            if operator == ">":
                meets = actual_value > target_value
            elif operator == ">=":
                meets = actual_value >= target_value
            elif operator == "<":
                meets = actual_value < target_value
            elif operator == "<=":
                meets = actual_value <= target_value
            else:
                meets = actual_value == target_value

            compliance_results["target_metrics"][metric] = {
                "target": f"{operator} {target_value}",
                "actual": actual_value,
                "meets_requirement": meets
            }

            if not meets:
                compliance_results["overall_compliance"] = False

        # 检查风险约束
        risk_constraints = ssm.get("risk_constraints", {})
        for constraint, requirement in risk_constraints.items():
            # 类似处理...
            pass

        return compliance_results

    def _identify_defects(self, performance_metrics: Dict[str, Any],
                          stress_test_results: Dict[str, Any],
                          compliance_check: Dict[str, Any],
                          ssm: Dict[str, Any]) -> List[str]:
        """识别策略缺陷"""
        defects = []

        # 基于性能指标识别缺陷
        if performance_metrics.get("Maximum Drawdown", 0) > 0.15:
            defects.append("EXCESSIVE_DRAWDOWN")

        if performance_metrics.get("Sharpe Ratio", 0) < 1.0:
            defects.append("LOW_SHARPE")

        if performance_metrics.get("Annual Return", 0) < ssm.get("target_metrics", {}).get("annualized_return", {}).get("value",
                                                                                                               0.10):
            defects.append("INSUFFICIENT_RETURN")

        if performance_metrics.get("Annualized Volatility", 0) > 0.25:
            defects.append("HIGH_VOLATILITY")

        if performance_metrics.get("Daily Win Rate", 0) < 0.45:
            defects.append("POOR_WIN_RATE")

        # 基于压力测试结果识别缺陷
        for scenario_name, result in stress_test_results.items():
            if result.get("estimated_loss", 0) > 0.20:
                defects.append("TAIL_RISK")
                break

        # 基于合规性检查识别缺陷
        if not compliance_check.get("overall_compliance", False):
            # 根据具体未满足的要求添加相应缺陷
            pass

        # 去重
        return list(set(defects))

    def _generate_evaluation_report(self, performance_metrics: Dict[str, Any],
                                    stress_test_results: Dict[str, Any],
                                    compliance_check: Dict[str, Any],
                                    defects: List[str]) -> Dict[str, Any]:
        """生成评估报告"""
        report = {
            "summary": {
                "overall_score": self._calculate_overall_score(
                    performance_metrics, stress_test_results, defects
                ),
                "key_strengths": self._identify_strengths(performance_metrics),
                "key_weaknesses": [self.defect_categories.get(d, d) for d in defects],
                "recommendation": self._generate_recommendation(defects, performance_metrics)
            },
            "detailed_metrics": performance_metrics,
            "stress_test_summary": {
                "scenarios_tested": len(stress_test_results),
                "worst_case_loss": max(
                    r.get("estimated_loss", 0) for r in stress_test_results.values()
                ) if stress_test_results else 0,
                "average_recovery_time": np.mean([
                    r.get("recovery_time", 0) for r in stress_test_results.values()
                ]) if stress_test_results else 0
            },
            "compliance_summary": {
                "meets_all_requirements": compliance_check.get("overall_compliance", False),
                "failed_requirements": [
                    k for k, v in compliance_check.get("target_metrics", {}).items()
                    if not v.get("meets_requirement", False)
                ]
            }
        }

        return report

    def _calculate_overall_score(self, performance_metrics: Dict[str, Any],
                                 stress_test_results: Dict[str, Any],
                                 defects: List[str]) -> float:
        """计算总体评分"""
        score = 100.0

        # 基于缺陷扣分
        score -= len(defects) * 10

        # 基于性能指标调整
        sharpe = performance_metrics.get("Sharpe Ratio", 0)
        if sharpe > 2.0:
            score += 10
        elif sharpe < 1.0:
            score -= 10

        # 基于压力测试结果调整
        if stress_test_results:
            worst_loss = max(r.get("estimated_loss", 0) for r in stress_test_results.values())
            if worst_loss > 0.30:
                score -= 20
            elif worst_loss < 0.10:
                score += 10

        return max(0, min(100, score))

    def _identify_strengths(self, performance_metrics: Dict[str, Any]) -> List[str]:
        """识别策略优势"""
        strengths = []

        if performance_metrics.get("Sharpe Ratio", 0) > 1.5:
            strengths.append("优秀的风险调整收益")

        if performance_metrics.get("Maximum Drawdown", 1) < 0.10:
            strengths.append("良好的下行风险控制")

        if performance_metrics.get("Daily Win Rate", 0) > 0.55:
            strengths.append("稳定的盈利能力")

        if performance_metrics.get("Calmar Ratio", 0) > 2.0:
            strengths.append("优秀的回撤收益比")

        return strengths

    def _generate_recommendation(self, defects: List[str],
                                 performance_metrics: Dict[str, Any]) -> str:
        """生成改进建议"""
        if not defects:
            return "策略表现优秀，建议保持当前配置并持续监控。"

        recommendations = []

        if "EXCESSIVE_DRAWDOWN" in defects:
            recommendations.append("考虑增加防御性资产或实施止损机制")

        if "LOW_SHARPE" in defects:
            recommendations.append("优化资产配置以提高风险调整收益")

        if "INSUFFICIENT_RETURN" in defects:
            recommendations.append("考虑增加高alpha因子或提高风险预算")

        if "HIGH_VOLATILITY" in defects:
            recommendations.append("增加低波动性资产或使用波动率目标策略")

        return "；".join(recommendations) + "。"

    def _run_comprehensive_backtest(self, weights: pd.DataFrame,
                                    symbols: List[str]) -> Dict[str, Any]:
        """运行全面回测"""

        # 简化示例
        results = {
            "Annual Return": 0.15,
            "Sharpe ratio": 1.5,
            "Maximum drawdown": 0.12,
            "Daily win rate": 0.52,
            "Calmar ratio": 1.25,
            "Annualized Volatility": 0.18,
            "Downside Volatility": 0.12,
            "Non-zero Coverage": 0.85
        }

        return results

    def _extract_portfolio_metrics(self, portfolio) -> Dict[str, Any]:
        """从portfolio对象提取指标"""
        if portfolio is None:
            return {}

        try:
            return {
                "Annual Return": getattr(portfolio, 'annualized_mean', 0),
                "Sharpe Ratio": getattr(portfolio, 'annualized_sharpe_ratio', 0),
                "Maximum Drawdown": getattr(portfolio, 'max_drawdown', 0),
                "Annualized Volatility": getattr(portfolio, 'annualized_standard_deviation', 0),
                "Calmar Ratio": getattr(portfolio, 'calmar_ratio', 0)
            }
        except:
            return {}