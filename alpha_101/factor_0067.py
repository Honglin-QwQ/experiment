import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_delta, multiply, add, subtract, adv,ts_rank

def factor_0067(data, **kwargs):
    """
    数学表达式: ((ts_rank(ts_corr(rank(high), rank(adv15), 8.91644), 13.9333) < rank(ts_delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157))) * -1) 
    中文描述: 这个因子计算的是一个排序值和另一个排序值的比较结果的负值。首先，计算过去8.91644天内，每天最高价的排名和过去15天平均成交额的排名的相关性，然后对这个相关性结果进行过去13.9333天的排名。同时，计算收盘价乘以0.518371加上最低价乘以(1-0.518371)的加权平均价格，然后计算这个加权平均价格在过去1.06157天的变化量，并对这个变化量进行排名。最后，比较相关性排名和加权平均价格变化量排名的大小，如果相关性排名小于加权平均价格变化量排名，则结果为1，否则为0，并将结果乘以-1。
    应用场景：
    1. 可以用于捕捉价格和成交量之间的异常关系，例如，当价格上涨但成交量萎缩时，可能预示着趋势反转。
    2. 可以用于构建趋势跟踪策略，当相关性排名持续低于价格变化量排名时，可能意味着趋势正在加强。
    3. 可以与其他因子结合使用，提高选股或择时策略的准确性。
    """
    # 计算 rank(high)
    rank_high = rank(data['high'])
    # 计算 adv15
    adv15 = adv(data['vol'],15)
    # 计算 rank(adv15)
    rank_adv15 = rank(adv15)
    # 计算 ts_corr(rank(high), rank(adv15), 8.91644)
    ts_corr_rank_high_rank_adv15 = ts_corr(rank_high, rank_adv15, d=8.91644)
    # 计算 ts_rank(ts_corr(rank(high), rank(adv15), 8.91644), 13.9333)
    ts_rank_ts_corr = ts_rank(ts_corr_rank_high_rank_adv15, d=13.9333)
    # 计算 (close * 0.518371)
    close_multiplied = multiply(data['close'], 0.518371)
    # 计算 (low * (1 - 0.518371))
    low_multiplied = multiply(data['low'], (1 - 0.518371))
    # 计算 ((close * 0.518371) + (low * (1 - 0.518371)))
    weighted_avg_price = add(close_multiplied, low_multiplied)
    # 计算 ts_delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157)
    ts_delta_weighted_avg_price = ts_delta(weighted_avg_price, d=1.06157)
    # 计算 rank(ts_delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157))
    rank_ts_delta = rank(ts_delta_weighted_avg_price)
    # 计算 (ts_rank(ts_corr(rank(high), rank(adv15), 8.91644), 13.9333) < rank(ts_delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157)))
    comparison_result = (ts_rank_ts_corr < rank_ts_delta).astype(int)
    # 计算 ((ts_rank(ts_corr(rank(high), rank(adv15), 8.91644), 13.9333) < rank(ts_delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157))) * -1)
    factor = multiply(comparison_result, -1)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()