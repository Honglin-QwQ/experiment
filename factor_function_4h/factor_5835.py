import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, rank, divide, ts_delta, ts_std_dev
import pandas as pd

def factor_5835(data, **kwargs):
    """
    因子名称: Volatility_Adjusted_Weighted_Price_Momentum_27999
    数学表达式: ts_decay_exp_window(rank(divide(ts_delta(close, 5), ts_std_dev(close, 10))), 20, factor=0.85)
    中文描述: 该因子在历史评估和改进建议的基础上进行了优化。它首先计算过去5天收盘价的变化量，并除以过去10天收盘价的标准差，以调整波动率。相较于原始因子，缩短了delta和std_dev的窗口期，旨在捕捉更短期的价格变化和波动率信息，以适应更快的市场变化。然后，对经过波动率调整后的价格变化进行横截面排名（rank），以消除量纲影响并关注相对表现。最后，对这个排名后的信号应用20天的指数衰减加权平均，权重因子调整为0.85，使得近期排名数据的影响更大，衰减速度更快。该因子结合了短期价格变化、短期波动率、横截面排名和时间衰减的概念，旨在识别经过波动率调整后的短期相对强势或弱势，并赋予近期表现更高的权重，可能用于捕捉短期趋势延续或反转机会。
    因子应用场景：
    1. 短期趋势识别：用于识别经过波动率调整后的短期相对强势或弱势的股票。
    2. 快速市场变化适应：适用于需要快速捕捉市场变化的策略。
    3. 趋势延续或反转机会：可能用于捕捉短期趋势延续或反转的机会。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], 5)
    # 2. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], 10)
    # 3. 计算 divide(ts_delta(close, 5), ts_std_dev(close, 10))
    data_divide = divide(data_ts_delta, data_ts_std_dev)
    # 4. 计算 rank(divide(ts_delta(close, 5), ts_std_dev(close, 10)))
    data_rank = rank(data_divide, 2)
    # 5. 计算 ts_decay_exp_window(rank(divide(ts_delta(close, 5), ts_std_dev(close, 10))), 20, factor=0.85)
    factor = ts_decay_exp_window(data_rank, 20, factor=0.85)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()