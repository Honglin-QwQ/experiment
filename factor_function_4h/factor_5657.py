import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, rank, ts_corr, log, ts_rank, ts_skewness, if_else, sign
import pandas as pd
import numpy as np

def factor_5657(data, **kwargs):
    """
    因子名称: factor_0007_30514
    数学表达式: ts_delta(rank(ts_corr(close, log(vol), 5)), 10) * ts_rank(ts_delta(close, 1), 20) * if_else(ts_skewness(ts_delta(close, 1), 20) > 0, 1, -1)
    中文描述: 该因子是对factor_0006的改进。在原因子的基础上，引入了成交量的对数，以减小成交量异常值的影响，并使用skewness判断短期价格动量的方向，从而增强了因子对趋势反转和加速的识别能力。具体来说，首先计算收盘价和成交量（取对数后）在过去5天的相关性，并对其进行横截面排名。然后计算该排名在过去10天的变化。同时，计算每日收盘价变化的1日差分，并对其进行20日的时间序列排名。最后，将这两个部分相乘，并乘以一个符号函数，该符号函数基于过去20天收盘价变化偏度的正负，从而捕捉价格和成交量之间的关系变化与短期价格动量之间的相互作用，并根据偏度判断趋势的持续性。
    因子应用场景：
    1. 趋势反转识别：因子值可能在趋势即将反转时发生变化，通过成交量和价格的相互作用来捕捉趋势变化。
    2. 趋势加速识别：当价格动量与成交量关系发生显著变化时，因子值可能预示趋势的加速。
    3. 短期价格动量方向判断：通过偏度判断短期价格动量的方向，辅助判断趋势的持续性。
    """
    # 1. 计算 log(vol)
    log_vol = log(data['vol'])
    # 2. 计算 ts_corr(close, log(vol), 5)
    ts_corr_close_log_vol = ts_corr(data['close'], log_vol, d=5)
    # 3. 计算 rank(ts_corr(close, log(vol), 5))
    rank_ts_corr = rank(ts_corr_close_log_vol)
    # 4. 计算 ts_delta(rank(ts_corr(close, log(vol), 5)), 10)
    ts_delta_rank_ts_corr = ts_delta(rank_ts_corr, d=10)
    # 5. 计算 ts_delta(close, 1)
    ts_delta_close = ts_delta(data['close'], d=1)
    # 6. 计算 ts_rank(ts_delta(close, 1), 20)
    ts_rank_ts_delta_close = ts_rank(ts_delta_close, d=20)
    # 7. 计算 ts_skewness(ts_delta(close, 1), 20)
    ts_skewness_ts_delta_close = ts_skewness(ts_delta_close, d=20)
    # 8. 计算 if_else(ts_skewness(ts_delta(close, 1), 20) > 0, 1, -1)
    if_else_condition = ts_skewness_ts_delta_close > 0
    if_else_result = if_else(if_else_condition, 1, -1)
    # 9. 计算 ts_delta(rank(ts_corr(close, log(vol), 5)), 10) * ts_rank(ts_delta(close, 1), 20) * if_else(ts_skewness(ts_delta(close, 1), 20) > 0, 1, -1)
    factor = ts_delta_rank_ts_corr * ts_rank_ts_delta_close * if_else_result

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()