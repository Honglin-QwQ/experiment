import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, ts_corr, ts_min_max_diff, ts_delta

def factor_5771(data, **kwargs):
    """
    因子名称: TS_Decay_MinMax_Diff_Corr_40883
    数学表达式: ts_decay_exp_window(ts_corr(low, vol, 10), 5, 0.7) - ts_min_max_diff(ts_delta(close, 3), 7, 0.3)
    中文描述: 该因子结合了时间序列指数衰减、相关性、最小值最大值差异和时间序列差分。首先，计算过去10天最低价(low)与成交量(vol)的相关性，并对该相关性序列应用5天窗口、衰减因子为0.7的指数衰减加权平均。这部分捕捉了近期价量关系的衰减趋势。然后，计算过去3天收盘价(close)的差值，并对该差值序列应用7天窗口、比例因子为0.3的最小值最大值差异运算。这部分衡量了短期价格变化的极值波动。最终因子值是这两部分的差值。这个因子旨在捕捉衰减的价量关系趋势与短期价格极值波动的相对强度，可能用于识别市场情绪的微妙变化或潜在的转折点。创新点在于结合了衰减相关性与极值差异，形成一个多维度的市场动态衡量指标，并利用了指数衰减和最小值最大值差异这两个在参考因子中未直接出现的运算符。
    因子应用场景：
    1. 市场情绪识别：捕捉衰减的价量关系趋势与短期价格极值波动的相对强度，可能用于识别市场情绪的微妙变化。
    2. 转折点预测：该因子可能有助于识别潜在的市场转折点。
    """
    # 1. 计算 ts_corr(low, vol, 10)
    data_ts_corr = ts_corr(data['low'], data['vol'], 10)
    # 2. 计算 ts_decay_exp_window(ts_corr(low, vol, 10), 5, 0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_corr, 5, 0.7)
    # 3. 计算 ts_delta(close, 3)
    data_ts_delta = ts_delta(data['close'], 3)
    # 4. 计算 ts_min_max_diff(ts_delta(close, 3), 7, 0.3)
    data_ts_min_max_diff = ts_min_max_diff(data_ts_delta, 7, 0.3)
    # 5. 计算 ts_decay_exp_window(ts_corr(low, vol, 10), 5, 0.7) - ts_min_max_diff(ts_delta(close, 3), 7, 0.3)
    factor = data_ts_decay_exp_window - data_ts_min_max_diff

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()