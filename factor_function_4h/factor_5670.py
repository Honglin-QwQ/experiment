import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import log, divide, ts_weighted_decay, ts_zscore, tanh, ts_delta
import pandas as pd
import numpy as np

def factor_5670(data, **kwargs):
    """
    数学表达式: ts_zscore(log(divide(amount, ts_weighted_decay(vol, k=0.3))), 22) + tanh(ts_delta(close, 5))
    中文描述: 该因子结合了历史因子ts_zscore(log(divide(amount, ts_weighted_decay(vol, k=0.3))), 22)和tanh(ts_delta(close, 5))。历史因子通过成交额与加权成交量的比率来捕捉市场情绪，而新增的tanh(ts_delta(close, 5))部分则捕捉了价格的短期动量。通过将价格动量与成交量/成交额信息结合，该因子旨在提高预测能力。tanh函数对价格变动进行缩放，使其值在-1到1之间，从而避免极端值的影响。
    因子应用场景：
    1. 市场情绪分析：通过成交额与加权成交量的比率，捕捉市场对股票的乐观或悲观情绪。
    2. 短期动量捕捉：通过tanh(ts_delta(close, 5))捕捉价格的短期动量。
    3. 结合量价信息：结合成交量/成交额信息和价格动量，提高预测能力。
    """
    # 1. 计算 ts_weighted_decay(vol, k=0.3)
    data_ts_weighted_decay = ts_weighted_decay(data['vol'], k=0.3)
    # 2. 计算 divide(amount, ts_weighted_decay(vol, k=0.3))
    data_divide = divide(data['amount'], data_ts_weighted_decay)
    # 3. 计算 log(divide(amount, ts_weighted_decay(vol, k=0.3)))
    data_log = log(data_divide)
    # 4. 计算 ts_zscore(log(divide(amount, ts_weighted_decay(vol, k=0.3))), 22)
    data_ts_zscore = ts_zscore(data_log, d=22)
    # 5. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], d=5)
    # 6. 计算 tanh(ts_delta(close, 5))
    data_tanh = tanh(data_ts_delta)
    # 7. 计算 ts_zscore(log(divide(amount, ts_weighted_decay(vol, k=0.3))), 22) + tanh(ts_delta(close, 5))
    factor = data_ts_zscore + data_tanh

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()