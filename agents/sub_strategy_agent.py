
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from loguru import logger
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from agents.base_agnet import BaseAgent, Message, MessageType

from config.system_config import SystemConfig, MarketType
from config.system_config import PromptTemplates
from llm.llm_client import OpenRouterClient


class SubStrategyAgent(BaseAgent):
    """子策略智能体 - 负责因子处理和子策略生成"""

    def __init__(self, name: str, llm_client: OpenRouterClient, config: SystemConfig,
                 factor_calculator, backtest_system):
        super().__init__(name, llm_client, config)
        self.factor_calculator = factor_calculator
        self.backtest_system = backtest_system
        self.normalization_methods = {
            'z-score': StandardScaler(),
            'min-max': MinMaxScaler(),
            'robust': RobustScaler(),
            'percentile': lambda: RobustScaler(quantile_range=(5.0, 95.0))
        }

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return PromptTemplates.sub_strategy_system_prompt()

    def process_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.type == MessageType.SUB_STRATEGY_REQUEST:
            return self._handle_sub_strategy_request(message)
        return None

    def _handle_sub_strategy_request(self, message: Message) -> Message:
        """处理子策略请求"""
        try:
            ssm = message.content.get("ssm", {})
            market_type = message.content.get("market_type", "US_EQUITIES")
            iteration = message.content.get("iteration", 0)
            refinement = message.content.get("refinement", {})

            # 计算因子值
            logger.info("Calculating factor values...")
            self.factor_calculator.cal_factor()
            # 因子反转
            self.factor_calculator.reverse_factor()
            factor_df =self.factor_calculator.factor_result



            if factor_df is None or factor_df.empty:
                raise ValueError("Failed to calculate factors")




            # 使用LLM决定归一化方法
            normalization_method = self._determine_normalization_method(
                ssm, market_type, factor_df, iteration, refinement
            )

            # 应用归一化
            logger.info(f"Applying {normalization_method} normalization...")
            normalized_df = self._apply_normalization(factor_df, normalization_method)


            # 计算因子收益
            logger.info("Calculating factor returns...")
            factor_returns = self._calculate_factor_returns(normalized_df)

            # 回测所有因子
            logger.info("Backtesting factors...")
            factor_metrics = self._backtest_factors(normalized_df)

            # 返回结果
            return self.send_message(
                receiver=message.sender,
                type=MessageType.SUB_STRATEGY_RESULT,
                content={
                    "sub_strategies": self._format_sub_strategies(factor_metrics),
                    "factor_returns": factor_returns,
                    "factor_metrics": factor_metrics,
                    "normalization_method": normalization_method,
                }
            )

        except Exception as e:
            logger.error(f"Error in sub-strategy generation: {str(e)}")
            return self.send_message(
                receiver=message.sender,
                type=MessageType.ERROR,
                content={"error": str(e)}
            )

    def _determine_normalization_method(self, ssm: Dict[str, Any], market_type: str,
                                        factor_df: pd.DataFrame, iteration: int,
                                        refinement: Dict[str, Any]) -> str:
        """使用LLM决定归一化方法"""
        prompt = f"""
        Please determine the optimal normalization method for factor values based on the following context:

        Market Type: {market_type}
        SSM Requirements:
        - Target Metrics: {ssm.get('target_metrics', {})}
        - Risk Constraints: {ssm.get('risk_constraints', {})}

        Data Statistics:
        - Number of factors: {len([col for col in factor_df.columns if col.startswith('F#')])}
        - Data points: {len(factor_df)}
        - Has negative values: {any(factor_df.select_dtypes(include=[np.number]).values.flatten() < 0)}

        Iteration: {iteration}
        Refinement Instructions: {refinement}

        Available normalization methods:
        1. z-score: Standardization (mean=0, std=1) - suitable for markets allowing short selling
        2. min-max: Scale to [0,1] - suitable for long-only strategies
        3. robust: Robust scaling using median and IQR - suitable for data with outliers
        4. percentile: Percentile-based scaling - suitable for non-normal distributions

        Consider:
        - For A-shares market, avoid negative weights (no short selling)
        - For US equities/futures, negative weights are acceptable
        - Factor distribution characteristics
        - Outlier sensitivity

        Please respond with just the method name (z-score/min-max/robust/percentile):
        """

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            model=self.config.models["sub_strategy_agent"],
            temperature=0.3
        )

        method = response.content.strip().lower()
        if method not in self.normalization_methods:
            logger.warning(f"Invalid normalization method: {method}, defaulting to z-score")
            method = "z-score"

        return method

    def _apply_normalization(self, df: pd.DataFrame, method: str) -> pd.DataFrame:
        """应用归一化"""
        df_copy = df.copy()
        factor_cols = [col for col in df.columns if col.startswith('F#')]

        if method in self.normalization_methods:
            scaler = self.normalization_methods[method]
            if callable(scaler):
                scaler = scaler()

            # 按时间截面归一化
            def normalize_cross_section(group):
                if len(group) > 1:
                    group[factor_cols] = scaler.fit_transform(group[factor_cols])
                return group

            df_copy = df_copy.groupby('dt').apply(normalize_cross_section)

        return df_copy



    def _calculate_factor_returns(self, weights_df: pd.DataFrame) -> pd.DataFrame:
        """计算因子收益"""

        factor_returns = self.factor_calculator.calculate_factor_returns_blocked(
            df=weights_df,
            n_jobs=self.config.backtest_config["n_jobs"],
            current_frequency='4h',
            split_time=pd.to_datetime('2024-01-01')
        )

        return factor_returns

    def _backtest_factors(self, weights_df: pd.DataFrame) -> pd.DataFrame:
        """回测所有因子"""

        self.factor_meric = self.factor_calculator.evaluate_factor_blocked(
            weights_df, n_jobs=self.config.backtest_config["n_jobs"],
            current_frequency='4h'
        )

        return self.factor_meric



    def _format_sub_strategies(self, factor_metrics: pd.DataFrame) -> Dict[str, Any]:
        """格式化子策略结果"""
        strategies = {}

        for _, row in factor_metrics.iterrows():
            factor_name = row['factor']
            strategies[factor_name] = {
                'annual_return': row.get('年化', 0),
                'sharpe_ratio': row.get('夏普', 0),
                'max_drawdown': row.get('最大回撤', 0),
                'win_rate': row.get('日胜率', 0),
                'calmar_ratio': row.get('卡玛', 0)
            }

        return strategies
