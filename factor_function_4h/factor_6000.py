import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import multiply
from operators import ts_delta
from operators import ts_decay_linear
from operators import ts_kurtosis
import pandas as pd

def factor_6000(data, **kwargs):
    """
    因子名称: Returns_Kurtosis_Weighted_Delta_37040
    数学表达式: multiply(ts_delta(returns, 1), ts_decay_linear(ts_kurtosis(vol, 20), 10))
    中文描述: 该因子结合了日收益率的变化（ts_delta(returns, 1)）和过去20天成交量峰度的线性衰减加权平均（ts_decay_linear(ts_kurtosis(vol, 20), 10)）。在参考因子的基础上，我们引入了收益率的差分来捕捉收益率的短期变化趋势，并使用线性衰减加权平均来赋予近期成交量峰度更大的权重，以反映市场情绪的最新变化。当收益率出现积极变化且近期成交量峰度较高时，因子值会放大，可能预示着由市场情绪驱动的短期动量机会。这旨在解决原因子预测能力弱和IC波动大的问题，通过捕捉更动态的市场信号来提升预测效果和稳定性。同时，将ts_kurtosis的时间窗口调整为20天，并引入10天的线性衰减窗口，尝试优化参数以提高因子效果。
    因子应用场景：
    1. 短期动量机会识别：因子值较高时，可能预示着由市场情绪驱动的短期动量机会。
    2. 市场情绪变化跟踪：通过成交量峰度的线性衰减加权平均，反映市场情绪的最新变化。
    """
    # 1. 计算 ts_delta(returns, 1)
    data_ts_delta_returns = ts_delta(data['returns'], 1)
    # 2. 计算 ts_kurtosis(vol, 20)
    data_ts_kurtosis_vol = ts_kurtosis(data['vol'], 20)
    # 3. 计算 ts_decay_linear(ts_kurtosis(vol, 20), 10)
    data_ts_decay_linear = ts_decay_linear(data_ts_kurtosis_vol, 10)
    # 4. 计算 multiply(ts_delta(returns, 1), ts_decay_linear(ts_kurtosis(vol, 20), 10))
    factor = multiply(data_ts_delta_returns, data_ts_decay_linear)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()