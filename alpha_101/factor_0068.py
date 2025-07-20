import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_delta, ts_max, indneutralize, multiply, subtract, adv

def factor_0068(data, **kwargs):
    """
    数学表达式: ((rank(ts_max(ts_delta(indneutralize(vwap, IndClass.industry), 2.72412), 4.79344))^ts_rank(ts_corr(((close * 0.490655) + (vwap * (1 - 0.490655))), adv20, 4.92416), 9.0615)) * -1)
    中文描述: 1. 详细描述：首先，对成交量加权平均价（vwap）进行行业中性化处理，然后计算过去2.72天的差分，再取过去4.79天的最大值，并计算其排序百分比。同时，计算收盘价乘以0.49加上成交量加权平均价乘以0.51的加权平均值，计算该值与过去20天平均成交额在过去4.92天内的相关系数，并计算过去9.06天的排名。最后，将前者的排名百分比与后者的排名相乘，取负数作为最终因子值。这个因子试图寻找短期内价格变化剧烈且行业调整后的股票，并结合量价关系的变化趋势。 2. 因子应用场景：1. 动量反转策略：该因子可以识别短期内超买的股票，预期未来价格下跌。2. 量价共振策略：该因子结合了价格变化和量价关系，可以用于捕捉量价背离或共振的股票，辅助判断趋势。3. 选股策略：将该因子与其他基本面或技术面因子结合，构建多因子选股模型，提高选股效果。
    """
    # 1. indneutralize(vwap, IndClass.industry)
    data_indneutralize = indneutralize(data['vwap'], data['industry'])
    # 2. ts_delta(indneutralize(vwap, IndClass.industry), 2.72412)
    data_ts_delta = ts_delta(data_indneutralize, 2.72412)
    # 3. ts_max(ts_delta(indneutralize(vwap, IndClass.industry), 2.72412), 4.79344)
    data_ts_max = ts_max(data_ts_delta, 4.79344)
    # 4. rank(ts_max(ts_delta(indneutralize(vwap, IndClass.industry), 2.72412), 4.79344))
    data_rank = rank(data_ts_max, 2)
    # 5. (close * 0.490655)
    data_close_weighted = multiply(data['close'], 0.490655)
    # 6. (vwap * (1 - 0.490655))
    data_vwap_weighted = multiply(data['vwap'], (1 - 0.490655))
    # 7. ((close * 0.490655) + (vwap * (1 - 0.490655)))
    data_sum = data_close_weighted + data_vwap_weighted
    # 8. adv20
    data['adv20'] = adv(data['vol'],20)
    # 9. ts_corr(((close * 0.490655) + (vwap * (1 - 0.490655))), adv20, 4.92416)
    data_ts_corr = ts_corr(data_sum, data['adv20'], 4.92416)
    # 10. ts_rank(ts_corr(((close * 0.490655) + (vwap * (1 - 0.490655))), adv20, 4.92416), 9.0615)
    data_ts_rank = rank(data_ts_corr, 2)
    # 11. (rank(ts_max(ts_delta(indneutralize(vwap, IndClass.industry), 2.72412), 4.79344))^ts_rank(ts_corr(((close * 0.490655) + (vwap * (1 - 0.490655))), adv20, 4.92416), 9.0615))
    data_multiply = multiply(data_rank, data_ts_rank)
    # 12. ((rank(ts_max(ts_delta(indneutralize(vwap, IndClass.industry), 2.72412), 4.79344))^ts_rank(ts_corr(((close * 0.490655) + (vwap * (1 - 0.490655))), adv20, 4.92416), 9.0615)) * -1)
    factor = multiply(data_multiply, -1)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    del data['adv20']
    return data.sort_index()