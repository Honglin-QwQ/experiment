import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_max, multiply

def factor_0049(data, **kwargs):
    """
    数学表达式: (-1 * ts_max(rank(ts_corr(rank(volume), rank(vwap), 5)), 5))
    中文描述: 该因子计算过去5天成交量和成交均价相关性的排序，取过去5天该排序的最大值，然后取负。这意味着寻找过去5天成交量和成交均价相关性最弱（负相关性最强）的股票，并对这些股票进行排序，数值越小代表负相关性越强。
    应用场景：
    1. 识别价格与成交量背离的股票，可能预示着趋势反转。
    2. 短期反转策略，当因子值较小时，买入；因子值较大时，卖出。
    3. 结合其他量价因子，提高选股模型的准确性。
    """
    # 1. 计算 rank(volume)
    rank_volume = rank(data['vol'])
    # 2. 计算 rank(vwap)
    rank_vwap = rank(data['vwap'])
    # 3. 计算 ts_corr(rank(volume), rank(vwap), 5)
    ts_corr_rank_volume_rank_vwap = ts_corr(rank_volume, rank_vwap, 5)
    # 4. 计算 rank(ts_corr(rank(volume), rank(vwap), 5))
    rank_ts_corr = rank(ts_corr_rank_volume_rank_vwap)
    # 5. 计算 ts_max(rank(ts_corr(rank(volume), rank(vwap), 5)), 5)
    ts_max_rank_ts_corr = ts_max(rank_ts_corr, 5)
    # 6. 计算 -1 * ts_max(rank(ts_corr(rank(volume), rank(vwap), 5)), 5)
    factor = multiply(-1, ts_max_rank_ts_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()