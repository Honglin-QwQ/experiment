import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_sum, add, divide,adv

def factor_0061(data, **kwargs):
    """
    数学表达式: ((rank(ts_corr(vwap, ts_sum(adv20, 22.4101), 9.91009)) < rank(((rank(open) + rank(open)) < (rank(((high + low) / 2)) + rank(high))))) * -1)
    中文描述: 描述：该因子首先计算过去9.91天成交量加权平均价(vwap)与过去22.41天平均成交额(adv20)之和的相关系数，然后对相关系数进行排序。同时，计算开盘价排序的加和，以及最高价和最低价均值与最高价排序的加和，比较这两个加和的大小。如果相关系数的排序小于两个加和比较结果的排序，则赋值为-1，否则为0。该因子试图捕捉量价关系与价格本身波动之间的关系，当成交量和成交额的相关性较低，且开盘价相对较弱时，因子值为-1。
    应用场景：
    1. 可以作为反转策略的信号，当因子值为-1时，可能预示着股价超跌，短期内可能反弹。
    2. 可以与其他因子结合，例如动量因子，形成更稳健的选股策略。
    3. 可以用于识别异常波动股票，因子值变化剧烈可能表明市场对该股票的看法发生转变。
    """
    # 计算adv20
    adv20 = adv(data['vol'],20)
    data['adv20'] = adv20
    # 1. 计算 ts_sum(adv20, 22.4101)
    data_ts_sum = ts_sum(data['adv20'], d=22)
    # 2. 计算 ts_corr(vwap, ts_sum(adv20, 22.4101), 9.91009)
    data_ts_corr = ts_corr(data['vwap'], data_ts_sum, d=10)
    # 3. 计算 rank(ts_corr(vwap, ts_sum(adv20, 22.4101), 9.91009))
    rank_ts_corr = rank(data_ts_corr, rate = 2)
    # 4. 计算 rank(open)
    rank_open1 = rank(data['open'], rate = 2)
    # 5. 计算 rank(open)
    rank_open2 = rank(data['open'], rate = 2)
    # 6. 计算 rank(open) + rank(open)
    sum_rank_open = add(rank_open1, rank_open2)
    # 7. 计算 (high + low) / 2
    high_low_mean = divide(add(data['high'], data['low']), 2)
    # 8. 计算 rank((high + low) / 2)
    rank_high_low_mean = rank(high_low_mean, rate = 2)
    # 9. 计算 rank(high)
    rank_high = rank(data['high'], rate = 2)
    # 10. 计算 rank(((high + low) / 2)) + rank(high)
    sum_rank_high_low = add(rank_high_low_mean, rank_high)
    # 11. 计算 (rank(open) + rank(open)) < (rank(((high + low) / 2)) + rank(high))
    condition = (sum_rank_open < sum_rank_high_low)
    # 12. 计算 rank(((rank(open) + rank(open)) < (rank(((high + low) / 2)) + rank(high)))))
    rank_condition = rank(condition.astype(float), rate = 2)
    # 13. 计算 (rank(ts_corr(vwap, ts_sum(adv20, 22.4101), 9.91009)) < rank(((rank(open) + rank(open)) < (rank(((high + low) / 2)) + rank(high)))))
    final_condition = (rank_ts_corr < rank_condition)
    # 14. 计算 ((rank(ts_corr(vwap, ts_sum(adv20, 22.4101), 9.91009)) < rank(((rank(open) + rank(open)) < (rank(((high + low) / 2)) + rank(high))))) * -1)
    factor = final_condition.astype(int) * -1

    # 删除中间变量
    del data['adv20']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()