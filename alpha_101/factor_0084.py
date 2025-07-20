import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_rank, adv, multiply, add, subtract,divide

def factor_0084(data, **kwargs):
    """
    数学表达式: (rank(ts_corr(((high * 0.876703) + (close * (1 - 0.876703))), adv30, 9.61331))^rank(ts_corr(ts_rank(((high + low) / 2), 3.70596), ts_rank(volume, 10.1595), 7.11408))) 
    中文描述: 该因子计算的是股票一段时间内的价格和成交量之间的关系。首先，它计算了一个价格的加权平均值，高价乘以0.876703加上收盘价乘以(1-0.876703)，然后计算这个加权价格与30日平均成交额在过去9.61331天的相关性，并对这个相关性进行排序。同时，它还计算了过去3.70596天内每日最高价和最低价平均值的排名，以及过去10.1595天成交量的排名，然后计算这两个排名在过去7.11408天的相关性，并对这个相关性进行排序。最后，将这两个排序后的相关性相乘。这个因子试图捕捉价格和成交量之间的联动关系，可能反映了市场对股票的关注度和资金流入情况。
    应用场景： 
    1. **趋势跟踪策略**：该因子可以用来识别价格和成交量同步上涨的股票，这些股票可能处于上升趋势中，可以考虑买入。
    2. **量价背离策略**：如果因子值较低，可能表示价格上涨但成交量没有相应增加，或者价格下跌但成交量反而增加，这可能预示着趋势的反转，可以考虑卖出或做空。
    3. **选股策略**：将该因子与其他基本面或技术指标结合，可以构建更有效的选股模型，例如，选择因子值较高且基本面良好的股票。
    """
    # 1. 计算 (high * 0.876703)
    high_weighted = multiply(data['high'], 0.876703)
    # 2. 计算 (close * (1 - 0.876703))
    close_weighted = multiply(data['close'], (1 - 0.876703))
    # 3. 计算 ((high * 0.876703) + (close * (1 - 0.876703)))
    price_weighted_avg = add(high_weighted, close_weighted)
    del high_weighted, close_weighted
    # 4. 计算 adv30
    adv30 = adv(data['vol'], d=30)
    # 5. 计算 ts_corr(((high * 0.876703) + (close * (1 - 0.876703))), adv30, 9.61331)
    corr1 = ts_corr(price_weighted_avg, adv30, d=9.61331)
    del price_weighted_avg, adv30
    # 6. 计算 rank(ts_corr(((high * 0.876703) + (close * (1 - 0.876703))), adv30, 9.61331))
    rank1 = rank(corr1, rate = 2)
    del corr1
    # 7. 计算 ((high + low) / 2)
    hl_avg = divide(add(data['high'], data['low']), 2)
    # 8. 计算 ts_rank(((high + low) / 2), 3.70596)
    rank_hl_avg = ts_rank(hl_avg, d=3.70596)
    del hl_avg
    # 9. 计算 ts_rank(volume, 10.1595)
    rank_volume = ts_rank(data['vol'], d=10.1595)
    # 10. 计算 ts_corr(ts_rank(((high + low) / 2), 3.70596), ts_rank(volume, 10.1595), 7.11408)
    corr2 = ts_corr(rank_hl_avg, rank_volume, d=7.11408)
    del rank_hl_avg, rank_volume
    # 11. 计算 rank(ts_corr(ts_rank(((high + low) / 2), 3.70596), ts_rank(volume, 10.1595), 7.11408))
    rank2 = rank(corr2, rate = 2)
    del corr2
    # 12. 计算 (rank(ts_corr(((high * 0.876703) + (close * (1 - 0.876703))), adv30, 9.61331))^rank(ts_corr(ts_rank(((high + low) / 2), 3.70596), ts_rank(volume, 10.1595), 7.11408)))
    factor = multiply(rank1, rank2)
    del rank1, rank2

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()