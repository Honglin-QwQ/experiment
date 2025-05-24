import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_6040(data, **kwargs):
    """
    因子名称: VolumeWeightedDeltaReturnVolatilityRatio_11535
    数学表达式: divide(ts_returns(divide(ts_sum(multiply(ts_delta(close, 2), volume), 5), ts_sum(volume, 5)), 10), ts_std_dev(divide(ts_sum(multiply(ts_delta(close, 2), volume), 5), ts_sum(volume, 5)), 10))
    中文描述: 该因子计算收盘价在2天周期内变动的成交量加权平均值，并计算该加权平均值在过去10天内的相对变动。最后，将该相对变动除以其在过去10天内的标准差。这旨在衡量短期价格动量相对于其自身波动性的表现，同时考虑了成交量的重要性。因子结合了参考因子1的短期价格动量捕捉能力和参考因子2的波动性衡量概念，并根据改进建议加入了成交量加权，通过标准化处理，使得因子更具可比性，减少极端波动对因子值的影响。高因子值可能表明在相对稳定的短期价格变动下，存在较强的动量效应，且这种动量得到了成交量的支持。
    因子应用场景：
    1. 动量分析：用于识别成交量支持的短期价格动量。
    2. 波动性评估：衡量价格动量相对于其自身波动性的表现。
    """
    # 1. 计算 ts_delta(close, 2)
    data_ts_delta_close = ts_delta(data['close'], d = 2)
    # 2. 计算 multiply(ts_delta(close, 2), volume)
    data_multiply = multiply(data_ts_delta_close, data['vol'])
    # 3. 计算 ts_sum(multiply(ts_delta(close, 2), volume), 5)
    data_ts_sum_multiply = ts_sum(data_multiply, d = 5)
    # 4. 计算 ts_sum(volume, 5)
    data_ts_sum_volume = ts_sum(data['vol'], d = 5)
    # 5. 计算 divide(ts_sum(multiply(ts_delta(close, 2), volume), 5), ts_sum(volume, 5))
    data_divide_sum = divide(data_ts_sum_multiply, data_ts_sum_volume)
    # 6. 计算 ts_returns(divide(ts_sum(multiply(ts_delta(close, 2), volume), 5), ts_sum(volume, 5)), 10)
    data_ts_returns = ts_returns(data_divide_sum, d = 10)
    # 7. 计算 ts_std_dev(divide(ts_sum(multiply(ts_delta(close, 2), volume), 5), ts_sum(volume, 5)), 10)
    data_ts_std_dev = ts_std_dev(data_divide_sum, d = 10)
    # 8. 计算 divide(ts_returns(divide(ts_sum(multiply(ts_delta(close, 2), volume), 5), ts_sum(volume, 5)), 10), ts_std_dev(divide(ts_sum(multiply(ts_delta(close, 2), volume), 5), ts_sum(volume, 5)), 10))
    factor = divide(data_ts_returns, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()