import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_min, subtract, multiply,indneutralize,adv
import pandas as pd

def factor_0066(data, **kwargs):
    """
    数学表达式: ((rank((high - ts_min(high, 2.14593)))^rank(ts_corr(indneutralize(vwap, IndClass.sector), indneutralize(adv20, IndClass.subindustry), 6.02936))) * -1)
    中文描述: 该因子首先计算过去2.14593天内最高价的最小值，并用当日最高价减去该最小值，然后对结果进行排序。同时，计算行业中性化的成交额（vwap）与子行业中性化的过去20天平均成交额（adv20）在过去6.02936天内的相关性，并对相关性进行排序。最后，将两个排序结果相乘，再乘以-1得到最终因子值。该因子试图捕捉价格短期波动与成交量相关性之间的反向关系，可能反映了市场情绪或资金流动的变化。
    因子应用场景包括：
    1. 识别价格短期超跌但成交量并未同步下降的股票，可能预示反弹机会。
    2. 结合其他技术指标，构建量化选股模型，筛选出具有潜在上涨动力的股票。
    3. 用于高频交易策略，捕捉日内价格波动与成交量变化之间的微小差异。
    """
    # 1. 计算 ts_min(high, 2.14593)
    data_ts_min_high = ts_min(data['high'],2.14593)

    # 2. 计算 high - ts_min(high, 2.14593)
    data_subtract_high_ts_min = subtract(data['high'], data_ts_min_high)

    # 3. 计算 rank(high - ts_min(high, 2.14593))
    data_rank_high_subtract_ts_min = rank(data_subtract_high_ts_min)

    # 4. 计算 indneutralize(vwap, IndClass.sector)

    data['indneutralize_vwap_sector'] = indneutralize(data['vwap'],data['industry'])

    # 5. 计算 adv20
    data['adv20'] = adv(data['vol'],20)

    # 6. 计算 indneutralize(adv20, IndClass.subindustry)
    data['indneutralize_adv20_subindustry'] = indneutralize(data['adv20'],data['industry'])

    # 7. 计算 ts_corr(indneutralize(vwap, IndClass.sector), indneutralize(adv20, IndClass.subindustry), 6.02936)
    data_ts_corr_vwap_adv20 = ts_corr(data['indneutralize_vwap_sector'],data['indneutralize_adv20_subindustry'],6.02936)

    # 8. 计算 rank(ts_corr(indneutralize(vwap, IndClass.sector), indneutralize(adv20, IndClass.subindustry), 6.02936))
    data_rank_ts_corr_vwap_adv20 = rank(data_ts_corr_vwap_adv20)

    # 9. 计算 rank(high - ts_min(high, 2.14593)) * rank(ts_corr(indneutralize(vwap, IndClass.sector), indneutralize(adv20, IndClass.subindustry), 6.02936))
    data_multiply_rank = multiply(data_rank_high_subtract_ts_min, data_rank_ts_corr_vwap_adv20)

    # 10. 计算 (rank(high - ts_min(high, 2.14593)) * rank(ts_corr(indneutralize(vwap, IndClass.sector), indneutralize(adv20, IndClass.subindustry), 6.02936))) * -1
    factor = multiply(data_multiply_rank, -1)

    # 删除中间变量
    del data['indneutralize_vwap_sector']
    del data['adv20']
    del data['indneutralize_adv20_subindustry']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()