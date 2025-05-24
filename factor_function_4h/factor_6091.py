import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_decay_exp_window, add

def factor_6091(data, **kwargs):
    """
    数学表达式: ts_decay_exp_window(ts_corr(vol, tbase, 10), 5, factor = 0.7) + ts_decay_exp_window(ts_corr(vol, tquote, 10), 5, factor = 0.7)
    中文描述: 该因子旨在捕捉成交量(vol)与主动买入基础币种数量(tbase)以及成交量(vol)与主动买入计价币种数量(tquote)之间在过去10天内的相关性，并通过过去5天的指数衰减加权平均来突出近期相关性的影响。相较于原始的三重相关性，我们将其分解为两个双变量相关性，并使用指数衰减代替线性衰减，以更灵活地反映市场信息衰减规律。这种分解和指数衰减的应用，旨在更精细地捕捉成交量与主动买卖行为之间的动态关系，识别潜在的短期交易机会。因子值高可能表明近期成交量与主动买卖行为呈现较强的正相关，预示着潜在的上涨动能；反之，低值可能暗示负相关或相关性减弱，可能预示下跌或盘整。
    因子应用场景：
    1. 趋势识别：该因子可以帮助识别成交量与主动买卖行为之间是否存在趋势，以及趋势的强度。
    2. 短期交易机会：通过捕捉成交量与主动买卖行为之间的动态关系，可以辅助识别潜在的短期交易机会。
    """
    # 1. 计算 ts_corr(vol, tbase, 10)
    data_ts_corr_vol_tbase = ts_corr(data['vol'], data['tbase'], d = 10)
    # 2. 计算 ts_decay_exp_window(ts_corr(vol, tbase, 10), 5, factor = 0.7)
    data_ts_decay_exp_window_vol_tbase = ts_decay_exp_window(data_ts_corr_vol_tbase, d = 5, factor = 0.7)
    # 3. 计算 ts_corr(vol, tquote, 10)
    data_ts_corr_vol_tquote = ts_corr(data['vol'], data['tquote'], d = 10)
    # 4. 计算 ts_decay_exp_window(ts_corr(vol, tquote, 10), 5, factor = 0.7)
    data_ts_decay_exp_window_vol_tquote = ts_decay_exp_window(data_ts_corr_vol_tquote, d = 5, factor = 0.7)
    # 5. 计算 ts_decay_exp_window(ts_corr(vol, tbase, 10), 5, factor = 0.7) + ts_decay_exp_window(ts_corr(vol, tquote, 10), 5, factor = 0.7)
    factor = add(data_ts_decay_exp_window_vol_tbase, data_ts_decay_exp_window_vol_tquote)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()