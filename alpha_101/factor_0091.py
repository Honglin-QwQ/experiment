import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_min, ts_rank, ts_decay_linear, divide, add, ts_corr, rank, adv, min

import pandas as pd

def factor_0091(data, **kwargs):
    """
    数学表达式: ts_min(ts_rank(ts_decay_linear(((((high + low) / 2) + close) < (low + open)), 14.7221), 18.8683), ts_rank(ts_decay_linear(ts_corr(rank(low), rank(adv30), 7.58555), 6.94024), 6.80584))
    中文描述: 该因子计算了两个部分之间的最小值，第一部分是过去18.87天内，14.72天线性衰减的((最高价+最低价)/2 + 收盘价)小于(最低价+开盘价)这个布尔值的时间序列排名的最小值；第二部分是过去6.81天内，对过去6.94天线性衰减的，低价的排名与过去30天平均成交额的排名的7.59天相关系数的时间序列排名的最小值。该因子试图捕捉价格和成交量之间的关系，并结合了价格的波动性和趋势信息，通过线性衰减和排名来平滑数据，最终取两部分最小值，可能反映了市场情绪的极端变化。
    应用场景：
    1. 可以用于构建量化交易策略，当因子值较低时，可能预示着超卖，可以考虑买入；当因子值较高时，可能预示着超买，可以考虑卖出。
    2. 可以作为其他复杂因子的输入，与其他因子组合使用，提高模型的预测能力。
    3. 可以用于风险管理，监控市场极端波动情况，辅助判断市场风险。
    """
    # 1. 计算 (high + low) / 2
    high_plus_low = add(data['high'], data['low'])
    mid_price = divide(high_plus_low, 2)

    # 2. 计算 ((high + low) / 2) + close
    mid_price_plus_close = add(mid_price, data['close'])

    # 3. 计算 low + open
    low_plus_open = add(data['low'], data['open'])

    # 4. 计算 (((high + low) / 2) + close) < (low + open)
    condition = mid_price_plus_close < low_plus_open

    # 5. 计算 ts_decay_linear(((((high + low) / 2) + close) < (low + open)), 14.7221)
    decay_linear_1 = ts_decay_linear(condition.astype(float), d=14.7221)

    # 6. 计算 ts_rank(ts_decay_linear(((((high + low) / 2) + close) < (low + open)), 14.7221), 18.8683)
    ts_rank_1 = ts_rank(decay_linear_1, d=18.8683)

    # 7. 计算 rank(low)
    rank_low = rank(data['low'])

    # 8. 计算 adv30
    adv30 = adv(data['vol'],30)

    # 9. 计算 rank(adv30)
    rank_adv30 = rank(adv30)

    # 10. 计算 ts_corr(rank(low), rank(adv30), 7.58555)
    ts_corr_val = ts_corr(rank_low, rank_adv30, d=7.58555)

    # 11. 计算 ts_decay_linear(ts_corr(rank(low), rank(adv30), 7.58555), 6.94024)
    decay_linear_2 = ts_decay_linear(ts_corr_val, d=6.94024)

    # 12. 计算 ts_rank(ts_decay_linear(ts_corr(rank(low), rank(adv30), 7.58555), 6.94024), 6.80584)
    ts_rank_2 = ts_rank(decay_linear_2, d=6.80584)

    # 13. 计算 ts_min(ts_rank(ts_decay_linear(((((high + low) / 2) + close) < (low + open)), 14.7221), 18.8683), ts_rank(ts_decay_linear(ts_corr(rank(low), rank(adv30), 7.58555), 6.94024), 6.80584))
    factor = min(ts_rank_1, ts_rank_2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()