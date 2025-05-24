import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5813(data, **kwargs):
    """
    因子名称: Volume_Weighted_Price_Momentum_Volatility_Ratio_58615
    数学表达式: divide(ts_corr(ts_delta(close, 5), ts_std_dev(volume, 15), 30), ts_std_dev(ts_weighted_decay(close, 0.7), 20))
    中文描述: 该因子旨在捕捉收盘价短期变化与成交量短期波动之间的关系，并在一个较长的时间窗口内计算它们的相关性，并将其与加权收盘价的波动性进行比值。具体而言，它首先计算过去5天收盘价的变化量，然后计算过去15天成交量的标准差（衡量成交量的波动性）。接着，计算这两个时间序列在过去30天内的相关性。同时，计算过去20天内经过0.7权重衰减处理的收盘价的标准差。最后，将前者的相关性除以后者的标准差。该因子在参考因子的基础上进行了创新，不仅考虑了价格动量和成交量波动性的相关性，还将其与考虑近期价格变动的波动性进行对比，试图识别在价格和成交量配合变化的同时，价格本身的波动风险。较高的因子值可能表明价格动量与成交量配合良好，且价格本身的波动相对可控，可能预示着趋势的延续性较强。
    因子应用场景：
    1. 趋势识别：用于识别价格动量和成交量波动性之间的关系，判断趋势的稳定性和可控性。
    2. 风险评估：通过对比价格动量与成交量的相关性以及价格本身的波动性，评估潜在的投资风险。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 2. 计算 ts_std_dev(volume, 15)
    data_ts_std_dev_volume = ts_std_dev(data['vol'], 15)
    # 3. 计算 ts_corr(ts_delta(close, 5), ts_std_dev(volume, 15), 30)
    data_ts_corr = ts_corr(data_ts_delta_close, data_ts_std_dev_volume, 30)
    # 4. 计算 ts_weighted_decay(close, 0.7)
    data_ts_weighted_decay_close = ts_weighted_decay(data['close'], 0.7)
    # 5. 计算 ts_std_dev(ts_weighted_decay(close, 0.7), 20)
    data_ts_std_dev = ts_std_dev(data_ts_weighted_decay_close, 20)
    # 6. 计算 divide(ts_corr(ts_delta(close, 5), ts_std_dev(volume, 15), 30), ts_std_dev(ts_weighted_decay(close, 0.7), 20))
    factor = divide(data_ts_corr, data_ts_std_dev)

    # 删除中间变量
    del data_ts_delta_close
    del data_ts_std_dev_volume
    del data_ts_corr
    del data_ts_weighted_decay_close
    del data_ts_std_dev

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()