import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5673(data, **kwargs):
    """
    数学表达式: rank(ts_sum(if_else(ts_delta(close, 1) > 0, ts_delta(close, 1), 0), 12) / (ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)), 0), 12) + 1e-6)) - rank(ts_std_dev(close, 20))
    中文描述: 该因子旨在结合正负动量比率和价格波动率来评估市场情绪。首先，计算过去12天收盘价上涨幅度总和与下跌幅度总和的比率，反映了市场看涨或看跌的程度。然后，减去过去20天收盘价的标准差的排名，衡量价格的波动程度。该因子的创新之处在于将市场情绪和价格波动两个维度结合起来，通过rank操作符，增强因子的鲁棒性。
    因子应用场景：
    1. 市场情绪分析：通过正负动量比率判断市场整体情绪。
    2. 波动率风险评估：结合价格波动率评估市场风险。
    3. 多因子策略：与其他因子结合，提高选股效果。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)

    # 2. 计算 if_else(ts_delta(close, 1) > 0, ts_delta(close, 1), 0)
    data_if_else_pos = if_else(data_ts_delta_close > 0, data_ts_delta_close, 0)

    # 3. 计算 ts_sum(if_else(ts_delta(close, 1) > 0, ts_delta(close, 1), 0), 12)
    data_ts_sum_pos = ts_sum(data_if_else_pos, 12)

    # 4. 计算 if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)), 0)
    data_if_else_neg = if_else(data_ts_delta_close < 0, abs(data_ts_delta_close), 0)

    # 5. 计算 ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)), 0), 12)
    data_ts_sum_neg = ts_sum(data_if_else_neg, 12)

    # 6. 计算 ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)), 0), 12) + 1e-6
    data_denominator = data_ts_sum_neg + 1e-6

    # 7. 计算 ts_sum(if_else(ts_delta(close, 1) > 0, ts_delta(close, 1), 0), 12) / (ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)), 0), 12) + 1e-6)
    data_ratio = divide(data_ts_sum_pos, data_denominator)

    # 8. 计算 rank(ts_sum(if_else(ts_delta(close, 1) > 0, ts_delta(close, 1), 0), 12) / (ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)), 0), 12) + 1e-6))
    data_rank_ratio = rank(data_ratio, 2)

    # 9. 计算 ts_std_dev(close, 20)
    data_ts_std_dev_close = ts_std_dev(data['close'], 20)

    # 10. 计算 rank(ts_std_dev(close, 20))
    data_rank_std = rank(data_ts_std_dev_close, 2)

    # 11. 计算 rank(ts_sum(if_else(ts_delta(close, 1) > 0, ts_delta(close, 1), 0), 12) / (ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)), 0), 12) + 1e-6)) - rank(ts_std_dev(close, 20))
    factor = subtract(data_rank_ratio, data_rank_std)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()