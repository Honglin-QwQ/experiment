import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, rank, ts_corr, ts_decay_linear

def factor_5833(data, **kwargs):
    """
    因子名称: Volatility_Decay_Correlation_Rank_Delta_82105
    数学表达式: ts_delta(rank(ts_corr(ts_decay_linear(vol, 15), ts_decay_linear(close, 15), 30)), 45)
    中文描述: 该因子计算过去30天内，基于15天线性衰减加权的成交量与收盘价之间的相关性。然后对这个相关性值进行横截面排名，最后计算排名在过去45天内的变化量。线性衰减加权突出了近期数据的重要性，成交量与收盘价的相关性可以反映价量关系的强度和方向。对相关性进行排名增强了因子在不同股票间的可比性，而计算排名的时间序列差分则捕捉了这种相对价量关系变化的动量。正值表示近期成交量与收盘价相关性的排名在过去45天内有所上升，可能预示着当前价量关系的持续性或强化。负值则表示下降。相对于参考因子，本因子结合了线性衰减加权、价量相关性和多周期的排名变化，以更精细地捕捉市场动态。同时，避免了历史输出中可能出现的因数值全为零的问题，通过计算相对排名变化，确保因子具有区分度。
    因子应用场景：
    1. 动量捕捉：捕捉成交量与收盘价相关性排名变化的动量。
    2. 趋势识别：识别成交量与收盘价相关性增强或减弱的趋势。
    3. 市场情绪：反映市场对当前价量关系的认可程度。
    """
    # 1. 计算 ts_decay_linear(vol, 15)
    data_ts_decay_linear_vol = ts_decay_linear(data['vol'], 15)
    # 2. 计算 ts_decay_linear(close, 15)
    data_ts_decay_linear_close = ts_decay_linear(data['close'], 15)
    # 3. 计算 ts_corr(ts_decay_linear(vol, 15), ts_decay_linear(close, 15), 30)
    data_ts_corr = ts_corr(data_ts_decay_linear_vol, data_ts_decay_linear_close, 30)
    # 4. 计算 rank(ts_corr(ts_decay_linear(vol, 15), ts_decay_linear(close, 15), 30))
    data_rank = rank(data_ts_corr, 2)
    # 5. 计算 ts_delta(rank(ts_corr(ts_decay_linear(vol, 15), ts_decay_linear(close, 15), 30)), 45)
    factor = ts_delta(data_rank, 45)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()