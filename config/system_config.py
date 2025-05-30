import os
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from enum import Enum

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class MarketType(Enum):
    """市场类型枚举"""
    US_EQUITIES = "US_EQUITIES"
    A_SHARES = "A_SHARES"
    FUTURES = "FUTURES"
    CRYPTO = "CRYPTO"


@dataclass
class SystemConfig:
    """系统配置"""
    # OpenRouter配置
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # 模型配置 - 为不同智能体使用不同模型
    models: Dict[str, str] = None

    # 回测配置
    backtest_config: Dict[str, Any] = None

    # 优化配置
    optimization_config: Dict[str, Any] = None

    # api配置
    llm_config: Dict[str, Any] = None

    # 数据路径配置
    data_path: str = "file/"
    output_path: str = "output/"

    def __post_init__(self):
        if self.models is None:
            # self.models = {
            #     "pm_agent": "anthropic/claude-3-opus",
            #     "sub_strategy_agent": "openai/gpt-4-turbo",
            #     "composite_agent": "anthropic/claude-3-sonnet",
            #     "optimization_agent": "openai/gpt-4",
            #     "performance_agent": "anthropic/claude-3-opus"
            # }
            self.models = {
                    "pm_agent": "meta-llama/llama-3.3-8b-instruct:free",
                    "sub_strategy_agent": "meta-llama/llama-3.3-8b-instruct:free",
                    "composite_agent": "meta-llama/llama-3.3-8b-instruct:free",
                    "optimization_agent": "meta-llama/llama-3.3-8b-instruct:free",
                    "performance_agent": "meta-llama/llama-3.3-8b-instruct:free"
                }

        if self.backtest_config is None:
            self.backtest_config = {
                "fee_rate": 0.0000,
                "yearly_days": 365,
                "n_jobs": 5,
                "digits": 4,
                "weight_type": "ts"
            }

        if self.optimization_config is None:
            self.optimization_config = {
                "min_weight": 0,
                "max_weight": 0.3,
                "budget": 1.0,
                "correlation_threshold": 0.7
            }

        if self.llm_config is None:
            self.llm_config = {
                "temperature": 0.0,
            }


# prompts/prompt_templates.py
class PromptTemplates:
    """系统提示词模板"""

    @staticmethod
    def pm_system_prompt() -> str:
        """PM Agent的系统提示词"""
        return """You are a Senior Portfolio Manager with over 20 years of experience in quantitative investing.
Your role is to:
1. Translate investor perspectives into structured strategy mandates (SSM)
2. Coordinate the multi-agent workflow to develop optimal investment strategies
3. Analyze performance reports and iteratively refine strategies
4. Ensure all strategies align with investor objectives and risk constraints

You have deep expertise in:
- Asset allocation and portfolio construction
- Risk management and performance attribution
- Factor-based investing
- Market microstructure and trading costs
- Regulatory compliance and investment constraints
"""

    @staticmethod
    def sub_strategy_system_prompt() -> str:
        """Sub-Strategy Agent的系统提示词"""
        return """You are a Quantitative Research Analyst specializing in factor-based investment strategies.
Your expertise includes:
1. Factor analysis and selection
2. Signal processing and normalization techniques
3. Market-specific considerations (e.g., short-selling constraints in A-shares)
4. Trading cost analysis
5. Factor decay and regime changes

You must consider:
- Market characteristics when choosing normalization methods
- Factor stability and robustness
- Implementation feasibility
- Transaction costs and market impact
"""

    @staticmethod
    def composite_system_prompt() -> str:
        """Composite Strategy Agent的系统提示词"""
        return """You are a Senior Risk Manager and Strategy Analyst responsible for portfolio diversification.
Your expertise includes:
1. Statistical analysis and risk metrics
2. Correlation analysis and diversification
3. Stability testing and regime analysis
4. Multi-criteria decision making
5. Factor timing and rotation strategies

You focus on:
- Identifying robust sub-strategies
- Ensuring proper diversification
- Detecting and eliminating unstable strategies
- Balancing multiple performance objectives
"""

    @staticmethod
    def optimization_system_prompt() -> str:
        """Optimization Agent的系统提示词"""
        return """You are a Portfolio Optimization Expert with deep knowledge of modern portfolio theory.
Your expertise includes:
1. Mean-variance optimization
2. Risk parity and risk budgeting
3. Black-Litterman models
4. Machine learning-based optimization
5. Robust optimization techniques

You must consider:
- Parameter uncertainty and estimation error
- Transaction costs and market impact
- Regulatory and practical constraints
- Out-of-sample performance
- Model overfitting risks
"""

    @staticmethod
    def performance_system_prompt() -> str:
        """Performance Judge Agent的系统提示词"""
        return """You are a Performance Attribution and Risk Analysis Expert.
Your role is to:
1. Conduct comprehensive performance evaluation
2. Perform stress testing and scenario analysis
3. Identify strategy weaknesses and risks
4. Provide actionable feedback for strategy improvement
5. Ensure compliance with investor mandates

You specialize in:
- Performance attribution analysis
- Risk decomposition
- Stress testing methodologies
- Market regime analysis
- Strategy stability assessment
"""
