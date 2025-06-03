import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_decay_linear, ts_corr, ts_max, rank, add, subtract, multiply, adv, max

def factor_0070(data, **kwargs):
    """
    数学表达式: ts_max(ts_rank(ts_decay_linear(ts_corr(ts_rank(close, 3.43976), ts_rank(adv180, 12.0647), 18.0175), 4.20501), 15.6948), ts_rank(  ts_decay_linear(  (rank( (  (low + open) - (vwap + vwap)  ) )^2  )  , 16.4662), 4.4388  ))
    中文描述: 首先计算过去180天平均成交额，然后计算收盘价和平均成交额在过去18天的秩相关系数，再对相关系数进行15天线性衰减加权，并计算4天排名，同时计算(最低价+开盘价-两倍平均成交价)的平方的16天线性衰减加权，计算4天排名，最后取两个排名的10天最大值。该因子衡量了成交量和价格相关性的变化趋势，以及价格异常波动的大小，可能反映了市场情绪和资金动向，可以用于识别趋势反转、量价背离或超买超卖机会，也可以用于构建量价复合策略。
    因子应用场景：
    1. 趋势反转识别：当因子值达到极端水平时，可能预示着市场趋势即将发生反转。
    2. 量价背离分析：通过观察因子值与价格走势之间的关系，可以发现量价背离现象，从而辅助判断市场是否存在潜在风险。
    3. 超买超卖判断：因子值可以作为判断市场超买超卖状态的指标之一，帮助投资者把握交易时机。
    """
    # 1. 计算adv180
    adv180 = adv(data['vol'],180)

    # 2. 计算ts_rank(close, 3.43976)
    ts_rank_close = ts_rank(data['close'], d=3.43976)

    # 3. 计算ts_rank(adv180, 12.0647)
    ts_rank_adv180 = ts_rank(adv180, d=12.0647)

    # 4. 计算ts_corr(ts_rank(close, 3.43976), ts_rank(adv180, 12.0647), 18.0175)
    ts_corr_factor = ts_corr(ts_rank_close, ts_rank_adv180, d=18.0175)

    # 5. 计算ts_decay_linear(ts_corr(ts_rank(close, 3.43976), ts_rank(adv180, 12.0647), 18.0175), 4.20501)
    ts_decay_linear_factor = ts_decay_linear(ts_corr_factor, d=4.20501)

    # 6. 计算ts_rank(ts_decay_linear(ts_corr(ts_rank(close, 3.43976), ts_rank(adv180, 12.0647), 18.0175), 4.20501), 15.6948)
    ts_rank_factor1 = ts_rank(ts_decay_linear_factor, d=15.6948)

    # 7. 计算(low + open) - (vwap + vwap)
    temp = rank(subtract(add(data['low'], data['open']), add(data['vwap'], data['vwap'])))

    # 8. 计算((low + open) - (vwap + vwap))^2
    temp_squared = multiply(temp, temp)

    # 9. 计算ts_decay_linear((rank(((low + open) - (vwap + vwap)))^2), 16.4662)
    ts_decay_linear_factor2 = ts_decay_linear(temp_squared, d=16.4662)

    # 10. 计算ts_rank(ts_decay_linear((rank(((low + open) - (vwap + vwap)))^2), 16.4662), 4.4388)
    ts_rank_factor2 = ts_rank(ts_decay_linear_factor2, d=4.4388)

    # 11. 计算ts_max( ts_rank(ts_decay_linear(ts_corr(ts_rank(close, 3.43976), ts_rank(adv180, 12.0647), 18.0175), 4.20501), 15.6948), ts_rank(ts_decay_linear((rank(((low + open) - (vwap + vwap)))^2), 16.4662), 4.4388))
    factor = max(ts_rank_factor1, ts_rank_factor2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()