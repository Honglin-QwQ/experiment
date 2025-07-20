import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_decay_linear, ts_delta, ts_rank, subtract, multiply, add, divide

def factor_0065(data, **kwargs):
    """
    数学表达式: ((rank(ts_decay_linear(ts_delta(vwap, 3.51013), 7.23052)) + ts_rank(ts_decay_linear(((((low * 0.96633) + (low * (1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157), 6.72611)) * -1)
    中文描述: 该因子计算了股票成交量加权平均价（vwap）短期变化的线性衰减排名，加上一个基于当日最低价、开盘价、最高价和vwap计算的复杂价格偏离指标的线性衰减排名，然后取负。这个因子试图捕捉短期价格动量和价格偏离程度，并通过排名进行标准化，最后取负值，可能意味着寻找超卖或潜在反转的机会。
    因子应用场景：
    1. 短线反转策略：寻找因子值较低的股票，认为其可能被低估，短期内有反弹机会。
    2. 动量衰减策略：结合其他动量指标，判断动量是否过热，因子值持续走高可能预示动量即将减弱。
    3. 异常价格检测：因子值异常波动可能提示市场对该股票的定价存在偏差，需要进一步分析。
    """
    # 1. 计算 ts_delta(vwap, 3.51013)
    data_ts_delta_vwap = ts_delta(data['vwap'], 3.51013)
    # 2. 计算 ts_decay_linear(ts_delta(vwap, 3.51013), 7.23052)
    data_ts_decay_linear_delta = ts_decay_linear(data_ts_delta_vwap, 7.23052)
    # 3. 计算 rank(ts_decay_linear(ts_delta(vwap, 3.51013), 7.23052))
    data_rank_decay_linear_delta = rank(data_ts_decay_linear_delta)

    # 4. 计算 (low * 0.96633)
    data_low_096633 = multiply(data['low'], 0.96633)
    # 5. 计算 (low * (1 - 0.96633))
    data_low_1_096633 = multiply(data['low'], (1 - 0.96633))
    # 6. 计算 ((low * 0.96633) + (low * (1 - 0.96633)))
    data_add_low = add(data_low_096633, data_low_1_096633)
    # 7. 计算 (((low * 0.96633) + (low * (1 - 0.96633))) - vwap)
    data_sub_vwap = subtract(data_add_low, data['vwap'])
    # 8. 计算 ((high + low) / 2)
    data_high_low = divide(add(data['high'], data['low']), 2)
    # 9. 计算 (open - ((high + low) / 2))
    data_open_high_low = subtract(data['open'], data_high_low)
    # 10. 计算 ((((low * 0.96633) + (low * (1 - 0.96633))) - vwap) / (open - ((high + low) / 2)))
    data_price_deviation = divide(data_sub_vwap, data_open_high_low)
    # 11. 计算 ts_decay_linear(((((low * 0.96633) + (low * (1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157)
    data_ts_decay_linear_deviation = ts_decay_linear(data_price_deviation, 11.4157)
    # 12. 计算 ts_rank(ts_decay_linear(((((low * 0.96633) + (low * (1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157), 6.72611)
    data_ts_rank_decay_linear = ts_rank(data_ts_decay_linear_deviation, 6.72611)

    # 13. 计算 (rank(ts_decay_linear(ts_delta(vwap, 3.51013), 7.23052)) + ts_rank(ts_decay_linear(((((low * 0.96633) + (low * (1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157), 6.72611))
    data_add_rank_tsrank = add(data_rank_decay_linear_delta, data_ts_rank_decay_linear)

    # 14. 计算 ((rank(ts_decay_linear(ts_delta(vwap, 3.51013), 7.23052)) + ts_rank(ts_decay_linear(((((low * 0.96633) + (low * (1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157), 6.72611)) * -1)
    factor = multiply(data_add_rank_tsrank, -1)

    del data_ts_delta_vwap
    del data_ts_decay_linear_delta
    del data_rank_decay_linear_delta
    del data_low_096633
    del data_low_1_096633
    del data_add_low
    del data_sub_vwap
    del data_high_low
    del data_open_high_low
    del data_price_deviation
    del data_ts_decay_linear_deviation
    del data_ts_rank_decay_linear
    del data_add_rank_tsrank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()