import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, adv

def factor_0074(data, **kwargs):
    """
    数学表达式: (rank(ts_corr(vwap, volume, 4.24304)) < rank(ts_corr(rank(low), rank(adv50), 12.4413))) 
    中文描述: 这个因子比较了两个相关性指标的相对排序。首先，计算过去4.24304天成交额加权平均价(vwap)与成交量的相关性，然后对所有股票在当前交易日的结果进行排序。其次，计算过去12.4413天最低价的排名与过去50天平均成交额(adv50)的排名的相关性，同样对所有股票在当前交易日的结果进行排序。最后，比较这两个排序结果，如果第一个相关性排序小于第二个相关性排序，则该因子取值为真，否则为假。这个因子可能捕捉了量价关系和价格与成交额之间的关系，数值越小，说明量价关系越弱，价格与成交额关系越强。
    应用场景：
    1. 识别量价背离的股票，用于短线反转策略。
    2. 结合其他基本面因子，筛选出基本面良好且量价关系异常的股票，用于价值投资。
    3. 用于构建量化选股模型，作为多因子模型中的一个因子，与其他因子结合使用，提高选股效果。
    """
    # 1. 计算 ts_corr(vwap, volume, 4.24304)
    data_ts_corr_vwap_volume = ts_corr(data['vwap'], data['vol'], 4.24304)
    # 2. 计算 rank(ts_corr(vwap, volume, 4.24304))
    data_rank_ts_corr_vwap_volume = rank(data_ts_corr_vwap_volume, 2)
    # 3. 计算 rank(low)
    data_rank_low = rank(data['low'], 2)
    # 4. 计算 adv50
    data['adv50'] = adv(data['vol'],50)
    # 5. 计算 rank(adv50)
    data_rank_adv50 = rank(data['adv50'], 2)
    # 6. 计算 ts_corr(rank(low), rank(adv50), 12.4413)
    data_ts_corr_rank_low_rank_adv50 = ts_corr(data_rank_low, data_rank_adv50, 12.4413)
    # 7. 计算 rank(ts_corr(rank(low), rank(adv50), 12.4413))
    data_rank_ts_corr_rank_low_rank_adv50 = rank(data_ts_corr_rank_low_rank_adv50, 2)
    # 8. 计算 (rank(ts_corr(vwap, volume, 4.24304)) < rank(ts_corr(rank(low), rank(adv50), 12.4413)))
    factor = data_rank_ts_corr_vwap_volume < data_rank_ts_corr_rank_low_rank_adv50

    # 删除中间变量
    del data['adv50']
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()