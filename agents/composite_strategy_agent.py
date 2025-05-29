
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from loguru import logger
from agents.base_agent import BaseAgent, Message, MessageType

from config.system_config import SystemConfig
from config.system_config import PromptTemplates
from llm.llm_client import OpenRouterClient


class CompositeStrategyAgent(BaseAgent):
    """复合策略智能体 - 负责筛选和组合子策略"""

    def __init__(self, name: str, llm_client: OpenRouterClient, config: SystemConfig):
        super().__init__(name, llm_client, config)

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return PromptTemplates.composite_system_prompt()

    def process_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.type == MessageType.COMPOSITE_REQUEST:
            return self._handle_composite_request(message)
        return None

    def _handle_composite_request(self, message: Message) -> Message:
        """处理复合策略请求"""
        try:
            # 提取数据
            factor_returns_dict = message.content.get("factor_returns", {})
            factor_metrics_dict = message.content.get("factor_metrics", {})
            config = message.content.get("config", {})
            ssm = message.content.get("ssm", {})

            # 转换为DataFrame
            factor_returns = pd.DataFrame(factor_returns_dict)
            factor_metrics = pd.DataFrame(factor_metrics_dict)

            # Stage 1: 稳定性和有效性筛选
            logger.info("Stage 1: Stability and validity filtering...")
            stable_factors = self._stability_filtering(factor_metrics, config)

            # Stage 2: 基于SSM的多指标排序
            logger.info("Stage 2: SSM-aligned multi-metric ranking...")
            selected_strategies = self._multi_metric_ranking(
                factor_metrics,
                factor_returns,
                stable_factors,
                config,
                ssm
            )

            # 准备返回的因子收益数据
            selected_factor_names = []
            for strategy_name, factors in selected_strategies.items():
                selected_factor_names.extend(factors)

            selected_factor_names = list(set(selected_factor_names))
            filtered_factor_returns = factor_returns[['dt'] + selected_factor_names]

            # 生成策略组合报告
            report = self._generate_composite_report(selected_strategies, factor_metrics)

            return self.send_message(
                receiver=message.sender,
                type=MessageType.COMPOSITE_RESULT,
                content={
                    "selected_strategies": selected_strategies,
                    "filtered_factor_returns": filtered_factor_returns,
                    "composite_report": report,
                    "num_strategies": len(selected_strategies),
                    "total_factors": len(selected_factor_names)
                }
            )

        except Exception as e:
            logger.error(f"Error in composite strategy generation: {str(e)}")
            return self.send_message(
                receiver=message.sender,
                type=MessageType.ERROR,
                content={"error": str(e)}
            )

    def _stability_filtering(self, factor_metrics: pd.DataFrame,
                             config: Dict[str, Any]) -> List[str]:
        """Stage 1: 稳定性和有效性筛选"""
        stability_filters = config.get("stability_filters", {})

        # 默认筛选条件
        min_sharpe = stability_filters.get("min_sharpe", 0.5)
        max_drawdown = stability_filters.get("max_drawdown", 0.20)
        min_win_rate = stability_filters.get("min_win_rate", 0.45)
        min_calmar = stability_filters.get("min_calmar", 0.5)

        # 应用筛选条件
        stable_mask = (
                (factor_metrics['夏普'] >= min_sharpe) &
                (factor_metrics['最大回撤'] <= max_drawdown) &
                (factor_metrics['日胜率'] >= min_win_rate) &
                (factor_metrics['卡玛'] >= min_calmar)
        )

        # 额外的统计可靠性检查
        # 检查是否有异常的收益率
        stable_mask &= (factor_metrics['年化'] <= 2.0)  # 年化收益不超过200%
        stable_mask &= (factor_metrics['年化'] >= -0.5)  # 年化亏损不超过50%

        stable_factors = factor_metrics[stable_mask]['factor'].tolist()

        logger.info(f"Stability filtering: {len(stable_factors)}/{len(factor_metrics)} factors passed")

        return stable_factors

    def _multi_metric_ranking(self, factor_metrics: pd.DataFrame,
                              factor_returns: pd.DataFrame,
                              stable_factors: List[str],
                              config: Dict[str, Any],
                              ssm: Dict[str, Any]) -> Dict[str, List[str]]:
        """Stage 2: 基于SSM的多指标排序"""
        # 只考虑稳定的因子
        metrics_df = factor_metrics[factor_metrics['factor'].isin(stable_factors)].copy()

        if metrics_df.empty:
            logger.warning("No stable factors found, returning empty strategies")
            return {}

        # 获取排序权重
        ranking_weights = config.get("ranking_weights", {
            "sharpe": 0.3,
            "calmar": 0.2,
            "annual_return": 0.3,
            "win_rate": 0.2
        })

        # 使用LLM动态调整策略组合
        strategies = self._generate_strategy_combinations(
            metrics_df,
            factor_returns,
            ranking_weights,
            config,
            ssm
        )

        return strategies

    def _generate_strategy_combinations(self, metrics_df: pd.DataFrame,
                                        factor_returns: pd.DataFrame,
                                        ranking_weights: Dict[str, float],
                                        config: Dict[str, Any],
                                        ssm: Dict[str, Any]) -> Dict[str, List[str]]:
        """使用LLM生成策略组合"""
        prompt = f"""
        Based on the SSM requirements and factor metrics, please design strategy combinations.

        SSM Requirements:
        - Target Return: {ssm.get('target_metrics', {}).get('annualized_return', {})}
        - Risk Constraints: {ssm.get('risk_constraints', {})}

        Available Factors: {len(metrics_df)}

        Top performing factors by different metrics:
        - By Sharpe: {metrics_df.nlargest(5, '夏普')['factor'].tolist()}
        - By Annual Return: {metrics_df.nlargest(5, '年化')['factor'].tolist()}
        - By Calmar: {metrics_df.nlargest(5, '卡玛')['factor'].tolist()}
        - By Win Rate: {metrics_df.nlargest(5, '日胜率')['factor'].tolist()}

        Please suggest multiple strategy combinations that:
        1. Balance risk and return according to SSM
        2. Ensure diversification (low correlation between factors)
        3. Include both aggressive and defensive strategies

        Respond with strategy names and selection criteria:
        {{
            "high_sharpe": {{"metric": "夏普", "top_n": 20, "strategy_type": "risk_adjusted"}},
            "high_return": {{"metric": "年化", "top_n": 20, "strategy_type": "aggressive"}},
            "balanced": {{"metrics": ["夏普", "卡玛"], "weights": [0.5, 0.5], "top_n": 30, "strategy_type": "balanced"}},
            "defensive": {{"metrics": ["最大回撤", "日胜率"], "weights": [-1, 1], "top_n": 20, "strategy_type": "defensive"}}
        }}
        """

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            model=self.config.models["composite_agent"],
            temperature=self.config.llm_config["temperature"]
        )

        strategy_specs = self.llm_client.parse_json_response(response.content)

        # 执行策略选择
        strategies = {}
        correlation_threshold = config.get("correlation_threshold", 0.7)

        for strategy_name, spec in strategy_specs.items():
            if "metric" in spec:
                # 单指标策略
                candidates = self._filter_factors(
                    metrics_df,
                    spec["metric"],
                    spec.get("top_n", 20),
                    ascending=spec.get("ascending", False)
                )
            else:
                # 多指标策略
                candidates = self._multi_metric_filter(
                    metrics_df,
                    spec.get("metrics", []),
                    spec.get("weights", []),
                    spec.get("top_n", 30)
                )

            # 相关性过滤
            selected = self._correlation_filter(
                candidates,
                min(spec.get("top_n", 20) // 2, len(candidates)),
                factor_returns,
                correlation_threshold
            )

            if len(selected) >= 3:  # 至少需要3个因子
                strategies[strategy_name] = selected
                logger.info(f"Strategy '{strategy_name}' selected {len(selected)} factors")

        return strategies

    def _filter_factors(self, metrics_df: pd.DataFrame, column_name: str,
                        n_factors: int, ascending: bool = False) -> List[str]:
        """基于单一指标筛选因子"""
        if column_name not in metrics_df.columns:
            logger.warning(f"Column '{column_name}' not found")
            return []

        sorted_df = metrics_df.sort_values(by=column_name, ascending=ascending)
        n_factors = min(n_factors, len(sorted_df))

        return sorted_df.head(n_factors)['factor'].tolist()

    def _multi_metric_filter(self, metrics_df: pd.DataFrame, metrics: List[str],
                             weights: List[float], n_factors: int) -> List[str]:
        """基于多指标加权筛选因子"""
        df_score = metrics_df.copy()

        # 计算每个指标的排名
        for i, metric in enumerate(metrics):
            if metric in df_score.columns:
                weight = weights[i] if i < len(weights) else 1.0
                if weight < 0:
                    # 负权重表示越小越好
                    df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=True)
                else:
                    df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=False)
                df_score[f'{metric}_rank'] *= abs(weight)

        # 计算总分
        rank_columns = [col for col in df_score.columns if col.endswith('_rank')]
        df_score['total_score'] = df_score[rank_columns].sum(axis=1)

        # 选择得分最高的因子
        df_score = df_score.sort_values('total_score', ascending=True)
        n_factors = min(n_factors, len(df_score))

        return df_score.head(n_factors)['factor'].tolist()

    def _correlation_filter(self, candidate_factors: List[str], target_n: int,
                            factor_returns: pd.DataFrame,
                            max_correlation: float = 0.7) -> List[str]:
        """相关性过滤确保分散化"""
        if len(candidate_factors) == 0:
            return []

        # 确保有日期列
        if 'dt' in factor_returns.columns:
            factor_returns = factor_returns.set_index('dt')

        selected = [candidate_factors[0]]

        for factor in candidate_factors[1:]:
            if len(selected) >= target_n:
                break

            # 检查与已选因子的相关性
            is_correlated = False

            if factor in factor_returns.columns:
                factor_returns_series = factor_returns[factor]

                for sel_factor in selected:
                    if sel_factor in factor_returns.columns:
                        correlation = factor_returns_series.corr(factor_returns[sel_factor])
                        if abs(correlation) >= max_correlation:
                            is_correlated = True
                            break

                if not is_correlated:
                    selected.append(factor)

        return selected

    def _generate_composite_report(self, selected_strategies: Dict[str, List[str]],
                                   factor_metrics: pd.DataFrame) -> Dict[str, Any]:
        """生成复合策略报告"""
        report = {
            "strategy_count": len(selected_strategies),
            "total_factors": sum(len(factors) for factors in selected_strategies.values()),
            "strategies": {}
        }

        for strategy_name, factors in selected_strategies.items():
            strategy_metrics = factor_metrics[factor_metrics['factor'].isin(factors)]

            report["strategies"][strategy_name] = {
                "factor_count": len(factors),
                "avg_sharpe": strategy_metrics['夏普'].mean(),
                "avg_return": strategy_metrics['年化'].mean(),
                "avg_drawdown": strategy_metrics['最大回撤'].mean(),
                "avg_win_rate": strategy_metrics['日胜率'].mean(),
                "factors": factors
            }

        return report