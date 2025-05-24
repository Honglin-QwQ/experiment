import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5626(data, **kwargs):
    """
    因子名称: factor_0006_18035
    数学表达式: ts_rank(s_log_1p(vol), d=10) + ts_rank(0.5*(open+close)+rank(vwap - close), d=10)
    中文描述: 该因子结合了交易量和价格行为的两种不同视角。首先，使用s_log_1p对交易量进行对数变换，然后计算过去10天交易量排名的ts_rank。其次，计算每日开盘价和收盘价的平均值，加上量价差异的排序，再计算过去10天这个组合因子的排名。最后，将这两个排名相加。这个因子旨在捕捉交易量的动量和价格行为的趋势，从而识别潜在的交易机会。
    因子应用场景：
    1. 交易量动量：通过对交易量取对数并计算排名，可以捕捉交易量变化的动量。
    2. 价格行为趋势：结合开盘价、收盘价和量价差异的排名，可以识别价格行为的趋势。
    3. 潜在交易机会：结合交易量动量和价格行为趋势，可以识别潜在的交易机会。
    """
    # 计算 s_log_1p(vol)
    s_log_1p_vol = s_log_1p(data['vol'])

    # 计算 ts_rank(s_log_1p(vol), d=10)
    ts_rank_vol = ts_rank(s_log_1p_vol, d=10)

    # 计算 0.5*(open+close)
    open_close_mean = 0.5 * (data['open'] + data['close'])

    # 计算 vwap - close
    vwap_close_diff = data['vwap'] - data['close']

    # 计算 rank(vwap - close)
    rank_vwap_close = rank(vwap_close_diff)

    # 计算 0.5*(open+close)+rank(vwap - close)
    combined_factor = open_close_mean + rank_vwap_close

    # 计算 ts_rank(0.5*(open+close)+rank(vwap - close), d=10)
    ts_rank_combined = ts_rank(combined_factor, d=10)

    # 计算 ts_rank(s_log_1p(vol), d=10) + ts_rank(0.5*(open+close)+rank(vwap - close), d=10)
    factor = ts_rank_vol + ts_rank_combined

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()