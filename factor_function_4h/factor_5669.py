import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5669(data, **kwargs):
    """
    因子名称: factor_volume_price_momentum_enhanced_29991
    数学表达式: if_else(ts_rank(close, 5) > ts_rank(low, 5), ts_delta(ts_rank(multiply(close, log(vol)), 10), 5), reverse(ts_delta(ts_rank(multiply(close, log(vol)), 10), 5)))
    中文描述: 该因子是factor_volume_price_momentum的增强版本，旨在通过引入条件判断来提升其在不同市场条件下的适应性。它首先比较了收盘价和最低价的短期排名，如果收盘价排名高于最低价排名，则使用原始的价量动量因子；反之，则使用原始因子的反转。这种设计旨在捕捉价格上涨和下跌趋势中的不同价量关系，当价格上涨时，使用原始因子捕捉顺势动量；当价格下跌时，使用反转因子捕捉逆势反弹的可能性。这种创新性的结构使得因子能够更好地适应不同的市场环境，提升了其稳定性和预测能力。
    因子应用场景：
    1. 趋势判断：用于判断当前是上涨趋势还是下跌趋势，从而选择不同的动量计算方式。
    2. 市场适应性：增强了因子在不同市场条件下的适应性，提高了稳定性。
    3. 动量捕捉：在上涨趋势中捕捉顺势动量，在下跌趋势中捕捉逆势反弹的可能性。
    """
    # 计算 ts_rank(close, 5)
    ts_rank_close = ts_rank(data['close'], 5)
    # 计算 ts_rank(low, 5)
    ts_rank_low = ts_rank(data['low'], 5)
    # 计算 log(vol)
    log_vol = log(data['vol'])
    # 计算 multiply(close, log(vol))
    multiply_close_log_vol = multiply(data['close'], log_vol)
    # 计算 ts_rank(multiply(close, log(vol)), 10)
    ts_rank_multiply_close_log_vol = ts_rank(multiply_close_log_vol, 10)
    # 计算 ts_delta(ts_rank(multiply(close, log(vol)), 10), 5)
    ts_delta_ts_rank_multiply_close_log_vol = ts_delta(ts_rank_multiply_close_log_vol, 5)
    # 计算 reverse(ts_delta(ts_rank(multiply(close, log(vol)), 10), 5))
    reverse_ts_delta_ts_rank_multiply_close_log_vol = reverse(ts_delta_ts_rank_multiply_close_log_vol)
    # 计算 if_else(ts_rank(close, 5) > ts_rank(low, 5), ts_delta(ts_rank(multiply(close, log(vol)), 10), 5), reverse(ts_delta(ts_rank(multiply(close, log(vol)), 10), 5)))
    factor = if_else(ts_rank_close > ts_rank_low, ts_delta_ts_rank_multiply_close_log_vol, reverse_ts_delta_ts_rank_multiply_close_log_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()