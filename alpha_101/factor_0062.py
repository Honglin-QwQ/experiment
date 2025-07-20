import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_decay_linear, ts_delta, ts_corr, ts_sum,indneutralize,adv
import pandas as pd

def factor_0062(data, **kwargs):
    """
    数学表达式: ((rank(ts_decay_linear(ts_delta(indneutralize(close, IndClass.industry), 2.25164), 8.22237)) - rank(ts_decay_linear(ts_corr(((vwap * 0.318108) + (open * (1 - 0.318108))), ts_sum(adv180, 37.2467), 13.557), 12.2883))) * -1)
    中文描述: 首先对股票的收盘价进行行业中性化处理，然后计算处理后收盘价的2.25164日差分，再计算该差分值的8.22237日线性衰减值，并对衰减值进行排序；同时，计算成交量加权平均价和开盘价的加权平均（权重分别为0.318108和1-0.318108），计算该加权平均价与过去37.2467日平均成交额之和在13.557日内的相关系数，再计算相关系数的12.2883日线性衰减值，并对衰减值进行排序；最后，计算前者的排序减去后者的排序的相反数。该因子可能捕捉了行业中性化后的价格变化趋势与成交量和价格相关性的反向关系，可以用于量化选股，例如构建多因子模型，或者用于高频交易中寻找短期套利机会。
    因子应用场景：
    1. 行业中性化价格趋势：用于识别在行业调整后，价格变化趋势相对较强的股票。
    2. 成交量与价格相关性反转：捕捉成交量变化与价格相关性出现反转的股票，可能预示着趋势的改变。
    """
    # 1. indneutralize(close, IndClass.industry)
    industry_neutralized_close =  indneutralize(data['close'], data['industry'])
    industry_neutralized_close.name = 'industry_neutralized_close'
    data = data.join(industry_neutralized_close)
    # 2. ts_delta(indneutralize(close, IndClass.industry), 2.25164)
    data_ts_delta = ts_delta(data['industry_neutralized_close'], 2.25164)
    # 3. ts_decay_linear(ts_delta(indneutralize(close, IndClass.industry), 2.25164), 8.22237)
    data_ts_decay_linear = ts_decay_linear(data_ts_delta, 8.22237)
    # 4. rank(ts_decay_linear(ts_delta(indneutralize(close, IndClass.industry), 2.25164), 8.22237))
    rank1 = rank(data_ts_decay_linear, 2)

    # 5. (vwap * 0.318108) + (open * (1 - 0.318108))
    weighted_price = (data['vwap'] * 0.318108) + (data['open'] * (1 - 0.318108))
    # 6. adv180
    adv180 = adv(data['vol'],180)
    adv180.name = 'adv180'
    data = data.join(adv180)
    # 7. ts_sum(adv180, 37.2467)
    data_ts_sum = ts_sum(data['adv180'], 37.2467)
    # 8. ts_corr(((vwap * 0.318108) + (open * (1 - 0.318108))), ts_sum(adv180, 37.2467), 13.557)
    data_ts_corr = ts_corr(weighted_price, data_ts_sum, 13.557)
    # 9. ts_decay_linear(ts_corr(((vwap * 0.318108) + (open * (1 - 0.318108))), ts_sum(adv180, 37.2467), 13.557), 12.2883)
    data_ts_decay_linear2 = ts_decay_linear(data_ts_corr, 12.2883)
    # 10. rank(ts_decay_linear(ts_corr(((vwap * 0.318108) + (open * (1 - 0.318108))), ts_sum(adv180, 37.2467), 13.557), 12.2883))
    rank2 = rank(data_ts_decay_linear2, 2)

    # 11. (rank(ts_decay_linear(ts_delta(indneutralize(close, IndClass.industry), 2.25164), 8.22237)) - rank(ts_decay_linear(ts_corr(((vwap * 0.318108) + (open * (1 - 0.318108))), ts_sum(adv180, 37.2467), 13.557), 12.2883))) * -1
    factor = (rank1 - rank2) * -1

    data.drop(columns=['industry_neutralized_close','adv180'], inplace=True)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()