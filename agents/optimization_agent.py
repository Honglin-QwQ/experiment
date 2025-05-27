import json

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from loguru import logger
from tqdm import tqdm
from agents.base_agnet import BaseAgent, Message, MessageType

from config.system_config import SystemConfig
from config.system_config import PromptTemplates
from llm.llm_client import OpenRouterClient

# skfolio imports
from skfolio import RiskMeasure, Population, PerfMeasure, RatioMeasure
from skfolio.optimization import (
    MeanRisk, ObjectiveFunction, InverseVolatility,
    RiskBudgeting, NestedClustersOptimization, EqualWeighted
)
from skfolio.model_selection import WalkForward, cross_val_predict
from skfolio.prior import EmpiricalPrior
from skfolio.moments import DenoiseCovariance, ShrunkMu


class OptimizationAgent(BaseAgent):
    """优化智能体 - 负责投资组合优化"""

    def __init__(self, name: str, llm_client: OpenRouterClient, config: SystemConfig):
        super().__init__(name, llm_client, config)
        self.optimization_models = self._initialize_models()

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return PromptTemplates.optimization_system_prompt()

    def _initialize_models(self) -> Dict[str, Any]:
        """初始化优化模型"""
        return {
            "MaxSharpe": lambda: MeanRisk(
                risk_measure=RiskMeasure.STANDARD_DEVIATION,
                objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                portfolio_params=dict(name="Max Sharpe")
            ),
            "MaxSharpe_shrinkage": lambda: MeanRisk(
                risk_measure=RiskMeasure.VARIANCE,
                objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                prior_estimator=EmpiricalPrior(
                    mu_estimator=ShrunkMu(),
                    covariance_estimator=DenoiseCovariance()
                ),
                portfolio_params=dict(name="Max Sharpe - Shrinkage")
            ),
            "MinCVaR": lambda: MeanRisk(
                risk_measure=RiskMeasure.CVAR,
                objective_function=ObjectiveFunction.MINIMIZE_RISK,
                portfolio_params=dict(name="Min CVaR")
            ),
            "InverseVol": lambda: InverseVolatility(
                portfolio_params=dict(name="Inverse Volatility")
            ),
            "EqualWeight": lambda: EqualWeighted(
                portfolio_params=dict(name="Equal Weight")
            ),
            "RiskParity": lambda: RiskBudgeting(
                risk_measure=RiskMeasure.VARIANCE,
                portfolio_params=dict(name="Risk Parity")
            ),
            "NCO": lambda: NestedClustersOptimization(
                inner_estimator=MeanRisk(
                    objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                    risk_measure=RiskMeasure.VARIANCE,
                    prior_estimator=EmpiricalPrior(
                        mu_estimator=ShrunkMu(),
                        covariance_estimator=DenoiseCovariance()
                    )
                ),
                outer_estimator=RiskBudgeting(risk_measure=RiskMeasure.CVAR),
                n_jobs=-1,
                portfolio_params=dict(name="Nested Clusters Optimization")
            )
        }

    def process_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.type == MessageType.OPTIMIZATION_REQUEST:
            return self._handle_optimization_request(message)
        return None

    def _handle_optimization_request(self, message: Message) -> Message:
        """处理优化请求"""
        try:
            selected_strategies = message.content.get("selected_strategies", {})
            factor_returns_dict = message.content.get("factor_returns", {})
            config = message.content.get("config", {})
            ssm = message.content.get("ssm", {})

            # 转换数据
            factor_returns_df = pd.DataFrame(factor_returns_dict)
            if 'dt' in factor_returns_df.columns:
                factor_returns_df['dt'] = pd.to_datetime(factor_returns_df['dt'])
                factor_returns_df.set_index('dt', inplace=True)

            # 使用LLM选择优化模型
            selected_models = self._select_optimization_models(
                selected_strategies, config, ssm
            )

            # 对每个策略组合进行优化
            optimization_results = {}

            for strategy_name, factors in tqdm(selected_strategies.items(),
                                               desc="Optimizing strategies"):
                logger.info(f"Optimizing strategy: {strategy_name}")

                # 准备策略数据
                strategy_returns = factor_returns_df[factors]

                # 划分训练集和测试集
                split_date = pd.Timestamp('2024-01-01')
                train_data = strategy_returns[strategy_returns.index <= split_date]
                test_data = strategy_returns[strategy_returns.index > split_date]

                # 优化策略
                strategy_results = self._optimize_strategy(
                    strategy_name,
                    train_data,
                    test_data,
                    selected_models,
                    config
                )

                optimization_results[strategy_name] = strategy_results

            # 选择最佳策略
            best_strategy = self._select_best_strategy(optimization_results, ssm)

            # 生成优化报告
            report = self._generate_optimization_report(optimization_results, best_strategy)

            return self.send_message(
                receiver=message.sender,
                type=MessageType.OPTIMIZATION_RESULT,
                content={
                    "results": optimization_results,
                    "best_strategy": best_strategy,
                    "report": report
                }
            )

        except Exception as e:
            logger.error(f"Error in optimization: {str(e)}")
            return self.send_message(
                receiver=message.sender,
                type=MessageType.ERROR,
                content={"error": str(e)}
            )

    def _select_optimization_models(self, selected_strategies: Dict[str, List[str]],
                                    config: Dict[str, Any],
                                    ssm: Dict[str, Any]) -> List[str]:
        """使用LLM选择优化模型"""
        prompt = f"""
        Based on the investment requirements and selected strategies, recommend optimization models.

        SSM Requirements:
        - Target Return: {ssm.get('target_metrics', {}).get('annualized_return', {})}
        - Risk Constraints: {ssm.get('risk_constraints', {})}
        - Market Type: {ssm.get('market_type', 'US_EQUITIES')}

        Selected Strategies:
        {json.dumps({k: len(v) for k, v in selected_strategies.items()}, indent=2)}

        Available Models:
        1. MaxSharpe - Maximize Sharpe ratio (good for risk-adjusted returns)
        2. MaxSharpe_shrinkage - MaxSharpe with shrinkage estimators (reduces estimation error)
        3. MinCVaR - Minimize Conditional Value at Risk (focuses on tail risk)
        4. InverseVol - Inverse volatility weighting (simple and robust)
        5. EqualWeight - Equal weighting (baseline)
        6. RiskParity - Risk parity (equal risk contribution)
        7. NCO - Nested Clusters Optimization (handles highly correlated assets)

        Recommend 3-5 models that would work best for these requirements.
        Consider:
        - If high returns are targeted, include MaxSharpe variants
        - If risk control is important, include MinCVaR or RiskParity
        - Always include a baseline (EqualWeight or InverseVol)
        - For many correlated factors, consider NCO

        Respond with a list of model names:
        ["model1", "model2", "model3"]
        """

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            model=self.config.models["optimization_agent"],
            temperature=0.3
        )

        try:
            models = json.loads(response.content)
            # 验证模型名称
            valid_models = [m for m in models if m in self.optimization_models]
            if not valid_models:
                valid_models = ["MaxSharpe", "InverseVol", "EqualWeight"]
            return valid_models
        except:
            # 默认模型组合
            return ["MaxSharpe", "InverseVol", "RiskParity"]

    def _optimize_strategy(self, strategy_name: str, train_data: pd.DataFrame,
                           test_data: pd.DataFrame, selected_models: List[str],
                           config: Dict[str, Any]) -> Dict[str, Any]:
        """优化单个策略"""
        model_results = {}
        populations = []

        # 设置滚动窗口交叉验证
        cv = WalkForward(train_size=252, test_size=21)  # 1年训练，1月测试

        for model_name in selected_models:
            try:
                logger.info(f"  Running {model_name} optimization...")

                # 创建模型实例
                model = self.optimization_models[model_name]()

                # 根据模型类型选择优化方法
                if model_name in ["NCO"]:
                    # NCO需要先fit再predict
                    model.fit(train_data)
                    pred = model.predict(test_data)
                else:
                    # 其他模型使用交叉验证
                    pred = cross_val_predict(
                        model,
                        test_data,
                        cv=cv,
                        portfolio_params=dict(name=f"{strategy_name}_{model_name}")
                    )

                # 保存结果
                model_results[model_name] = {
                    "portfolio": pred,
                    "weights": pred.weights_per_observation,
                    "performance": {
                        "annual_return": pred.annualized_mean,
                        "annual_volatility": pred.annualized_standard_deviation,
                        "sharpe_ratio": pred.annualized_sharpe_ratio,
                        "max_drawdown": pred.max_drawdown,
                        "sortino_ratio": pred.annualized_sortino_ratio,
                        "calmar_ratio": pred.calmar_ratio
                    }
                }

                populations.append(pred)

            except Exception as e:
                logger.warning(f"  Model {model_name} failed: {str(e)}")
                continue

        # 创建Population对象用于比较
        if populations:
            population = Population(populations)
            model_results["population"] = population

        return model_results

    def _select_best_strategy(self, optimization_results: Dict[str, Dict[str, Any]],
                              ssm: Dict[str, Any]) -> Dict[str, Any]:
        """选择最佳策略"""
        # 提取所有策略的性能指标
        all_strategies = []

        for strategy_name, strategy_results in optimization_results.items():
            for model_name, model_result in strategy_results.items():
                if model_name != "population" and "performance" in model_result:
                    perf = model_result["performance"]
                    all_strategies.append({
                        "strategy_name": strategy_name,
                        "model_name": model_name,
                        "combined_name": f"{strategy_name}_{model_name}",
                        **perf
                    })

        if not all_strategies:
            logger.error("No strategies to select from")
            return {}

        # 转换为DataFrame便于分析
        strategies_df = pd.DataFrame(all_strategies)

        # 使用LLM根据SSM选择最佳策略
        prompt = f"""
        Select the best strategy based on SSM requirements and performance metrics.

        SSM Targets:
        {json.dumps(ssm.get('target_metrics', {}), indent=2)}

        Strategy Performance:
        {strategies_df.to_string()}

        Please select the best strategy considering:
        1. Meeting or exceeding target metrics
        2. Risk-adjusted returns (Sharpe/Sortino ratio)
        3. Downside protection (max drawdown)
        4. Overall balance of risk and return

        Respond with the combined_name of the best strategy.
        """

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            model=self.config.models["optimization_agent"],
            temperature=0.1
        )

        best_name = response.content.strip().strip('"')

        # 查找对应的策略
        best_row = strategies_df[strategies_df['combined_name'] == best_name]

        if best_row.empty:
            # 如果LLM选择无效，使用夏普比率最高的
            best_row = strategies_df.loc[strategies_df['sharpe_ratio'].idxmax()]

        # 获取完整的策略信息
        strategy_name = best_row.iloc[0]['strategy_name']
        model_name = best_row.iloc[0]['model_name']

        best_strategy = {
            "strategy_name": strategy_name,
            "model_name": model_name,
            "performance": best_row.iloc[0].to_dict(),
            "weights": optimization_results[strategy_name][model_name]["weights"],
            "portfolio": optimization_results[strategy_name][model_name]["portfolio"]
        }

        return best_strategy

    def _generate_optimization_report(self, optimization_results: Dict[str, Dict[str, Any]],
                                      best_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """生成优化报告"""
        report = {
            "total_strategies_tested": sum(
                len([k for k in v.keys() if k != "population"])
                for v in optimization_results.values()
            ),
            "best_strategy": {
                "name": f"{best_strategy.get('strategy_name', '')}_{best_strategy.get('model_name', '')}",
                "performance": best_strategy.get("performance", {})
            },
            "strategy_comparison": {}
        }

        # 添加每个策略组的最佳模型
        for strategy_name, results in optimization_results.items():
            best_model = None
            best_sharpe = -float('inf')

            for model_name, model_result in results.items():
                if model_name != "population" and "performance" in model_result:
                    sharpe = model_result["performance"].get("sharpe_ratio", -float('inf'))
                    if sharpe > best_sharpe:
                        best_sharpe = sharpe
                        best_model = model_name

            if best_model:
                report["strategy_comparison"][strategy_name] = {
                    "best_model": best_model,
                    "sharpe_ratio": best_sharpe,
                    "performance": results[best_model]["performance"]
                }

        return report
