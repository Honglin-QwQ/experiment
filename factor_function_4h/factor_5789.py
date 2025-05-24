import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5789(data, **kwargs):
    """
    因子名称: Price_Volatility_Skew_Divergence_26791
    数学表达式: ts_delta(ts_skewness(ts_std_dev(close, 15), 25), 40) * ts_corr(ts_delta(high, 7), ts_delta(low, 7), 20)
    中文描述: 该因子旨在捕捉收盘价波动率偏度的长期变化与短期高低价变化相关性之间的背离。首先，计算过去15天收盘价的标准差，衡量短期价格波动。然后计算这个波动率序列在过去25天内的偏度，反映波动率分布的非对称性。接着，计算这个偏度序列在过去40天内的变化，捕捉波动率偏度的长期趋势。同时，计算过去7天高价变化与过去7天低价变化在过去20天内的相关性，衡量短期价格波动的同步性。最后，将波动率偏度的长期变化与短期高低价变化的相关性相乘。因子逻辑在于，当收盘价波动率的偏度长期上升（例如，市场对下跌风险越来越敏感）而短期高低价变化的相关性下降（例如，价格波动变得不协调）时，可能预示着市场动量正在减弱或出现背离，这可能是一个潜在的交易信号。相较于参考因子，该因子将分析的基础价格从low替换为close，并调整了各个时间窗口参数，以期捕捉更具代表性的价格波动特征。同时，简化了部分嵌套结构，降低了噪音放大的风险。
    因子应用场景：
    1. 识别市场背离：当因子值显著变化时，可能预示着市场动量减弱或出现背离，为交易者提供预警信号。
    2. 风险评估：通过分析波动率偏度的变化，评估市场对潜在风险的敏感度，辅助风险管理。
    3. 短期交易策略：结合高低价变化的相关性，捕捉短期价格波动的不协调性，为短期交易提供参考。
    """
    # 1. 计算 ts_std_dev(close, 15)
    data_ts_std_dev_close = ts_std_dev(data['close'], 15)
    # 2. 计算 ts_skewness(ts_std_dev(close, 15), 25)
    data_ts_skewness = ts_skewness(data_ts_std_dev_close, 25)
    # 3. 计算 ts_delta(ts_skewness(ts_std_dev(close, 15), 25), 40)
    data_ts_delta_skewness = ts_delta(data_ts_skewness, 40)
    # 4. 计算 ts_delta(high, 7)
    data_ts_delta_high = ts_delta(data['high'], 7)
    # 5. 计算 ts_delta(low, 7)
    data_ts_delta_low = ts_delta(data['low'], 7)
    # 6. 计算 ts_corr(ts_delta(high, 7), ts_delta(low, 7), 20)
    data_ts_corr = ts_corr(data_ts_delta_high, data_ts_delta_low, 20)
    # 7. 计算 ts_delta(ts_skewness(ts_std_dev(close, 15), 25), 40) * ts_corr(ts_delta(high, 7), ts_delta(low, 7), 20)
    factor = data_ts_delta_skewness * data_ts_corr

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()