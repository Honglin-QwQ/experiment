import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_min, rank, ts_decay_linear, ts_corr, add, divide, subtract,adv,min

def factor_0076(data, **kwargs):
    """
    数学表达式: ts_min(rank(ts_decay_linear(((((high + low) / 2) + high) - (vwap + high)), 20.0451)), rank(ts_decay_linear(ts_corr(((high + low) / 2), adv40, 3.1614), 5.64125)))
    中文描述: 这个因子计算了两个排序值的最小值。第一个排序值是过去20天左右的((最高价+最低价)/2 + 最高价) - (量价平均价格 + 最高价)的线性衰减值的排名。第二个排序值是过去5天左右的成交量40日均值和((最高价+最低价)/2)的3天左右相关性的线性衰减值的排名。这个因子可能捕捉了价格和成交量的短期变化趋势，以及它们之间的相关性，并对这些趋势进行了排序和综合。
    因子应用场景：
    1. 可以用于构建量化选股模型，选择短期内价格和成交量关系发生显著变化的股票。
    2. 可以用于高频交易策略，捕捉日内价格和成交量的微小变化。
    3. 可以与其他因子结合，提高选股或交易策略的稳健性。
    """
    # 1. 计算 (high + low) / 2
    high_plus_low = add(data['high'], data['low'])
    mid_price = divide(high_plus_low, 2)

    # 2. 计算 ((high + low) / 2) + high
    mid_price_plus_high = add(mid_price, data['high'])

    # 3. 计算 adv40
    adv40 = adv(data['vol'], d = 40)

    # 4. 计算 vwap + high
    vwap_plus_high = add(data['vwap'], data['high'])

    # 5. 计算 (((high + low) / 2) + high) - (vwap + high)
    price_diff = subtract(mid_price_plus_high, vwap_plus_high)

    # 6. 计算 ts_decay_linear(((((high + low) / 2) + high) - (vwap + high)), 20.0451)
    decay_linear_price = ts_decay_linear(price_diff, d = 20.0451)

    # 7. 计算 rank(ts_decay_linear(((((high + low) / 2) + high) - (vwap + high)), 20.0451))
    rank_price = rank(decay_linear_price)

    # 8. 计算 ts_corr(((high + low) / 2), adv40, 3.1614)
    corr_price_volume = ts_corr(mid_price, adv40, d = 3.1614)

    # 9. 计算 ts_decay_linear(ts_corr(((high + low) / 2), adv40, 3.1614), 5.64125)
    decay_linear_corr = ts_decay_linear(corr_price_volume, d = 5.64125)

    # 10. 计算 rank(ts_decay_linear(ts_corr(((high + low) / 2), adv40, 3.1614), 5.64125))
    rank_corr = rank(decay_linear_corr)

    # 11. 计算 ts_min(rank(ts_decay_linear(((((high + low) / 2) + high) - (vwap + high)), 20.0451)), rank(ts_decay_linear(ts_corr(((high + low) / 2), adv40, 3.1614), 5.64125)))
    factor = min(rank_price, rank_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()