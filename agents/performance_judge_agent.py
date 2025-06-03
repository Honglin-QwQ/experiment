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


            # 执行全面评估
            logger.info("Performing comprehensive evaluation...")

            # 1. 基础性能评估
            # performance_metrics = self._evaluate_basic_performance(strategy, symbols)
            performance_metrics = self._evaluate_basic_performance(strategy)


            # 3. SSM合规性检查
            compliance_check = self._check_ssm_compliance(performance_metrics, ssm)

            # 4. 识别缺陷
            defects = self._identify_defects(
                performance_metrics,
                compliance_check,
                ssm
            )

            # 5. 生成评估报告
            evaluation_report = self._generate_evaluation_report(
                performance_metrics,
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



        # 基于合规性检查识别缺陷
        if not compliance_check.get("overall_compliance", False):
            # 根据具体未满足的要求添加相应缺陷
            pass

        # 去重
        return list(set(defects))

    def _generate_evaluation_report(self, performance_metrics: Dict[str, Any],

                                    compliance_check: Dict[str, Any],
                                    defects: List[str]) -> Dict[str, Any]:
        """生成评估报告"""
        report = {
            "summary": {
                "overall_score": self._calculate_overall_score(
                    performance_metrics, defects
                ),
                "key_strengths": self._identify_strengths(performance_metrics),
                "key_weaknesses": [self.defect_categories.get(d, d) for d in defects],
                "recommendation": self._generate_recommendation(defects, performance_metrics)
            },
            "detailed_metrics": performance_metrics,

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
            recommendations.append("考虑增加更多低回测低波动率的因子")

        if "LOW_SHARPE" in defects:
            recommendations.append("考虑增加更多高夏普的因子")

        if "INSUFFICIENT_RETURN" in defects:
            recommendations.append("考虑增加更多高年华的因子")

        if "HIGH_VOLATILITY" in defects:
            recommendations.append("增加低波动性因子")

        return "；".join(recommendations) + "。"



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