import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_decay_linear, ts_corr, rank, indneutralize, adv, multiply, subtract

def factor_0090(data, **kwargs):
    """
    数学表达式: ((ts_rank(ts_decay_linear(ts_decay_linear(ts_corr(indneutralize(close, IndClass.industry), volume, 9.74928), 16.398), 3.83219), 4.8667) - rank(ts_decay_linear(ts_corr(vwap, adv30, 4.01303), 2.6809))) * -1)
    中文描述: 这个因子计算的是一个排序反转的指标，它结合了行业中性化后的收益率与成交量的相关性、成交额与成交量的相关性，然后对这些相关性进行时间衰减和排序。具体来说，首先计算经过行业中性化处理的收盘价与成交量在过去大约10天内的相关性，然后对这个相关性进行两次时间衰减，分别以大约16天和4天为周期。接着，计算成交额与过去30天平均成交额在过去大约4天内的相关性，并进行一次大约3天的时间衰减。然后，分别对这两个时间衰减后的相关性进行排序，一个排序周期大约为5天，另一个是横截面排序。最后，将这两个排序结果相减，取相反数，得到最终的因子值。这个因子可能捕捉了市场中一些反转效应，即当行业中性化收益率与成交量的相关性较高，而成交额与成交量的相关性较低时，可能预示着价格下跌；反之，可能预示着价格上涨。
    因子应用场景包括：
    1. 短期反转策略：当因子值较高时，做空股票；当因子值较低时，做多股票。
    2. 动量策略的辅助指标：结合动量因子，在动量较弱且因子值较高时，做空股票；在动量较强且因子值较低时，做多股票。
    3. 风险控制：当因子值在整个股票池中分布极端时，可能预示着市场风险较高，可以适当降低仓位。
    """
    # 1. indneutralize(close, IndClass.industry)
    ind_neutralize = indneutralize(data['close'], data['industry'])

    # 2. ts_corr(indneutralize(close, IndClass.industry), volume, 9.74928)
    ts_corr_1 = ts_corr(ind_neutralize, data['vol'], 9.74928)

    # 3. ts_decay_linear(ts_corr(indneutralize(close, IndClass.industry), volume, 9.74928), 16.398)
    ts_decay_linear_1 = ts_decay_linear(ts_corr_1, 16.398)

    # 4. ts_decay_linear(ts_decay_linear(ts_corr(indneutralize(close, IndClass.industry), volume, 9.74928), 16.398), 3.83219)
    ts_decay_linear_2 = ts_decay_linear(ts_decay_linear_1, 3.83219)

    # 5. ts_rank(ts_decay_linear(ts_decay_linear(ts_corr(indneutralize(close, IndClass.industry), volume, 9.74928), 16.398), 3.83219), 4.8667)
    ts_rank_1 = ts_rank(ts_decay_linear_2, 4.8667)

    # 6. adv30
    adv30_data = adv(data['amount'],30)

    # 7. ts_corr(vwap, adv30, 4.01303)
    ts_corr_2 = ts_corr(data['vwap'], adv30_data, 4.01303)

    # 8. ts_decay_linear(ts_corr(vwap, adv30, 4.01303), 2.6809)
    ts_decay_linear_3 = ts_decay_linear(ts_corr_2, 2.6809)

    # 9. rank(ts_decay_linear(ts_corr(vwap, adv30, 4.01303), 2.6809))
    rank_1 = rank(ts_decay_linear_3)

    # 10. ts_rank(ts_decay_linear(ts_decay_linear(ts_corr(indneutralize(close, IndClass.industry), volume, 9.74928), 16.398), 3.83219), 4.8667) - rank(ts_decay_linear(ts_corr(vwap, adv30, 4.01303), 2.6809))
    sub = subtract(ts_rank_1, rank_1)

    # 11. (ts_rank(ts_decay_linear(ts_decay_linear(ts_corr(indneutralize(close, IndClass.industry), volume, 9.74928), 16.398), 3.83219), 4.8667) - rank(ts_decay_linear(ts_corr(vwap, adv30, 4.01303), 2.6809))) * -1
    factor = multiply(sub, -1)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()