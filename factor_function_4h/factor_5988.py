import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract, rank, ts_decay_exp_window, ts_max_diff, ts_min_diff
import pandas as pd

def factor_5988(data, **kwargs):
    """
    因子名称: RankedPriceExtremesDecayDiff_22677
    数学表达式: subtract(rank(ts_decay_exp_window(ts_max_diff(close, 15), factor=0.7)), rank(ts_decay_exp_window(ts_min_diff(open, 15), factor=0.7)))
    中文描述: 该因子旨在捕捉经过指数衰减加权处理后的收盘价最大差异和开盘价最小差异的排名差异。它首先计算过去15天收盘价与过去15天最大收盘价的差值，并应用衰减因子为0.7的指数加权平均。接着，计算过去15天开盘价与过去15天最小开盘价的差值，同样应用衰减因子为0.7的指数加权平均。最后，计算这两组经过衰减加权处理后的差异的排名差。这个因子结合了价格极值变化、指数衰减加权和排名信息，旨在更平滑地反映近期价格极值差异的相对强弱，并将其转化为可比较的排名。相较于原始因子，创新点在于引入了ts_decay_exp_window操作符，对价格差异进行了指数衰减加权处理，使得因子更侧重于近期的数据，同时调整了时间窗口，并保留了排名和差值的逻辑，以期提升因子的预测能力和稳定性。
    因子应用场景：
    1. 趋势反转识别：当因子值发生显著变化时，可能预示着市场趋势的反转。
    2. 波动率预测：该因子可以作为衡量市场波动率的指标之一，因子值越高，可能表示市场波动性越大。
    """
    # 1. 计算 ts_max_diff(close, 15)
    data_ts_max_diff_close = ts_max_diff(data['close'], 15)
    # 2. 计算 ts_decay_exp_window(ts_max_diff(close, 15), factor=0.7)
    data_ts_decay_exp_window_max = ts_decay_exp_window(data_ts_max_diff_close, factor=0.7)
    # 3. 计算 rank(ts_decay_exp_window(ts_max_diff(close, 15), factor=0.7))
    rank_max = rank(data_ts_decay_exp_window_max, rate = 2)
    # 4. 计算 ts_min_diff(open, 15)
    data_ts_min_diff_open = ts_min_diff(data['open'], 15)
    # 5. 计算 ts_decay_exp_window(ts_min_diff(open, 15), factor=0.7)
    data_ts_decay_exp_window_min = ts_decay_exp_window(data_ts_min_diff_open, factor=0.7)
    # 6. 计算 rank(ts_decay_exp_window(ts_min_diff(open, 15), factor=0.7))
    rank_min = rank(data_ts_decay_exp_window_min, rate = 2)
    # 7. 计算 subtract(rank(ts_decay_exp_window(ts_max_diff(close, 15), factor=0.7)), rank(ts_decay_exp_window(ts_min_diff(open, 15), factor=0.7)))
    factor = subtract(rank_max, rank_min)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()