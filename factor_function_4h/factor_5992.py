import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract
from operators import rank
from operators import ts_decay_exp_window
from operators import multiply
from operators import ts_max_diff
from operators import ts_min_diff

import pandas as pd

def factor_5992(data, **kwargs):
    """
    因子名称: VolWeightedPriceExtremesDecayRankDiff_30964
    数学表达式: subtract(rank(ts_decay_exp_window(multiply(ts_max_diff(close, 10), vol), factor=0.8)), rank(ts_decay_exp_window(multiply(ts_min_diff(open, 10), vol), factor=0.8)))
    中文描述: 该因子旨在捕捉经过成交量加权和指数衰减加权处理后的收盘价最大差异和开盘价最小差异的排名差异。它首先计算过去10天收盘价与过去10天最大收盘价的差值，并将其与当天的成交量相乘。接着，计算过去10天开盘价与过去10天最小开盘价的差值，并将其与当天的成交量相乘。然后，对这两组经过成交量加权处理后的差异应用衰减因子为0.8的指数加权平均。最后，计算这两组经过衰减加权处理后的差异的排名差。这个因子结合了价格极值变化、成交量信息、指数衰减加权和排名信息，旨在更平滑地反映近期价格极值差异的相对强弱，并将其转化为可比较的排名。相较于原始因子，创新点在于引入了成交量加权，使得因子更能反映市场活跃度对价格差异的影响，同时调整了时间窗口和衰减因子，并保留了指数衰减加权、排名和差值的逻辑，以期提升因子的预测能力和稳定性。
    因子应用场景：
    1. 市场活跃度分析：通过成交量加权，该因子能更好地反映市场活跃度对价格差异的影响。
    2. 价格极值变化分析：结合价格极值变化、成交量信息、指数衰减加权和排名信息，旨在更平滑地反映近期价格极值差异的相对强弱，并将其转化为可比较的排名。
    """
    # 1. 计算 ts_max_diff(close, 10)
    data_ts_max_diff_close = ts_max_diff(data['close'], d=10)
    # 2. 计算 multiply(ts_max_diff(close, 10), vol)
    data_multiply_max = multiply(data_ts_max_diff_close, data['vol'])
    # 3. 计算 ts_decay_exp_window(multiply(ts_max_diff(close, 10), vol), factor=0.8)
    data_ts_decay_exp_window_max = ts_decay_exp_window(data_multiply_max, factor=0.8)
    # 4. 计算 rank(ts_decay_exp_window(multiply(ts_max_diff(close, 10), vol), factor=0.8))
    data_rank_max = rank(data_ts_decay_exp_window_max)
    # 5. 计算 ts_min_diff(open, 10)
    data_ts_min_diff_open = ts_min_diff(data['open'], d=10)
    # 6. 计算 multiply(ts_min_diff(open, 10), vol)
    data_multiply_min = multiply(data_ts_min_diff_open, data['vol'])
    # 7. 计算 ts_decay_exp_window(multiply(ts_min_diff(open, 10), vol), factor=0.8)
    data_ts_decay_exp_window_min = ts_decay_exp_window(data_multiply_min, factor=0.8)
    # 8. 计算 rank(ts_decay_exp_window(multiply(ts_min_diff(open, 10), vol), factor=0.8))
    data_rank_min = rank(data_ts_decay_exp_window_min)
    # 9. 计算 subtract(rank(ts_decay_exp_window(multiply(ts_max_diff(close, 10), vol), factor=0.8)), rank(ts_decay_exp_window(multiply(ts_min_diff(open, 10), vol), factor=0.8)))
    factor = subtract(data_rank_max, data_rank_min)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()