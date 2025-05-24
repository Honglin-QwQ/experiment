import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_sum, if_else, ts_delta, ts_rank, abs, multiply

import pandas as pd

def factor_5664(data, **kwargs):
    """
    因子名称: factor_0002_63254
    数学表达式: ts_sum(if_else(ts_delta(close, 1) > 0, ts_delta(close, 1) * vol * ts_rank(high, d=5), 0), d=20) / ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)) * vol * ts_rank(low, d=5), 0), d=20)
    中文描述: 该因子是对factor_0001的改进，旨在更精确地衡量市场上涨和下跌的强度。它计算过去20天内上涨交易量与下跌交易量的比率，但引入了ts_rank(high, d=5)和ts_rank(low, d=5)来量化上涨和下跌的强度。具体来说，当收盘价上涨时，将上涨幅度乘以成交量和过去5天最高价的排名；当收盘价下跌时，将下跌幅度乘以成交量和过去5天最低价的排名。通过引入最高价和最低价的排名，该因子能够更敏感地捕捉市场情绪的变化，从而更准确地识别趋势反转点。创新之处在于将价格变化、成交量和价格波动范围相结合，以期更全面地反映市场动态。
    因子应用场景：
    1. 趋势识别：该因子可以帮助识别市场上涨和下跌的强度，从而辅助判断市场趋势。
    2. 反转点识别：通过捕捉市场情绪的变化，该因子可能有助于识别趋势反转点。
    """

    # 1. 计算 ts_delta(close, 1)
    delta_close = ts_delta(data['close'], d=1)

    # 2. 计算 ts_rank(high, d=5)
    rank_high = ts_rank(data['high'], d=5)

    # 3. 计算 ts_rank(low, d=5)
    rank_low = ts_rank(data['low'], d=5)

    # 4. 计算 if_else(ts_delta(close, 1) > 0, ts_delta(close, 1) * vol * ts_rank(high, d=5), 0)
    condition_up = delta_close > 0
    up_volume = if_else(condition_up, multiply(delta_close, data['vol'], rank_high), 0)

    # 5. 计算 if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)) * vol * ts_rank(low, d=5), 0)
    condition_down = delta_close < 0
    down_volume = if_else(condition_down, multiply(abs(delta_close), data['vol'], rank_low), 0)

    # 6. 计算 ts_sum(if_else(ts_delta(close, 1) > 0, ts_delta(close, 1) * vol * ts_rank(high, d=5), 0), d=20)
    sum_up_volume = ts_sum(up_volume, d=20)

    # 7. 计算 ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)) * vol * ts_rank(low, d=5), 0), d=20)
    sum_down_volume = ts_sum(down_volume, d=20)

    # 8. 计算 ts_sum(if_else(ts_delta(close, 1) > 0, ts_delta(close, 1) * vol * ts_rank(high, d=5), 0), d=20) / ts_sum(if_else(ts_delta(close, 1) < 0, abs(ts_delta(close, 1)) * vol * ts_rank(low, d=5), 0), d=20)
    factor = sum_up_volume / sum_down_volume

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()