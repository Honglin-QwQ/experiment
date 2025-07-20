import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_decay_linear, ts_corr, multiply, subtract, indneutralize

def factor_0058(data, **kwargs):
    """
    数学表达式: (-1 * ts_rank(ts_decay_linear(ts_corr(indneutralize(((vwap * 0.728317) + (vwap * (1 - 0.728317))), IndClass.industry), volume, 4.25197), 16.2289), 8.19648))
    中文描述: 首先计算成交量加权平均价（VWAP），然后将其乘以0.728317，再加上VWAP乘以(1-0.728317)的结果，本质上是对VWAP进行加权平均；接着对结果进行行业中性化处理，消除行业的影响；然后计算行业中性化后的VWAP与成交量在过去4.25197天的相关性；对相关性进行16.2289天的线性衰减加权；计算衰减加权后的相关性在过去8.19648天的排名；最后取排名的负值。这个因子可能捕捉了行业中性化后的价格与成交量相关性的变化趋势，并通过排名和取负，使得排名靠前的股票具有更高的因子值，可以用于量化选股，例如，选择因子值高的股票构建多头组合，做多因子值上升最快的股票，或者用于风险管理，规避因子值持续下降的股票。
    因子应用场景：
    1. 行业中性化后的价格与成交量相关性的变化趋势分析。
    2. 量化选股：选择因子值高的股票构建多头组合。
    3. 风险管理：规避因子值持续下降的股票。
    """
    # 1. 计算 (vwap * 0.728317)
    vwap_0728317 = multiply(data['vwap'], 0.728317)
    # 2. 计算 (1 - 0.728317)
    one_minus_0728317 = 1 - 0.728317
    # 3. 计算 (vwap * (1 - 0.728317))
    vwap_one_minus_0728317 = multiply(data['vwap'], one_minus_0728317)
    # 4. 计算 ((vwap * 0.728317) + (vwap * (1 - 0.728317)))
    vwap_weighted_avg = multiply(vwap_0728317,vwap_one_minus_0728317)
    # 5. 计算 indneutralize(((vwap * 0.728317) + (vwap * (1 - 0.728317))), IndClass.industry)
    ind_neutralized_vwap = indneutralize(vwap_weighted_avg, data['industry'])
    # 6. 计算 ts_corr(indneutralize(((vwap * 0.728317) + (vwap * (1 - 0.728317))), IndClass.industry), volume, 4.25197)
    ts_corr_ind_neutralized_vwap_volume = ts_corr(ind_neutralized_vwap, data['vol'], 4.25197)
    # 7. 计算 ts_decay_linear(ts_corr(indneutralize(((vwap * 0.728317) + (vwap * (1 - 0.728317))), IndClass.industry), volume, 4.25197), 16.2289)
    ts_decay_linear_corr = ts_decay_linear(ts_corr_ind_neutralized_vwap_volume, 16.2289)
    # 8. 计算 ts_rank(ts_decay_linear(ts_corr(indneutralize(((vwap * 0.728317) + (vwap * (1 - 0.728317))), IndClass.industry), volume, 4.25197), 16.2289), 8.19648)
    ts_rank_decay_linear_corr = ts_rank(ts_decay_linear_corr, 8.19648)
    # 9. 计算 -1 * ts_rank(ts_decay_linear(ts_corr(indneutralize(((vwap * 0.728317) + (vwap * (1 - 0.728317))), IndClass.industry), volume, 4.25197), 16.2289), 8.19648)
    factor = -1 * ts_rank_decay_linear_corr

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()