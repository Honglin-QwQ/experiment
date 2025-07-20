import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_min, ts_rank, ts_corr, ts_sum, add, divide, signed_power,adv,subtract

def factor_0094(data, **kwargs):
    """
    数学表达式: (rank((open - ts_min(open, 12.4105))) < ts_rank((rank(ts_corr(ts_sum(((high + low) / 2), 19.1351), ts_sum(adv40, 19.1351), 12.8742))^5), 11.7584)) 
    中文描述: 该因子计算当日开盘价与过去12.4105个周期内最低开盘价差值的排序，然后判断这个排序是否小于过去11.7584个周期内，对一个复杂表达式计算结果的排序。这个复杂表达式是：先计算过去19.1351个周期内每天的最高价和最低价平均值的总和，以及过去19.1351个周期内40日平均成交额的总和，然后计算这两个总和在过去12.8742个周期内的相关系数，再将这个相关系数的5次方进行排序。这个因子试图捕捉开盘价相对过去一段时间最低价的位置，与一个基于量价关系计算出的复杂指标的排序之间的关系。
    应用场景：
    1. 可以用于短线交易策略，当因子值较高时，可能意味着股价有上涨潜力。
    2. 可以与其他技术指标结合使用，例如成交量、均线等，以提高交易信号的准确性。
    3. 可以用于构建量化选股模型，作为其中一个因子，筛选出具有潜在投资价值的股票。
    """
    # 1. 计算 ts_min(open, 12.4105)
    data_ts_min = ts_min(data['open'], d = 12.4105)
    # 2. 计算 open - ts_min(open, 12.4105)
    data_subtract = subtract(data['open'], data_ts_min)
    # 3. 计算 rank(open - ts_min(open, 12.4105))
    data_rank1 = rank(data_subtract)

    # 4. 计算 (high + low) / 2
    data_add = add(data['high'], data['low'])
    data_divide = divide(data_add, 2)
    # 5. 计算 ts_sum(((high + low) / 2), 19.1351)
    data_ts_sum1 = ts_sum(data_divide, d = 19.1351)
    # 6. 计算 adv40
    data['adv40'] = adv(data['vol'],40)
    # 7. 计算 ts_sum(adv40, 19.1351)
    data_ts_sum2 = ts_sum(data['adv40'], d = 19.1351)
    # 8. 计算 ts_corr(ts_sum(((high + low) / 2), 19.1351), ts_sum(adv40, 19.1351), 12.8742)
    data_ts_corr = ts_corr(data_ts_sum1, data_ts_sum2, d = 12.8742)
    # 9. 计算 (ts_corr(ts_sum(((high + low) / 2), 19.1351), ts_sum(adv40, 19.1351), 12.8742))^5
    data_signed_power = signed_power(data_ts_corr, 5)
    # 10. 计算 rank((ts_corr(ts_sum(((high + low) / 2), 19.1351), ts_sum(adv40, 19.1351), 12.8742))^5)
    data_rank2 = rank(data_signed_power)
    # 11. 计算 ts_rank((rank(ts_corr(ts_sum(((high + low) / 2), 19.1351), ts_sum(adv40, 19.1351), 12.8742))^5), 11.7584)
    data_ts_rank = ts_rank(data_rank2, d = 11.7584)

    # 12. 计算 rank((open - ts_min(open, 12.4105))) < ts_rank((rank(ts_corr(ts_sum(((high + low) / 2), 19.1351), ts_sum(adv40, 19.1351), 12.8742))^5), 11.7584))
    factor = (data_rank1 < data_ts_rank).astype(int)

    del data['adv40']
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()