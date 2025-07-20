import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_sum, multiply, subtract, add, divide,adv

def factor_0098(data, **kwargs):
    """
    数学表达式: ((rank(ts_corr(ts_sum(((high + low) / 2), 19.8975), ts_sum(adv60, 19.8975), 8.8136)) < rank(ts_corr(low, volume, 6.28259))) * -1)
    中文描述: 该因子首先计算过去19.8975天内每天高价和低价平均值的总和，以及过去19.8975天内60日平均成交额的总和，然后计算这两个总和在过去8.8136天内的相关性，并对相关性结果进行排序；同时，计算过去6.28259天内每天的低价和成交量的相关性，并对相关性结果进行排序；最后，如果第一个相关性的排序小于第二个相关性的排序，则赋值为-1，否则赋值为0。该因子试图寻找价格与成交量之间关系的变化，可能反映了市场情绪或者资金流动的变化，可以用于构建量化交易策略，例如，当因子值为-1时，可能预示着价格下跌的风险增加，可以考虑卖出或者做空；或者可以与其他因子结合使用，提高选股或者择时的准确性。
    因子应用场景：
    1. 市场情绪判断：通过分析价格和成交量之间的关系，判断市场的乐观或悲观情绪。
    2. 资金流动跟踪：捕捉资金流入流出的迹象，辅助判断股票的买卖时机。
    3. 量化交易策略构建：与其他因子结合，提高选股和择时的准确性。
    """
    # 1. 计算 (high + low) / 2
    data_high_plus_low = add(data['high'], data['low'])
    data_price_avg = divide(data_high_plus_low, 2)

    # 2. 计算 ts_sum(((high + low) / 2), 19.8975)
    data_ts_sum_price_avg = ts_sum(data_price_avg, d=19.8975)

    # 3. 计算 adv60
    data_adv60 = adv(data['vol'],60)

    # 4. 计算 ts_sum(adv60, 19.8975)
    data_ts_sum_adv60 = ts_sum(data_adv60, d=19.8975)

    # 5. 计算 ts_corr(ts_sum(((high + low) / 2), 19.8975), ts_sum(adv60, 19.8975), 8.8136)
    data_ts_corr_1 = ts_corr(data_ts_sum_price_avg, data_ts_sum_adv60, d=8.8136)

    # 6. 计算 rank(ts_corr(ts_sum(((high + low) / 2), 19.8975), ts_sum(adv60, 19.8975), 8.8136))
    data_rank_1 = rank(data_ts_corr_1, rate=2)

    # 7. 计算 ts_corr(low, volume, 6.28259)
    data_ts_corr_2 = ts_corr(data['low'], data['vol'], d=6.28259)

    # 8. 计算 rank(ts_corr(low, volume, 6.28259))
    data_rank_2 = rank(data_ts_corr_2, rate=2)

    # 9. 计算 (rank(ts_corr(...)) < rank(ts_corr(low, volume, 6.28259))) * -1
    condition = data_rank_1 < data_rank_2
    factor = condition.astype(int) * -1

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()