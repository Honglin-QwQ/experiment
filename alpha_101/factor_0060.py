import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_min, subtract

def factor_0060(data, **kwargs):
    """
    数学表达式: (rank((vwap - ts_min(vwap, 16.1219))) < rank(ts_corr(vwap, adv180, 17.9282))) 
    中文描述: 该因子首先计算过去16.1219个时间单位内每天的成交量加权平均价(vwap)的最小值，然后用当天的vwap减去该最小值，接着计算结果在所有股票中的排序百分比；同时，计算每天的成交量加权平均价(vwap)与过去180天平均成交额(adv180)在过去17.9282个时间单位内的相关系数，并计算相关系数在所有股票中的排序百分比；最后，比较两个排序百分比的大小。该因子试图找出那些近期vwap相对于过去一段时间低点上涨幅度较小，但与成交额的相关性排名较高的股票，可能意味着这些股票的上涨趋势尚未被市场充分认知，存在潜在的投资机会。
    应用场景：
    1. 选股策略：选取因子值较高的股票，构建多头组合，预期这些股票未来会上涨。
    2. 动量策略：结合其他动量因子，筛选出既有一定动量，又未被市场过度追捧的股票。
    3. 风险控制：避免买入因子值过低的股票，这些股票可能已经过度上涨，存在回调风险。
    """
    # 计算过去16.1219个时间单位内每天的成交量加权平均价(vwap)的最小值
    vwap_min = ts_min(data['vwap'], d = 16.1219)
    # 用当天的vwap减去该最小值
    vwap_diff = subtract(data['vwap'], vwap_min)
    # 计算结果在所有股票中的排序百分比
    rank_vwap_diff = rank(vwap_diff)
    # 计算每天的成交量加权平均价(vwap)与过去180天平均成交额(adv180)在过去17.9282个时间单位内的相关系数
    vwap_adv180_corr = ts_corr(data['vwap'], data['amount'], d = 17.9282)
    # 计算相关系数在所有股票中的排序百分比
    rank_vwap_adv180_corr = rank(vwap_adv180_corr)
    # 比较两个排序百分比的大小
    factor = (rank_vwap_diff < rank_vwap_adv180_corr).astype(int)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()