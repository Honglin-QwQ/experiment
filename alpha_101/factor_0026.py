import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_sum

def factor_0026(data, **kwargs):
    """
    数学表达式: ((0.5 < rank((ts_sum(ts_corr(rank(volume), rank(vwap), 6), 2) / 2.0))) ? (-1 * 1) : 1)
    中文描述: 如果过去6天成交量排名和成交均价排名的相关性之和的2日平均值的排名大于0.5，则赋值-1，否则赋值1，该因子衡量量价关系，可用于构建量价反转策略或趋势跟踪策略，也可用于识别市场情绪。
    因子应用场景：
    1. 量价反转策略：当因子值为-1时，可能表示量价关系出现背离，预示着反转的可能性。
    2. 趋势跟踪策略：当因子值为1时，可能表示量价关系一致，预示着趋势的持续性。
    3. 市场情绪识别：通过观察因子值的变化，可以辅助判断市场情绪的乐观或悲观。
    """
    # 1. 计算 rank(volume)
    rank_volume = rank(data['vol'])
    # 2. 计算 rank(vwap)
    rank_vwap = rank(data['vwap'])
    # 3. 计算 ts_corr(rank(volume), rank(vwap), 6)
    ts_corr_rank_volume_rank_vwap = ts_corr(rank_volume, rank_vwap, 6)
    # 4. 计算 ts_sum(ts_corr(rank(volume), rank(vwap), 6), 2)
    ts_sum_corr = ts_sum(ts_corr_rank_volume_rank_vwap, 2)
    # 5. 计算 (ts_sum(ts_corr(rank(volume), rank(vwap), 6), 2) / 2.0)
    divided_sum_corr = ts_sum_corr / 2.0
    # 6. 计算 rank((ts_sum(ts_corr(rank(volume), rank(vwap), 6), 2) / 2.0))
    rank_divided_sum_corr = rank(divided_sum_corr)

    # 7. 计算 ((0.5 < rank((ts_sum(ts_corr(rank(volume), rank(vwap), 6), 2) / 2.0))) ? (-1 * 1) : 1)
    factor = (rank_divided_sum_corr > 0.5) * -1 + (rank_divided_sum_corr <= 0.5) * 1

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()