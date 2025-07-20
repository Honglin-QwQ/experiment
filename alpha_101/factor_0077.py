import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_sum, multiply, add, subtract, adv

def factor_0077(data, **kwargs):
    """
    数学表达式: (rank(ts_corr(ts_sum(((low * 0.352233) + (vwap * (1 - 0.352233))), 19.7428), ts_sum(adv40, 19.7428), 6.83313))^rank(ts_corr(rank(vwap), rank(volume), 5.77492))) 
    中文描述: 对数级别成交额和加权平均价的短期相关性排名与加权平均价和成交量的短期相关性排名的乘积。 应用场景：1. 捕捉量价关系变化：该因子结合了成交额、加权平均价和成交量的信息，可以用于识别市场中量价关系的变化，例如，当成交额和价格的相关性较高，而成交量和价格的相关性较低时，可能预示着市场趋势的转变。2. 短期趋势跟踪：该因子可以作为短期趋势跟踪策略的信号，例如，当因子值较高时，可能表明市场处于上升趋势，反之则可能处于下降趋势。3. 异动股票筛选：可以利用该因子筛选出量价关系出现异动的股票，例如，因子值突然大幅上升或下降的股票，可能存在潜在的投资机会。
    """
    # 1. 计算 (low * 0.352233)
    data_low_weighted = multiply(data['low'], 0.352233)
    # 2. 计算 (vwap * (1 - 0.352233))
    data_vwap_weighted = multiply(data['vwap'], (1 - 0.352233))
    # 3. 计算 ((low * 0.352233) + (vwap * (1 - 0.352233)))
    data_sum_weighted = add(data_low_weighted, data_vwap_weighted)
    # 4. 计算 ts_sum(((low * 0.352233) + (vwap * (1 - 0.352233))), 19.7428)
    data_ts_sum1 = ts_sum(data_sum_weighted, d = 19.7428)
    # 5. 计算 adv40
    adv40 = adv(data['vol'],40)
    # 6. 计算 ts_sum(adv40, 19.7428)
    data_ts_sum2 = ts_sum(adv40, d = 19.7428)
    # 7. 计算 ts_corr(ts_sum(((low * 0.352233) + (vwap * (1 - 0.352233))), 19.7428), ts_sum(adv40, 19.7428), 6.83313)
    data_ts_corr1 = ts_corr(data_ts_sum1, data_ts_sum2, d = 6.83313)
    # 8. 计算 rank(ts_corr(ts_sum(((low * 0.352233) + (vwap * (1 - 0.352233))), 19.7428), ts_sum(adv40, 19.7428), 6.83313))
    data_rank1 = rank(data_ts_corr1)
    # 9. 计算 rank(vwap)
    data_rank_vwap = rank(data['vwap'])
    # 10. 计算 rank(volume)
    data_rank_volume = rank(data['vol'])
    # 11. 计算 ts_corr(rank(vwap), rank(volume), 5.77492)
    data_ts_corr2 = ts_corr(data_rank_vwap, data_rank_volume, d = 5.77492)
    # 12. 计算 rank(ts_corr(rank(vwap), rank(volume), 5.77492))
    data_rank2 = rank(data_ts_corr2)
    # 13. 计算 (rank(ts_corr(ts_sum(((low * 0.352233) + (vwap * (1 - 0.352233))), 19.7428), ts_sum(adv40, 19.7428), 6.83313))^rank(ts_corr(rank(vwap), rank(volume), 5.77492)))
    factor = multiply(data_rank1, data_rank2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()