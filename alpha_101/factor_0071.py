import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_decay_linear, ts_rank, adv, add, divide

def factor_0071(data, **kwargs):
    """
    数学表达式: (rank(ts_decay_linear(ts_corr(((high + low) / 2), adv40, 8.93345), 10.1519)) / rank(ts_decay_linear(ts_corr(ts_rank(vwap, 3.72469), ts_rank(volume, 18.5188), 6.86671), 2.95011))) 
    中文描述: 该因子计算股票池中股票排序后的值，分子是过去10.1519天，每天的（过去8.93345天中每天的(最高价+最低价)/2与过去40天平均成交额的相关系数）的线性衰减值，再进行排序。分母是过去2.95011天，每天的（过去6.86671天中每天的(过去3.72469天成交额排名与过去18.5188天成交量的排名的相关系数)）的线性衰减值，再进行排序。该因子试图捕捉价格与成交额的联动关系，并结合成交量排名与成交额排名的相关性，通过线性衰减强调近期数据的影响，最后通过排序进行标准化。
    应用场景：
    1. 短期反转策略：寻找分子排名较高，分母排名较低的股票，可能代表短期内价格与成交额的正相关性较高，但成交量排名与成交额排名的相关性较低，预示着超买或超卖，可能出现反转。
    2. 趋势跟踪策略：寻找分子和分母排名都较高的股票，可能代表价格与成交额的联动性以及成交量排名与成交额排名的相关性都较强，是趋势强劲的信号。
    3. 量价异常检测：将该因子作为异常检测的指标，观察因子值大幅偏离历史均值的股票，可能存在市场关注度或资金流向的异常变化。
    """
    # 分子计算
    # (high + low) / 2
    high_plus_low = add(data['high'], data['low'])
    hl_half = divide(high_plus_low, 2)
    # adv40
    adv40 = adv(data['amount'], d = 40)
    # ts_corr(((high + low) / 2), adv40, 8.93345)
    corr_hl_adv = ts_corr(hl_half, adv40, d = 8.93345)
    # ts_decay_linear(ts_corr(((high + low) / 2), adv40, 8.93345), 10.1519)
    decay_corr_hl_adv = ts_decay_linear(corr_hl_adv, d = 10.1519)
    # rank(ts_decay_linear(ts_corr(((high + low) / 2), adv40, 8.93345), 10.1519))
    numerator = rank(decay_corr_hl_adv, rate = 2)
    
    # 分母计算
    # ts_rank(vwap, 3.72469)
    rank_vwap = ts_rank(data['vwap'], d = 3.72469)
    # ts_rank(volume, 18.5188)
    rank_volume = ts_rank(data['vol'], d = 18.5188)
    # ts_corr(ts_rank(vwap, 3.72469), ts_rank(volume, 18.5188), 6.86671)
    corr_rank_vwap_volume = ts_corr(rank_vwap, rank_volume, d = 6.86671)
    # ts_decay_linear(ts_corr(ts_rank(vwap, 3.72469), ts_rank(volume, 18.5188), 6.86671), 2.95011)
    decay_corr_rank_vwap_volume = ts_decay_linear(corr_rank_vwap_volume, d = 2.95011)
    # rank(ts_decay_linear(ts_corr(ts_rank(vwap, 3.72469), ts_rank(volume, 18.5188), 6.86671), 2.95011))
    denominator = rank(decay_corr_rank_vwap_volume, rate = 2)
    
    # 计算因子
    factor = divide(numerator, denominator)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()