import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_min, ts_rank, ts_corr, multiply

def factor_0093(data, **kwargs):
    """
    数学表达式: ((rank((vwap - ts_min(vwap, 11.5783)))^ts_rank(ts_corr(ts_rank(vwap, 19.6462), ts_rank(adv60, 4.02992), 18.0926), 2.70756)) * -1)
    中文描述: 该因子首先计算过去11.5783天内每天的成交量加权平均价(vwap)的最小值，然后用当天的vwap减去这个最小值，并对结果进行排序，得到一个排序值。接着，计算过去19.6462天vwap的排序值与过去4.02992天平均成交额(adv60)的排序值之间的相关性，再对这个相关性进行过去2.70756天的排序。最后，将前述vwap差值的排序值与相关性排序值相乘，并将结果取反。这个因子试图捕捉价格相对于近期低点的强度，并结合量价关系的变化趋势，反向操作。
    应用场景：
    1. 短期反转策略：当因子值较高时，可能意味着价格短期内过度上涨，预期价格回调，可以考虑卖出；反之，因子值较低时，预期价格反弹，可以考虑买入。
    2. 量价共振分析：该因子结合了价格和成交量的关系，可以用于识别量价背离或共振的情况，辅助判断趋势的可靠性。
    3. 趋势跟踪策略的过滤：该因子可以作为趋势跟踪策略的过滤条件，避免在趋势较弱或反转风险较高时入场。
    """
    # 1. 计算 ts_min(vwap, 11.5783)
    data_ts_min_vwap = ts_min(data['vwap'], d = 11.5783)
    # 2. 计算 (vwap - ts_min(vwap, 11.5783))
    data_subtract = data['vwap'] - data_ts_min_vwap
    # 3. 计算 rank((vwap - ts_min(vwap, 11.5783)))
    data_rank = rank(data_subtract, rate = 2)
    # 4. 计算 ts_rank(vwap, 19.6462)
    data_ts_rank_vwap = ts_rank(data['vwap'], d = 19.6462)
    # 5. 计算 ts_rank(adv60, 4.02992)
    data_adv60 = data['amount']/data['vol']
    data_ts_rank_adv60 = ts_rank(data_adv60, d = 4.02992)
    # 6. 计算 ts_corr(ts_rank(vwap, 19.6462), ts_rank(adv60, 4.02992), 18.0926)
    data_ts_corr = ts_corr(data_ts_rank_vwap, data_ts_rank_adv60, d = 18.0926)
    # 7. 计算 ts_rank(ts_corr(ts_rank(vwap, 19.6462), ts_rank(adv60, 4.02992), 18.0926), 2.70756)
    data_ts_rank_corr = ts_rank(data_ts_corr, d = 2.70756)
    # 8. 计算 (rank((vwap - ts_min(vwap, 11.5783)))^ts_rank(ts_corr(ts_rank(vwap, 19.6462), ts_rank(adv60, 4.02992), 18.0926), 2.70756))
    factor = data_rank ** data_ts_rank_corr
    # 9. 计算 ((rank((vwap - ts_min(vwap, 11.5783)))^ts_rank(ts_corr(ts_rank(vwap, 19.6462), ts_rank(adv60, 4.02992), 18.0926), 2.70756)) * -1)
    factor = factor * -1

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()