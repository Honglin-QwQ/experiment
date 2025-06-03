import json
import re
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from loguru import logger
from agents.base_agent import BaseAgent, Message, MessageType

from config.system_config import SystemConfig
from config.system_config import PromptTemplates
from llm.llm_client import OpenRouterClient, parse_json_response


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
        max_drawdown = stability_filters.get("max_drawdown", 0.30)
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


        # 使用LLM动态调整策略组合
        strategies = self._generate_strategy_combinations(
            metrics_df,
            factor_returns,
            config,
            ssm
        )

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
            json_content = json_content.replace("(", "[").replace(")", "]")
            # 2. 替换独立的false为"false"（后面会转回Python的False）
            json_content = json_content.replace("False", "false")
            json_content = json_content.replace("True", "true")
            # 将JSON字符串转换为Python字典
            rules_dict = json.loads(json_content)

            # 将filtering_rules中的列表转换为元组
            rules_dict['filtering_rules'] = [
                tuple(rule) for rule in rules_dict['filtering_rules']
            ]

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
    def _generate_strategy_combinations(self, metrics_df: pd.DataFrame,
                                        factor_returns: pd.DataFrame,

                                        config: Dict[str, Any],
                                        ssm: Dict[str, Any]) -> Dict[str, List[str]]:
        """使用LLM生成策略组合"""

        # 第一步：让LLM生成筛选规则
        prompt = f"""Based on the SSM requirements and available metrics, generate factor filtering rules.

        SSM Requirements:
        - Target Return: {ssm.get('target_metrics', {}).get('annualized_return', {})}
        - Risk Constraints: {ssm.get('risk_constraints', {})}
        - Investment Philosophy: {ssm.get('investment_philosophy', 'balanced')}

        Available Metrics in factor_metrics_df:
        - Annualized Return (年化收益率)
        - Sharpe Ratio (夏普比率)
        - Calmar Ratio (卡玛比率)
        - Maximum Drawdown (最大回撤)
        - Daily Win Rate (日胜率)
        - Single Profit (单笔收益)
        - Daily Win Facet (日赢面)
        - New High Percentage (新高占比)
        - New High Interval (新高间隔)
        - Downside Volatility (下行波动率)
        - Daily P/L Ratio (日盈亏比)
        - Annualized Volatility (年化波动率)
        - Trading Win Rate (交易胜率)
        - Holding Time (持仓K线数)
        - Long Percentage (多头占比)
        - Short Percentage (空头占比)
        

        Please generate filtering rules in the following format (JSON format):
        {{
            "filtering_rules": [
                ("strategy_name", "primary_metric", n_factors, n2_factors, ascending),
                ("high20_sharpe", "Sharpe Ratio", 5, 0, false),
                ("high20_return", "Annualized Return", 5, 0, false),
                ("balanced_risk_return", "balance_strategy", 5, 0, false),
                ("multi_dim_alpha", "multi_dimensional_strategy", 5, 0, false)
            ],
            "balance_strategies": {{
                "balanced_risk_return": {{
                    "metrics": ["Sharpe Ratio", "Daily Win Facet", "Maximum Drawdown"],
                    "weights": [0.4, 0.5, 0.3],
                    "ascending": [false, false, true]
                }}
            }},
            "multi_dim_strategies": {{
                "multi_dim_alpha": {{
                    "positive_metrics": ["Annual Return", "Sharpe Ratio", "Single Profit"],
                    "negative_metrics": ["Maximum Drawdown", "Downside Volatility"],
                    "weights": {{
                        "Annual Return": 1.0,
                        "Sharpe Ratio": 1.0,
                        "Single Profit": 1.0,
                        "Maximum Drawdown": 1.0,
                        "Downside Volatility": 1.0
                    }}
                }}
            }}
        }}

        Guidelines:
        1. Create at least 6-8 different strategies
        2. Include both single-metric and multi-metric strategies
        3. For balanced strategies, use "balance_strategy" as the metric
        4. For multi-dimensional strategies, use "multi_dimensional_strategy" as the metric
        5. n2_factors is used for difference set filtering (if n2_factors > 0, select top n_factors minus top n2_factors)
        6. Consider the SSM requirements when setting weights and selecting metrics
        7. For balance_strategy and multi_dimensional_strategy that appear in filtering_rules, specific definitions must be given in balance_strategies and multi_dim_strategies, and strategy_name needs to correspond correctly.
        """

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            model=self.config.models["composite_agent"],
            temperature=self.config.llm_config["temperature"],
            max_tokens=10000,
        )

        strategy_config = self.load_factor_rules(response.content)

        if strategy_config=={}:
            logger.error(f"Failed to parse LLM response")

            strategy_config = self._get_default_strategy_config()

        # 第二步：执行筛选规则
        strategies = {}
        filtering_rules = strategy_config.get("filtering_rules", [])
        balance_strategies = strategy_config.get("balance_strategies", {})
        multi_dim_strategies = strategy_config.get("multi_dim_strategies", {})

        for rule in filtering_rules:
            strategy_name, column_name, n_factors, n2_factors, ascending = rule

            try:
                if column_name == "balance_strategy":
                    # 执行平衡策略
                    selected_factors = self._execute_balance_strategy(
                        metrics_df,
                        strategy_name,
                        n_factors,
                        factor_returns,
                        balance_strategies.get(strategy_name, {})
                    )
                elif column_name == "multi_dimensional_strategy":
                    # 执行多维度策略
                    selected_factors = self._execute_multi_dim_strategy(
                        metrics_df,
                        strategy_name,
                        n_factors,
                        factor_returns,
                        multi_dim_strategies.get(strategy_name, {})
                    )
                else:
                    # 执行单指标筛选
                    if n2_factors == 0:
                        candidate_factors = self._filter_factors(
                            metrics_df, column_name, len(metrics_df), ascending
                        )
                        selected_factors = self._correlation_filter(
                            candidate_factors, n_factors, factor_returns,
                            config.get("correlation_threshold", 0.7)
                        )
                    else:
                        # 差集筛选
                        candidate_factors = self._filter_factors(
                            metrics_df, column_name, len(metrics_df), ascending
                        )
                        selected_factors1 = self._correlation_filter(
                            candidate_factors, n_factors, factor_returns,
                            config.get("correlation_threshold", 0.7)
                        )
                        selected_factors2 = self._correlation_filter(
                            candidate_factors, n2_factors, factor_returns,
                            config.get("correlation_threshold", 0.7)
                        )
                        selected_factors = list(set(selected_factors1) - set(selected_factors2))

                if len(selected_factors) >= 3:
                    strategies[strategy_name] = selected_factors
                    logger.info(f"Strategy '{strategy_name}' selected {len(selected_factors)} factors")
                else:
                    logger.warning(f"Strategy '{strategy_name}' selected too few factors: {len(selected_factors)}")

            except Exception as e:
                logger.error(f"Error executing strategy '{strategy_name}': {e}")
                continue

        return strategies

    def _execute_balance_strategy(self, metrics_df: pd.DataFrame,
                                  strategy_name: str, n_factors: int,
                                  factor_returns: pd.DataFrame,
                                  strategy_config: Dict[str, Any]) -> List[str]:
        """执行平衡策略"""
        df_score = metrics_df.copy()

        # 获取策略配置
        metrics = strategy_config.get("metrics", ["Sharpe Ratio", "Annual Return", "Maximum Drawdown"])
        weights = strategy_config.get("weights", [0.33, 0.33, 0.34])
        ascending_list = strategy_config.get("ascending", [False, False, True])

        # 计算每个指标的排名
        total_weight = 0
        for i, (metric, weight, ascending) in enumerate(zip(metrics, weights, ascending_list)):
            if metric in df_score.columns:
                df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=ascending)
                df_score[f'{metric}_rank'] *= weight
                total_weight += weight

        # 计算总得分
        rank_columns = [col for col in df_score.columns if col.endswith('_rank')]
        if rank_columns:
            df_score['total_score'] = df_score[rank_columns].sum(axis=1) / total_weight
        else:
            df_score['total_score'] = 0

        # 选择得分最高的因子
        top_factors = df_score.sort_values('total_score').head(int(n_factors * 10))['factor'].tolist()

        return self._correlation_filter(top_factors, n_factors, factor_returns, 0.7)

    def _execute_multi_dim_strategy(self, metrics_df: pd.DataFrame,
                                    strategy_name: str, n_factors: int,
                                    factor_returns: pd.DataFrame,
                                    strategy_config: Dict[str, Any]) -> List[str]:
        """执行多维度策略"""
        df_score = metrics_df.copy()

        # 获取策略配置
        positive_metrics = strategy_config.get("positive_metrics", ["Annual Return", "Sharpe Ratio"])
        negative_metrics = strategy_config.get("negative_metrics", ["Maximum Drawdown"])
        weights = strategy_config.get("weights", {})

        # 对正向指标进行排名（越高越好）
        for metric in positive_metrics:
            if metric in df_score.columns:
                df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=False)
                # 应用权重
                if metric in weights:
                    df_score[f'{metric}_rank'] *= weights[metric]

        # 对负向指标进行排名（越低越好）
        for metric in negative_metrics:
            if metric in df_score.columns:
                df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=True)
                # 应用权重
                if metric in weights:
                    df_score[f'{metric}_rank'] *= weights[metric]

        # 计算综合得分
        rank_columns = [col for col in df_score.columns if col.endswith('_rank')]
        if rank_columns:
            df_score['total_score'] = df_score[rank_columns].sum(axis=1)
        else:
            df_score['total_score'] = 0

        # 选择得分最高的因子
        df_score = df_score.sort_values('total_score')
        top_factors = df_score['factor'].head(int(n_factors * 10)).tolist()

        return self._correlation_filter(top_factors, n_factors, factor_returns, 0.7)

    def _get_default_strategy_config(self) -> Dict[str, Any]:
        """获取默认策略配置"""
        return {
            "filtering_rules": [
                ["high20_sharpe", "Sharpe Ratio", 20, 0, False],
                ["high20_return", "Annual Return", 20, 0, False],
                ["high20_单笔收益", "单笔收益", 20, 0, False],
                ["high20_日赢面", "日赢面", 20, 0, False],
                ["balanced_收益风险", "balance_strategy", 30, 0, False],
                ["multi_dim_alpha", "multi_dimensional_strategy", 20, 0, False],
                ["multi_dim_stable", "multi_dimensional_strategy", 20, 0, False],
                ["balanced_stable_高收益", "balance_strategy", 30, 0, False],
            ],
            "balance_strategies": {
                "balanced_收益风险": {
                    "metrics": ["Sharpe Ratio", "日赢面", "Maximum Drawdown"],
                    "weights": [0.4, 0.5, 0.3],
                    "ascending": [False, False, True]
                },
                "balanced_stable_高收益": {
                    "metrics": ["Maximum Drawdown", "Annual Return", "单笔收益"],
                    "weights": [0.3, 0.5, 0.5],
                    "ascending": [True, False, False]
                }
            },
            "multi_dim_strategies": {
                "multi_dim_alpha": {
                    "positive_metrics": ["Annual Return", "Sharpe Ratio", "单笔收益"],
                    "negative_metrics": ["Maximum Drawdown", "Downside Volatility"],
                    "weights": {
                        "Annual Return": 1.0,
                        "Sharpe Ratio": 1.0,
                        "单笔收益": 1.0,
                        "Maximum Drawdown": 1.0,
                        "Downside Volatility": 1.0
                    }
                },
                "multi_dim_stable": {
                    "positive_metrics": ["Sharpe Ratio", "Daily Win Rate", "新高占比", "Annual Return"],
                    "negative_metrics": ["Maximum Drawdown", "新高间隔"],
                    "weights": {
                        "Sharpe Ratio": 1.0,
                        "Daily Win Rate": 1.0,
                        "新高占比": 1.0,
                        "Annual Return": 1.0,
                        "Maximum Drawdown": 1.0,
                        "新高间隔": 1.0
                    }
                }
            }
        }

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