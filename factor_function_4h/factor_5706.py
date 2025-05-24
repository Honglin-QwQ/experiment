import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_weighted_decay
from operators import multiply
from operators import ts_delta
import pandas as pd

def factor_5706(data, **kwargs):
    """
    因子名称: Volume_Weighted_Price_Momentum_Decay_98788
    数学表达式: ts_weighted_decay(multiply(ts_delta(close, 12), vol), k=0.75)
    中文描述: 该因子结合了短期价格动量和交易量，并应用指数衰减加权来平滑信号。它首先计算过去12天收盘价的变化（ts_delta(close, 12)），然后将这个价格变化与当前交易量（vol）相乘，得到一个考虑了交易活跃度的价格动量信号。最后，使用ts_weighted_decay运算符对这个信号进行加权衰减处理，其中k=0.75表示当前日的信号权重较高，前一日的信号权重较低。这种衰减机制使得因子更侧重于近期的数据，同时保留了历史信息的影响，但权重逐渐减小。这有助于捕捉近期强劲的价格动量，并过滤掉较远期数据的噪声。该因子可以用于识别那些在近期价格变动显著且伴随高交易量的股票，并期望这种趋势在短期内持续。创新点在于结合了价格变化、交易量和加权衰减，以更精细地捕捉市场动量。
    因子应用场景：
    1. 动量交易：识别价格动量强劲且成交量活跃的股票，适用于短期动量策略。
    2. 趋势跟踪：用于确认价格趋势，特别是在成交量配合的情况下，提高趋势的可信度。
    3. 风险管理：通过衰减加权，降低旧数据对当前因子的影响，从而更快地适应市场变化。
    """
    # 1. 计算 ts_delta(close, 12)
    data_ts_delta_close = ts_delta(data['close'], d=12)
    # 2. 计算 multiply(ts_delta(close, 12), vol)
    data_multiply = multiply(data_ts_delta_close, data['vol'])
    # 3. 计算 ts_weighted_decay(multiply(ts_delta(close, 12), vol), k=0.75)
    factor = ts_weighted_decay(data_multiply, k=0.75)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()