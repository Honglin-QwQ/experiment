import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import subtract, divide, ts_std_dev, ts_decay_exp_window
import pandas as pd

def factor_5769(data, **kwargs):
    """
    因子名称: volume_weighted_price_oscillation_decay_39579
    数学表达式: ts_decay_exp_window(divide(subtract(close, vwap), ts_std_dev(returns, 30)), 10, 0.7)
    中文描述: 该因子衡量收盘价相对于成交量加权平均价（VWAP）的标准化偏离程度，并应用指数衰减加权平均。首先计算收盘价与VWAP的差值，然后除以过去30天的收益率标准差进行标准化，以衡量价格偏离的波动性调整强度。最后，对标准化后的偏离值计算过去10天的指数衰减加权平均，衰减因子为0.7，使得近期数据具有更高的权重。该因子旨在捕捉经过波动率调整的价格偏离的持续性和方向性，并对近期市场行为赋予更高的权重。创新点在于结合了VWAP、收益率波动率和指数衰减加权平均，以更精细地刻画价格偏离的动态特征，并响应改进建议中关于引入其他因子（如VWAP）、调整参数（如时间窗口和衰减因子）以及使用指数衰减操作符提升因子的方向。
    因子应用场景：
    1. 波动性调整的价格偏离分析：用于识别价格相对于其平均水平的偏离程度，并根据收益率的波动性进行调整。
    2. 短期趋势跟踪：通过指数衰减加权平均，可以更敏感地捕捉近期价格偏离的趋势。
    """
    # 1. 计算 subtract(close, vwap)
    data_subtract = subtract(data['close'], data['vwap'])
    # 2. 计算 ts_std_dev(returns, 30)
    data_ts_std_dev = ts_std_dev(data['returns'], 30)
    # 3. 计算 divide(subtract(close, vwap), ts_std_dev(returns, 30))
    data_divide = divide(data_subtract, data_ts_std_dev)
    # 4. 计算 ts_decay_exp_window(divide(subtract(close, vwap), ts_std_dev(returns, 30)), 10, 0.7)
    factor = ts_decay_exp_window(data_divide, 10, 0.7)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()