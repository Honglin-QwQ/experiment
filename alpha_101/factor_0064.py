import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_sum, ts_min, subtract, multiply, add

def factor_0064(data, **kwargs):
    """
    数学表达式: ((rank(ts_corr(((open * 0.00817205) + (vwap * (1 - 0.00817205))), ts_sum(adv60, 8.6911), 6.40374)) < rank((open - ts_min(open, 13.635)))) * -1)
    中文描述: 1. **详细描述：** 该因子首先计算一个加权平均价格，权重分别为0.00817205和(1-0.00817205)，分别应用于开盘价和成交量加权平均价。然后，计算该加权平均价格与过去8.6911天成交额均值之和的相关系数，窗口期为6.40374天，并对相关系数进行排序。同时，计算开盘价与过去13.635天开盘价最小值之差，并对其进行排序。最后，如果相关系数的排序小于开盘价差值的排序，则赋值为-1，否则为0。该因子试图捕捉价格与成交量之间的关系，并与价格的波动范围进行比较，可能反映了市场情绪和价格趋势的背离或一致性。 2. **因子应用场景：** * **趋势反转策略：** 当因子值为-1时，可能表明价格与成交量的关系异常，预示着趋势可能发生反转。可以结合其他技术指标，构建趋势反转策略。 * **量价关系验证：** 该因子可以用于验证量价关系理论，例如，如果因子持续为正，可能表明量价关系健康，趋势将继续；如果因子频繁变动，可能表明市场不稳定。 * **高频交易信号：** 由于因子计算涉及到高频数据（开盘价、成交量加权平均价），可以将其作为高频交易策略的输入信号，捕捉短期的价格波动。
    """
    # 1. 计算 (open * 0.00817205)
    open_weighted = multiply(data['open'], 0.00817205)
    # 2. 计算 (vwap * (1 - 0.00817205))
    vwap_weighted = multiply(data['vwap'], (1 - 0.00817205))
    # 3. 计算 ((open * 0.00817205) + (vwap * (1 - 0.00817205)))
    price_weighted_sum = add(open_weighted, vwap_weighted)
    # 4. 计算 ts_sum(adv60, 8.6911)  这里没有adv60，使用vol代替
    adv60_sum = ts_sum(data['vol'], 8.6911)
    # 5. 计算 ts_corr(((open * 0.00817205) + (vwap * (1 - 0.00817205))), ts_sum(adv60, 8.6911), 6.40374)
    corr_factor = ts_corr(price_weighted_sum, adv60_sum, 6.40374)
    # 6. 计算 rank(ts_corr(((open * 0.00817205) + (vwap * (1 - 0.00817205))), ts_sum(adv60, 8.6911), 6.40374))
    rank_corr = rank(corr_factor)
    # 7. 计算 ts_min(open, 13.635)
    open_min = ts_min(data['open'], 13.635)
    # 8. 计算 (open - ts_min(open, 13.635))
    open_diff = subtract(data['open'], open_min)
    # 9. 计算 rank((open - ts_min(open, 13.635)))
    rank_open_diff = rank(open_diff)
    # 10. 计算 (rank(ts_corr(((open * 0.00817205) + (vwap * (1 - 0.00817205))), ts_sum(adv60, 8.6911), 6.40374)) < rank((open - ts_min(open, 13.635))))
    factor = (rank_corr < rank_open_diff) * -1

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()