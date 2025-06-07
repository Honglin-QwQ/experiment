import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_decay_linear, ts_corr, ts_delta, indneutralize, adv, subtract, multiply, add
import pandas as pd


def factor_0088(data, **kwargs):
    """
    数学表达式: (ts_rank(ts_decay_linear(ts_corr(((low * 0.967285) + (low * (1 - 0.967285))), adv10, 6.94279), 5.51607), 3.79744) - ts_rank(ts_decay_linear(ts_delta(indneutralize(vwap, IndClass.industry), 3.48158), 10.1466), 15.3012))
    中文描述: 该因子计算了两个部分的差值。第一部分是：先计算过去6.94天内，当前低价乘以0.967和当前低价乘以0.033与过去10天平均成交额的相关性，然后对这个相关性进行过去5.52天线性衰减，再计算过去3.8天衰减值的排名。第二部分是：先计算行业中性化后的成交量加权平均价与3.48天前的差值，然后对这个差值进行过去10.15天线性衰减，再计算过去15.3天衰减值的排名。最后，用第一部分的排名减去第二部分的排名。这个因子试图捕捉低价与成交量之间的关系，并结合行业中性化后的价格变化信息，通过排名来标准化数据。
    因子应用场景：
    1. 可以用于构建量化选股模型，寻找低价与成交量关系异常的股票。
    2. 可以用于短线交易策略，捕捉价格短期反转的机会。
    3. 可以用于风险管理，识别市场情绪极端化的股票。
    """
    # 第一部分
    # 1. 计算 (low * 0.967285)
    low_0967285 = multiply(data['low'], 0.967285)
    # 2. 计算 (low * (1 - 0.967285))
    low_0032715 = multiply(data['low'], (1 - 0.967285))
    # 3. 计算 ((low * 0.967285) + (low * (1 - 0.967285)))
    low_combined = add(low_0967285, low_0032715)
    # 4. 计算 adv10
    adv10 = adv(data['vol'])
    # 5. 计算 ts_corr(((low * 0.967285) + (low * (1 - 0.967285))), adv10, 6.94279)
    ts_corr_low_adv10 = ts_corr(low_combined, adv10, 7)
    # 6. 计算 ts_decay_linear(ts_corr(((low * 0.967285) + (low * (1 - 0.967285))), adv10, 6.94279), 5.51607)
    ts_decay_linear_corr = ts_decay_linear(ts_corr_low_adv10, 6)
    # 7. 计算 ts_rank(ts_decay_linear(ts_corr(((low * 0.967285) + (low * (1 - 0.967285))), adv10, 6.94279), 5.51607), 3.79744)
    ts_rank_decay_corr = ts_rank(ts_decay_linear_corr, 4)

    # 第二部分
    # 1. 计算 indneutralize(vwap, IndClass.industry)
    ind_neutralize_vwap = indneutralize(data['vwap'], data['industry'])
    # 2. 计算 ts_delta(indneutralize(vwap, IndClass.industry), 3.48158)
    ts_delta_ind_vwap = ts_delta(ind_neutralize_vwap, 3)
    # 3. 计算 ts_decay_linear(ts_delta(indneutralize(vwap, IndClass.industry), 3.48158), 10.1466)
    ts_decay_linear_delta = ts_decay_linear(ts_delta_ind_vwap, 10)
    # 4. 计算 ts_rank(ts_decay_linear(ts_delta(indneutralize(vwap, IndClass.industry), 3.48158), 10.1466), 15.3012)
    ts_rank_decay_delta = ts_rank(ts_decay_linear_delta, 15)

    # 计算差值
    factor = subtract(ts_rank_decay_corr, ts_rank_decay_delta)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()