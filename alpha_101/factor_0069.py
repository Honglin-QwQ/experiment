import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_delta, indneutralize, adv, ts_rank, multiply

def factor_0069(data, **kwargs):
    """
    数学表达式: ((rank(ts_delta(vwap, 1.29456))^ts_rank(ts_corr(indneutralize(close, IndClass.industry), adv50, 17.8256), 17.9171)) * -1) 
    中文描述: 该因子首先计算过去1.29456期成交量加权平均价(vwap)的变化，然后对这个变化值进行排序，得到一个排序百分比。同时，计算行业中性化后的收盘价与过去50日平均成交额在过去17.8256天内的相关性，再对这个相关性进行过去17.9171天的排名。将vwap变化排序的百分比进行相关性排名次方运算，最后取负值。这个因子衡量了价格变化趋势的强度和行业调整后价格与成交额相关性的关系，并取反向。应用场景：1.可以用于识别价格趋势反转的潜在机会，当因子值较高时，可能预示着下跌趋势即将结束。2.可以结合其他因子构建多因子模型，例如与动量因子、价值因子等结合，提高选股效果。3.可以用于高频交易策略，快速捕捉市场短期内的异常波动。
    """
    # 1. 计算 ts_delta(vwap, 1.29456)
    data_ts_delta_vwap = ts_delta(data['vwap'], 1.29456)
    # 2. 计算 rank(ts_delta(vwap, 1.29456))
    data_rank_ts_delta_vwap = rank(data_ts_delta_vwap)
    # 3. 计算 indneutralize(close, IndClass.industry)
    data_indneutralize_close = indneutralize(data['close'], data['industry'])
    # 4. 计算 adv50
    data_adv50 = adv(data['vol'],50)
    # 5. 计算 ts_corr(indneutralize(close, IndClass.industry), adv50, 17.8256)
    data_ts_corr = ts_corr(data_indneutralize_close, data_adv50, 17.8256)
    # 6. 计算 ts_rank(ts_corr(indneutralize(close, IndClass.industry), adv50, 17.8256), 17.9171)
    data_ts_rank = ts_rank(data_ts_corr, 17.9171)
    # 7. 计算 rank(ts_delta(vwap, 1.29456))^ts_rank(ts_corr(indneutralize(close, IndClass.industry), adv50, 17.8256), 17.9171)
    data_signed_power = data_rank_ts_delta_vwap ** data_ts_rank
    # 8. 计算 (rank(ts_delta(vwap, 1.29456))^ts_rank(ts_corr(indneutralize(close, IndClass.industry), adv50, 17.8256), 17.9171)) * -1
    factor = multiply(data_signed_power, -1)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()