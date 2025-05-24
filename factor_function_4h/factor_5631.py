import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_rank, ts_delta, log

def factor_5631(data, **kwargs):
    """
    因子名称: VolumeAdjustedPriceTrend_74223
    数学表达式: ts_corr(ts_rank(ts_delta(close, 5), 10), ts_rank(log(vol), 10), 20)
    中文描述: 该因子旨在捕捉价格趋势变化与成交量之间的关系。首先，计算过去5天收盘价的变化量（ts_delta(close, 5)），然后对过去10天该变化量进行排名。同时，计算过去10天成交量取对数后的排名。最后，计算这两个排名在过去20天内的相关性。相较于历史因子，本因子直接关注价格变化而非价格水平，可能更有效地捕捉价格趋势的早期信号。对成交量取对数，能够更有效地捕捉成交量与价格之间的非线性关系。通过观察价格趋势变化与成交量之间的相关性，辅助判断市场情绪和潜在的交易机会。
    因子应用场景：
    1. 趋势识别：通过价格变化与成交量的相关性，识别潜在的趋势反转点。
    2. 市场情绪分析：成交量与价格变化的背离可能预示着市场情绪的变化。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], 5)
    # 2. 计算 ts_rank(ts_delta(close, 5), 10)
    data_ts_rank_delta = ts_rank(data_ts_delta, 10)
    # 3. 计算 log(vol)
    data_log_vol = log(data['vol'])
    # 4. 计算 ts_rank(log(vol), 10)
    data_ts_rank_log_vol = ts_rank(data_log_vol, 10)
    # 5. 计算 ts_corr(ts_rank(ts_delta(close, 5), 10), ts_rank(log(vol), 10), 20)
    factor = ts_corr(data_ts_rank_delta, data_ts_rank_log_vol, 20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()