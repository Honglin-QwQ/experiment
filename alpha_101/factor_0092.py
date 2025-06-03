import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_decay_linear, ts_corr, rank, ts_delta, multiply, subtract, adv,indneutralize

def factor_0092(data, **kwargs):
    """
    数学表达式: (ts_rank(ts_decay_linear(ts_corr(indneutralize(vwap, IndClass.industry), adv81, 17.4193), 19.848), 7.54455) / rank(ts_decay_linear(ts_delta(((close * 0.524434) + (vwap * (1 - 0.524434))), 2.77377), 16.2664))) 
    中文描述: 描述：该因子首先计算过去17.4193天行业中性化的成交量加权平均价(vwap)与81日平均成交额(adv81)的相关性，然后对该相关性进行19.848天的线性衰减，并计算过去7.54455天衰减相关性的排名。同时，计算收盘价乘以0.524434加上成交量加权平均价乘以(1-0.524434)的加权平均价，对该加权平均价进行2.77377天的差分，再进行16.2664天的线性衰减，并计算其排名。最后，将衰减相关性的排名除以衰减加权平均价差分的排名。该因子试图捕捉成交量、价格和行业之间的复杂关系，通过时间衰减和排名来平滑数据，可能反映了市场对特定行业或股票的关注度变化。
    应用场景：
    1. 可以作为量化选股的因子，用于筛选出具有特定市场关注度模式的股票。
    2. 可以用于构建配对交易策略，寻找相关性变化异常的股票对。
    3. 可以用于风险管理，监控市场情绪和行业轮动。
    """
    # 计算 adv81
    adv81 = adv(data['vol'],81)
    # 1. 计算 indneutralize(vwap, IndClass.industry)
    industry_neutral_vwap = indneutralize(data['vwap'],data['industry'])
    # 2. 计算 ts_corr(indneutralize(vwap, IndClass.industry), adv81, 17.4193)
    corr_data = ts_corr(industry_neutral_vwap, adv81, 17.4193)
    # 3. 计算 ts_decay_linear(ts_corr(indneutralize(vwap, IndClass.industry), adv81, 17.4193), 19.848)
    decay_linear_corr = ts_decay_linear(corr_data, 19.848)
    # 4. 计算 ts_rank(ts_decay_linear(ts_corr(indneutralize(vwap, IndClass.industry), adv81, 17.4193), 19.848), 7.54455)
    numerator = ts_rank(decay_linear_corr, 7.54455)
    
    # 5. 计算 (close * 0.524434)
    close_weighted = multiply(data['close'], 0.524434)
    # 6. 计算 (vwap * (1 - 0.524434))
    vwap_weighted = multiply(data['vwap'], (1 - 0.524434))
    # 7. 计算 ((close * 0.524434) + (vwap * (1 - 0.524434)))
    weighted_avg = close_weighted + vwap_weighted
    # 8. 计算 ts_delta(((close * 0.524434) + (vwap * (1 - 0.524434))), 2.77377)
    delta_weighted_avg = ts_delta(weighted_avg, 2.77377)
    # 9. 计算 ts_decay_linear(ts_delta(((close * 0.524434) + (vwap * (1 - 0.524434))), 2.77377), 16.2664)
    decay_linear_delta = ts_decay_linear(delta_weighted_avg, 16.2664)
    # 10. 计算 rank(ts_decay_linear(ts_delta(((close * 0.524434) + (vwap * (1 - 0.524434))), 2.77377), 16.2664))
    denominator = rank(decay_linear_delta, 2)
    
    # 11. 计算 (ts_rank(ts_decay_linear(ts_corr(indneutralize(vwap, IndClass.industry), adv81, 17.4193), 19.848), 7.54455) / rank(ts_decay_linear(ts_delta(((close * 0.524434) + (vwap * (1 - 0.524434))), 2.77377), 16.2664)))
    factor = numerator / denominator
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()