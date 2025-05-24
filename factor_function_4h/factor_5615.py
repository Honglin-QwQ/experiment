import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_delta, rank, ts_rank, ts_corr, ts_returns

import pandas as pd
import numpy as np

def factor_5615(data, **kwargs):
    """
    数学表达式: ts_zscore(ts_delta(close, 3), 240) + rank(ts_delta(low, 1)) + ts_rank(ts_corr(low, ts_returns(close,1), 20), 5)
    中文描述: 该因子结合了价格变化的标准分数、最低价的变化排名以及最低价与收益率相关性的时间序列排名。第一部分ts_zscore(ts_delta(close, 3), 240)衡量了收盘价短期变化的异常程度。第二部分rank(ts_delta(low, 1))捕捉了每日最低价变动的相对位置。第三部分ts_rank(ts_corr(low, ts_returns(close,1), 20), 5)捕捉了每日最低价和日收益率之间历史相关性的相对位置。该因子旨在综合考虑价格的短期波动、最低价的变动以及价格与收益率之间的关系，从而更全面地评估股票的潜在投资价值。
    因子应用场景：
    1. 异常波动检测：通过ts_zscore识别收盘价的异常波动。
    2. 最低价变动分析：通过rank(ts_delta(low, 1))评估最低价变动的相对位置。
    3. 价格与收益率关系：通过ts_rank(ts_corr(low, ts_returns(close,1), 20), 5)捕捉最低价和收益率之间的相关性。
    """
    # 1. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], 3)
    # 2. 计算 ts_zscore(ts_delta(close, 3), 240)
    data_ts_zscore = ts_zscore(data_ts_delta_close, 240)
    # 3. 计算 ts_delta(low, 1)
    data_ts_delta_low = ts_delta(data['low'], 1)
    # 4. 计算 rank(ts_delta(low, 1))
    data_rank = rank(data_ts_delta_low, 2)
    # 5. 计算 ts_returns(close, 1)
    data_ts_returns = ts_returns(data['close'], 1)
    # 6. 计算 ts_corr(low, ts_returns(close,1), 20)
    data_ts_corr = ts_corr(data['low'], data_ts_returns, 20)
    # 7. 计算 ts_rank(ts_corr(low, ts_returns(close,1), 20), 5)
    data_ts_rank = ts_rank(data_ts_corr, 5)
    # 8. 计算 ts_zscore(ts_delta(close, 3), 240) + rank(ts_delta(low, 1)) + ts_rank(ts_corr(low, ts_returns(close,1), 20), 5)
    factor = data_ts_zscore + data_rank + data_ts_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()