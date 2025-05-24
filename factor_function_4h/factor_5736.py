import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_zscore, ts_delta, divide
import pandas as pd

def factor_5736(data, **kwargs):
    """
    因子名称: VolPriceChangeRankRatio_33177
    数学表达式: divide(ts_rank(ts_zscore(vol, 97), 240), ts_rank(ts_delta(close, 3), 240))
    中文描述: 该因子结合了成交量的标准化变化和收盘价的短期变化，并通过时间序列排名进行比较。首先计算成交量在过去97天的Z分数，衡量当前成交量相对于历史均值的异常程度。然后计算收盘价在过去3天内的变化量。接着，分别计算这两个指标在过去240天内的排名。最后，用成交量Z分数的排名除以收盘价变化量的排名。该因子旨在捕捉在市场波动和交易活跃度异常时，价格变化的相对强度。如果成交量异常活跃（Z分数排名高）且价格变化相对较小（变化量排名低），则因子值可能较高，反之亦然。这可以用于识别潜在的价格反转或趋势延续信号。
    因子应用场景：
    1. 识别潜在的价格反转或趋势延续信号。
    2. 市场波动和交易活跃度异常时，价格变化的相对强度。
    """
    # 1. 计算 ts_zscore(vol, 97)
    data_ts_zscore_vol = ts_zscore(data['vol'], d=97)
    # 2. 计算 ts_rank(ts_zscore(vol, 97), 240)
    data_ts_rank_zscore = ts_rank(data_ts_zscore_vol, d=240)
    # 3. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], d=3)
    # 4. 计算 ts_rank(ts_delta(close, 3), 240)
    data_ts_rank_delta = ts_rank(data_ts_delta_close, d=240)
    # 5. 计算 divide(ts_rank(ts_zscore(vol, 97), 240), ts_rank(ts_delta(close, 3), 240))
    factor = divide(data_ts_rank_zscore, data_ts_rank_delta)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()