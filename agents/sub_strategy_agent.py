import json
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from loguru import logger
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

from experiment import calculate_factor_returns_blocked, normalize_column_parallel_blocked

from scipy import stats
from agents.base_agent import BaseAgent, Message, MessageType
from config.system_config import SystemConfig, MarketType
from config.system_config import PromptTemplates
from llm.llm_client import OpenRouterClient
from llm.llm_client import parse_json_response


class SubStrategyAgent(BaseAgent):
    """子策略智能体 - 负责因子处理和子策略生成"""

    def __init__(self, name: str, llm_client: OpenRouterClient, config: SystemConfig,
                 factor_calculator, backtest_system):
        super().__init__(name, llm_client, config)
        self.factor_calculator = factor_calculator
        self.backtest_system = backtest_system

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
            factor_df = self.factor_calculator.factor_result

            if factor_df is None or factor_df.empty:
                raise ValueError("Failed to calculate factors")

            # 使用LLM决定归一化方法
            normalization_config = self._determine_normalization_method(
                ssm, market_type, factor_df, iteration, refinement
            )

            # 应用归一化
            factor_cols=[f for f in factor_df.columns if f.startswith("F#")]
            logger.info(f"Applying {normalization_config['method']} normalization...")


            weights_df = normalize_column_parallel_blocked(
                factor_df, factor_cols, method=normalization_config['method'],
                n_jobs=self.factor_calculator.n_jobs, current_frequency=self.factor_calculator.frequency
            )

            # 计算因子收益
            logger.info("Calculating factor returns...")
            factor_returns = self._calculate_factor_returns(weights_df)

            # 回测所有因子
            logger.info("Backtesting factors...")
            factor_metrics = self._backtest_factors(weights_df)

            # 返回结果
            return self.send_message(
                receiver=message.sender,
                type=MessageType.SUB_STRATEGY_RESULT,
                content={
                    "sub_strategies": self._format_sub_strategies(factor_metrics),
                    "factor_returns": factor_returns,
                    "factor_metrics": factor_metrics,
                    "normalization_config": normalization_config,
                    "weights_df": weights_df,
                }
            )

        except Exception as e:
            logger.error(f"Error in sub-strategy generation: {str(e)}")
            return self.send_message(
                receiver=message.sender,
                type=MessageType.ERROR,
                content={"error": str(e)}
            )

    def _validate_config_method(self, config, logger, default_method="zscore"):
        valid_methods = [
            "zscore", "zscore_clip", "zscore_maxmin", "max_min", "sum",
            "rank_s", "rank_balanced", "rank_c", "long_only_zscore", "long_only_softmax"
        ]
        if config.get("method") not in valid_methods:
            logger.warning(f"Invalid method: {config.get('method')}, defaulting to {default_method}")
            config["method"] = default_method
        return config


    def get_default_config(self, market_type):
        if market_type == "A_SHARES":
            return {
                "method": "long_only_zscore",
                "params": {"winsorize": True, "q": 0.05},
                "reasoning": "Default for A-shares market"
            }
        else:
            return {
                "method": "zscore",
                "params": {"winsorize": True, "q": 0.05},
                "reasoning": "Default for other markets"
            }


    def _determine_normalization_method(self, ssm: Dict[str, Any], market_type: str,
                                        factor_df: pd.DataFrame, iteration: int,
                                        refinement: Dict[str, Any]) -> Dict[str, Any]:
        """使用LLM决定归一化方法和参数"""
        prompt = f"""
        You are determining the optimal method to convert factor values into portfolio weights.

        Context:
        - Market Type: {market_type}
        - Target Metrics: {ssm.get('target_metrics', {})}
        - Risk Constraints: {ssm.get('risk_constraints', {})}
        - Number of factors: {len([col for col in factor_df.columns if col.startswith('F#')])}
        - Data points: {len(factor_df)}
        - Iteration: {iteration}
        - Refinement: {refinement}

        Available normalization methods:

        1. **zscore**: Standard z-score normalization
           - Converts to mean=0, std=1
           - Can produce negative weights (suitable for short selling)
           - Best for normally distributed factors

        2. **zscore_clip**: Z-score with clipping to [-1, 1]
           - Limits extreme values
           - Reduces outlier impact

        3. **zscore_maxmin**: Z-score normalized by max absolute value
           - Scales to [-1, 1] range
           - Preserves relative differences

        4. **max_min**: Simple scaling by max absolute value
           - Fast and simple
           - Good for factors with clear bounds

        5. **sum**: Normalize by sum of absolute values
           - Ensures weights sum to 1 (in absolute terms)
           - Good for equal volatility allocation

        6. **rank_s**: Standard rank transformation to [-1, 1]
           - Robust to outliers
           - Loses magnitude information

        7. **rank_balanced**: Balanced rank with normal transformation
           - Maps ranks to normal distribution
           - Good for non-normal factor distributions

        8. **rank_c**: Custom rank with top/bottom n selection
           - Only selects top/bottom n stocks
           - Good for concentrated portfolios

        9. **long_only_zscore**: Z-score shifted to positive range
           - For markets without short selling (e.g., A-shares)
           - Maps to [0, 1] range

        10. **long_only_softmax**: Softmax transformation
            - Ensures all positive weights (e.g., A-shares)
            - Emphasizes relative differences

        Please consider:
        - only A-shares market cannot short sell (需要正权重)
        - US equities,futures and crypto market can have negative weights (可以做空)
        - Factor distribution characteristics
        - Risk management requirements

        Respond in JSON format (in English):
        {{
            "method": "method_name",
            "params": {{
                "winsorize": true/false,
                "q": 0.05,  // for winsorization
                "n": 10,    // for rank_c method
                "temperature": 1.0  // for softmax
            }},
            "reasoning": "brief explanation"
        }}
        CRITICAL: Please ensure the JSON response is complete and properly closed with all necessary closing braces. Do not truncate the response.
        """

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            model=self.config.models["sub_strategy_agent"],
            temperature=self.config.llm_config["temperature"]
        )

        try:
            config = parse_json_response(response.content)
            # 验证方法名
            valid_methods = [
                "zscore", "zscore_clip", "zscore_maxmin", "max_min", "sum",
                "rank_s", "rank_balanced", "rank_c", "long_only_zscore", "long_only_softmax"
            ]
            if config["method"] not in valid_methods:
                logger.warning(f"Invalid method: {config['method']}, defaulting to zscore")
                config["method"] = "zscore"
            return config
        except:
            logger.warning("Failed to parse LLM response, using default config")
            # 根据市场类型选择默认方法
            if market_type == "A_SHARES":
                return {
                    "method": "long_only_zscore",
                    "params": {"winsorize": True, "q": 0.05},
                    "reasoning": "Default for A-shares market"
                }
            else:
                return {
                    "method": "zscore",
                    "params": {"winsorize": True, "q": 0.05},
                    "reasoning": "Default for other markets"
                }



    def _apply_normalization(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """应用向量化的归一化方法"""
        df_copy = df.copy()
        factor_cols = [col for col in df.columns if col.startswith('F#')]

        # 准备数据
        dt_array = df_copy['dt'].values

        # 对每个因子列应用归一化
        for col in factor_cols:
            x_array = df_copy[col].values
            normalized = self._cross_normalize_numpy(
                dt_array, x_array,
                method=config['method'],
                **config.get('params', {})
            )
            df_copy[col] = normalized

        return df_copy

    def _cross_normalize_numpy(self, dt_array: np.ndarray, x_array: np.ndarray,
                               method: str = 'zscore', **kwargs) -> np.ndarray:
        """基于NumPy的向量化归一化函数"""
        # 检查NaN值
        nan_mask = np.isnan(x_array)
        if np.any(nan_mask):
            raise ValueError(f"Factor has missing values: {np.sum(nan_mask)}")

        # 获取参数
        winsorize = kwargs.get("winsorize", False)
        q = kwargs.get("q", 0.05)
        n = kwargs.get("n", 10)
        temperature = kwargs.get("temperature", 1.0)

        # 创建结果数组
        result = np.zeros_like(x_array, dtype=np.float64)

        # 获取唯一日期
        unique_dates, dt_inverse = np.unique(dt_array, return_inverse=True)

        # 按日期分组处理
        for i, dt in enumerate(unique_dates):
            # 创建当前日期的掩码
            dt_mask = (dt_inverse == i)
            dt_indices = np.where(dt_mask)[0]
            dt_x_values = x_array[dt_mask]

            # 检查数据点数量
            if len(dt_x_values) <= 1:
                continue

            # Winsorize处理
            if winsorize:
                lower, upper = np.percentile(dt_x_values, [q * 100, (1 - q) * 100])
                if lower < upper:
                    dt_x_values = np.clip(dt_x_values, lower, upper)

            # 应用归一化方法
            normalized = np.zeros_like(dt_x_values)

            try:
                if method == "zscore":
                    mean = np.mean(dt_x_values)
                    std = np.std(dt_x_values)
                    if std > 1e-9:
                        normalized = (dt_x_values - mean) / std

                elif method == "zscore_clip":
                    mean = np.mean(dt_x_values)
                    std = np.std(dt_x_values)
                    if std > 1e-9:
                        normalized = (dt_x_values - mean) / std
                        normalized = np.clip(normalized, -1, 1)

                elif method == "zscore_maxmin":
                    mean = np.mean(dt_x_values)
                    std = np.std(dt_x_values)
                    if std > 1e-9:
                        z = (dt_x_values - mean) / std
                        max_abs = np.max(np.abs(z))
                        if max_abs > 1e-9:
                            normalized = z / max_abs

                elif method == "max_min":
                    max_abs_val = np.max(np.abs(dt_x_values))
                    if max_abs_val > 1e-9:
                        normalized = dt_x_values / max_abs_val

                elif method == "sum":
                    sum_abs = np.sum(np.abs(dt_x_values))
                    if sum_abs > 1e-9:
                        normalized = dt_x_values / sum_abs

                elif method == "rank_s":
                    ranks = stats.rankdata(dt_x_values, method='average')
                    n_valid = len(dt_x_values)
                    if n_valid > 0:
                        normalized = 2 * (ranks - (n_valid + 1) / 2) / n_valid

                elif method == "rank_balanced":
                    ranks = stats.rankdata(dt_x_values)
                    n_valid = len(dt_x_values)
                    if n_valid > 0:
                        percentiles = ranks / (n_valid + 1)
                        normalized = stats.norm.ppf(percentiles)
                        normalized = np.clip(normalized, -3, 3)

                elif method == "rank_c":
                    n_valid = len(dt_x_values)
                    if n_valid > 0:
                        actual_n = min(n, n_valid // 2)  # 确保不超过一半的股票
                        sorted_indices = np.argsort(dt_x_values)

                        # 初始化为0
                        normalized = np.zeros_like(dt_x_values)

                        # 底部n个股票赋负权重
                        bottom_indices = sorted_indices[:actual_n]
                        for j, idx in enumerate(bottom_indices):
                            normalized[idx] = -(actual_n - j) / actual_n

                        # 顶部n个股票赋正权重
                        top_indices = sorted_indices[-actual_n:]
                        for j, idx in enumerate(top_indices):
                            normalized[idx] = (j + 1) / actual_n

                elif method == "long_only_zscore":
                    # 适用于不能做空的市场
                    mean = np.mean(dt_x_values)
                    std = np.std(dt_x_values)
                    if std > 1e-9:
                        z = (dt_x_values - mean) / std
                        # 转换到[0, 1]范围
                        min_z = np.min(z)
                        max_z = np.max(z)
                        if max_z > min_z:
                            normalized = (z - min_z) / (max_z - min_z)

                elif method == "long_only_softmax":
                    # Softmax确保所有权重为正
                    # 先标准化以提高数值稳定性
                    mean = np.mean(dt_x_values)
                    std = np.std(dt_x_values)
                    if std > 1e-9:
                        z = (dt_x_values - mean) / std
                        # 应用温度参数
                        z = z / temperature
                        # Softmax
                        exp_z = np.exp(z - np.max(z))  # 减去最大值提高稳定性
                        normalized = exp_z / np.sum(exp_z)

                else:
                    raise ValueError(f"Unsupported normalization method: {method}")

                # 存储结果（保留原始精度，不再强制舍入到2位小数）
                result[dt_indices] = normalized

            except Exception as e:
                logger.error(f"Error in normalization for date {dt}: {e}")
                # 错误时保持为0

        return result

    def _calculate_factor_returns(self, weights_df: pd.DataFrame) -> pd.DataFrame:
        """计算因子收益"""
        factor_returns = calculate_factor_returns_blocked(
            df=weights_df,
            n_jobs=self.config.backtest_config["n_jobs"],
            current_frequency='4h',
            split_time=pd.to_datetime('2024-01-01')
        )
        return factor_returns

    def _backtest_factors(self, weights_df: pd.DataFrame) -> pd.DataFrame:
        """回测所有因子"""
        self.factor_metric = self.factor_calculator.evaluate_factor_blocked(
            weights_df, n_jobs=self.config.backtest_config["n_jobs"],
            current_frequency='4h'
        )
        return self.factor_metric

    def _format_sub_strategies(self, factor_metrics: pd.DataFrame) -> Dict[str, Any]:
        """格式化子策略结果"""
        strategies = {}
        for _, row in factor_metrics.iterrows():
            factor_name = row['factor']
            strategies[factor_name] = {
                'annual_return': row.get('Annual Return', 0),
                'sharpe_ratio': row.get('Sharpe Ratio', 0),
                'max_drawdown': row.get('Maximum Drawdown', 0),
                'win_rate': row.get('Daily Win Rate', 0),
                'calmar_ratio': row.get('Calmar Ratio', 0)
            }
        return strategies