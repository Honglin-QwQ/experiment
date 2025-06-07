import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_decay_linear, ts_corr, ts_rank, ts_min, adv,add,subtract,min

def factor_0087(data, **kwargs):
    """
    数学表达式: ts_min(rank(ts_decay_linear(((rank(open) + rank(low)) - (rank(high) + rank(close))), 8.06882)), ts_rank(ts_decay_linear(ts_corr(ts_rank(close, 8.44728), ts_rank(adv60, 20.6966), 8.01266), 6.65053), 2.61957))
    中文描述: 详细描述：该因子首先计算开盘价和最低价排名的和，以及最高价和收盘价排名的和，然后计算二者之差，并对该差值进行8.06882个周期的线性衰减，再计算衰减结果的排名，并取该排名的过去一段时间内的最小值。同时，计算收盘价在8.44728个周期内的排名，成交额在60日平均值在20.6966个周期内的排名，计算这两个排名的相关性，再对该相关性进行6.65053个周期的线性衰减，计算衰减结果的过去一段时间内的排名，并取该排名的过去2.61957个周期内的排名。最后，取上述两个排名的最小值。这个因子结合了价格动量、成交量和时间衰减的概念，旨在寻找价格行为和成交量变化趋势一致且近期表现较弱的股票。
    因子应用场景：1. 趋势反转策略：寻找超卖股票，当因子值较低时，表明股票可能被低估，可能存在反弹机会。2. 量价共振策略：结合成交量和价格变化，筛选出量价背离或共振的股票，辅助判断趋势的可靠性。3. 动量衰减策略：利用线性衰减捕捉动量逐渐减弱的股票，用于构建风险控制模型或动态调整仓位。
    """
    # 1. 计算 rank(open)
    rank_open = rank(data['open'], rate = 2)
    # 2. 计算 rank(low)
    rank_low = rank(data['low'], rate = 2)
    # 3. 计算 rank(open) + rank(low)
    add_rank_open_rank_low = add(rank_open, rank_low)
    # 4. 计算 rank(high)
    rank_high = rank(data['high'], rate = 2)
    # 5. 计算 rank(close)
    rank_close = rank(data['close'], rate = 2)
    # 6. 计算 rank(high) + rank(close)
    add_rank_high_rank_close = add(rank_high, rank_close)
    # 7. 计算 (rank(open) + rank(low)) - (rank(high) + rank(close))
    subtract_add_rank_open_rank_low_add_rank_high_rank_close = subtract(add_rank_open_rank_low, add_rank_high_rank_close)
    # 8. 计算 ts_decay_linear(((rank(open) + rank(low)) - (rank(high) + rank(close))), 8.06882)
    ts_decay_linear_subtract_add_rank_open_rank_low_add_rank_high_rank_close = ts_decay_linear(subtract_add_rank_open_rank_low_add_rank_high_rank_close, d = 8.06882)
    # 9. 计算 rank(ts_decay_linear(((rank(open) + rank(low)) - (rank(high) + rank(close))), 8.06882))
    rank_ts_decay_linear_subtract_add_rank_open_rank_low_add_rank_high_rank_close = rank(ts_decay_linear_subtract_add_rank_open_rank_low_add_rank_high_rank_close, rate = 2)
    # 10. 计算 ts_min(rank(ts_decay_linear(((rank(open) + rank(low)) - (rank(high) + rank(close))), 8.06882)))
    ts_min_rank_ts_decay_linear_subtract_add_rank_open_rank_low_add_rank_high_rank_close = ts_min(rank_ts_decay_linear_subtract_add_rank_open_rank_low_add_rank_high_rank_close)
    # 11. 计算 adv60
    adv60 = adv(data['vol'], d = 60)
    # 12. 计算 ts_rank(close, 8.44728)
    ts_rank_close = ts_rank(data['close'], d = 8.44728)
    # 13. 计算 ts_rank(adv60, 20.6966)
    ts_rank_adv60 = ts_rank(adv60, d = 20.6966)
    # 14. 计算 ts_corr(ts_rank(close, 8.44728), ts_rank(adv60, 20.6966), 8.01266)
    ts_corr_ts_rank_close_ts_rank_adv60 = ts_corr(ts_rank_close, ts_rank_adv60, d = 8.01266)
    # 15. 计算 ts_decay_linear(ts_corr(ts_rank(close, 8.44728), ts_rank(adv60, 20.6966), 8.01266), 6.65053)
    ts_decay_linear_ts_corr_ts_rank_close_ts_rank_adv60 = ts_decay_linear(ts_corr_ts_rank_close_ts_rank_adv60, d = 6.65053)
    # 16. 计算 ts_rank(ts_decay_linear(ts_corr(ts_rank(close, 8.44728), ts_rank(adv60, 20.6966), 8.01266), 6.65053), 2.61957)
    ts_rank_ts_decay_linear_ts_corr_ts_rank_close_ts_rank_adv60 = ts_rank(ts_decay_linear_ts_corr_ts_rank_close_ts_rank_adv60, d = 2.61957)
    # 17. 计算 ts_min(rank(ts_decay_linear(((rank(open) + rank(low)) - (rank(high) + rank(close))), 8.06882)), ts_rank(ts_decay_linear(ts_corr(ts_rank(close, 8.44728), ts_rank(adv60, 20.6966), 8.01266), 6.65053), 2.61957))
    factor = min(ts_min_rank_ts_decay_linear_subtract_add_rank_open_rank_low_add_rank_high_rank_close, ts_rank_ts_decay_linear_ts_corr_ts_rank_close_ts_rank_adv60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()