import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_sum, ts_delay, ts_min

import pandas as pd
import numpy as np

def factor_0023(data, **kwargs):
    """
    数学表达式: ((((ts_delta((ts_sum(close, 100) / 100), 100) / ts_delay(close, 100)) < 0.05) || ((ts_delta((ts_sum(close, 100) / 100), 100) / ts_delay(close, 100)) == 0.05)) ? (-1 * (close - ts_min(close, 100))) : (-1 * ts_delta(close, 3)))
    中文描述: 该因子首先计算过去100天收盘价的平均值，然后计算该平均值100天后的变化量，再除以100天前的收盘价，如果这个比率小于等于0.05，则取负的（当前收盘价减去过去100天收盘价的最小值），否则取负的过去3天收盘价的变化量。这个因子试图捕捉价格趋势变化，如果过去100天平均价格的长期变化率较低，则关注短期价格与长期最低价的偏离程度；如果长期变化率较高，则关注短期价格变化。
    因子应用场景：
    1. 可以作为趋势反转策略的信号，当因子值为正且较大时，可能预示着下跌趋势的反转。
    2. 可以结合其他技术指标，如成交量，形成更复杂的交易规则，例如，当因子值与成交量同时放大时，可能是一个更强的买入或卖出信号。
    3. 可以用于构建量化选股模型，选择因子值较低的股票，预期这些股票可能具有更高的上涨潜力。
    """
    # 计算 ts_sum(close, 100)
    ts_sum_close_100 = ts_sum(data['close'], 100)

    # 计算 (ts_sum(close, 100) / 100)
    avg_close_100 = ts_sum_close_100 / 100

    # 计算 ts_delta((ts_sum(close, 100) / 100), 100)
    ts_delta_avg_100_100 = ts_delta(avg_close_100, 100)

    # 计算 ts_delay(close, 100)
    ts_delay_close_100 = ts_delay(data['close'], 100)

    # 计算 (ts_delta((ts_sum(close, 100) / 100), 100) / ts_delay(close, 100))
    ratio = ts_delta_avg_100_100 / ts_delay_close_100

    # 计算 (ts_delta((ts_sum(close, 100) / 100), 100) / ts_delay(close, 100)) < 0.05
    condition1 = ratio < 0.05

    # 计算 (ts_delta((ts_sum(close, 100) / 100), 100) / ts_delay(close, 100)) == 0.05
    condition2 = ratio == 0.05

    # 计算 condition1 || condition2
    condition = condition1 | condition2

    # 计算 ts_min(close, 100)
    ts_min_close_100 = ts_min(data['close'], 100)

    # 计算 (close - ts_min(close, 100))
    close_minus_min = data['close'] - ts_min_close_100

    # 计算 -1 * (close - ts_min(close, 100))
    true_value = -1 * close_minus_min

    # 计算 ts_delta(close, 3)
    ts_delta_close_3 = ts_delta(data['close'], 3)

    # 计算 -1 * ts_delta(close, 3)
    false_value = -1 * ts_delta_close_3

    # 使用条件表达式
    factor = np.where(condition, true_value, false_value)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()