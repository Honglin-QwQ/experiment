import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log_diff, ts_decay_exp_window, divide
import pandas as pd
import numpy as np

def factor_5717(data, **kwargs):
    """
    数学表达式: divide(log_diff(high), ts_decay_exp_window(vol, d=10, factor=0.6))
    中文描述: 该因子结合了最高价的对数差分和成交量的指数衰减加权平均，旨在捕捉价格动量与近期成交量加权平均的比例关系。首先计算当前最高价的对数差分，反映了最高价的相对变化率。然后计算过去10天成交量的指数衰减加权平均，给予近期成交量更高的权重。最后，将对数差分除以该加权平均成交量。这个因子创新性地将价格变化率与近期加权的成交量相结合，可能用于识别在近期成交活跃度背景下的价格动量强度。如果比例较高，可能表示当前最高价的相对变化较大，且发生在近期成交量加权平均较低的位置，这可能暗示着价格在相对缺乏成交支持的情况下出现较强的动量。反之，如果比例较低，可能表示当前最高价的相对变化较小，或者发生在近期成交量加权平均较高的位置，可能暗示着价格在成交活跃的情况下动量较弱或处于盘整。该因子适用于捕捉短期内价格动量与近期成交量模式的相互作用。
    因子应用场景：
    1. 动量识别：用于识别价格动量与成交量之间的关系，辅助判断趋势的可靠性。
    2. 成交量验证：通过成交量的加权平均，验证价格变动的成交量支持，判断趋势的可持续性。
    """
    # 1. 计算 log_diff(high)
    data_log_diff_high = log_diff(data['high'])
    # 2. 计算 ts_decay_exp_window(vol, d=10, factor=0.6)
    data_ts_decay_exp_window = ts_decay_exp_window(data['vol'], d=10, factor=0.6)
    # 3. 计算 divide(log_diff(high), ts_decay_exp_window(vol, d=10, factor=0.6))
    factor = divide(data_log_diff_high, data_ts_decay_exp_window)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()