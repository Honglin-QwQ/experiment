import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, ts_std_dev, jump_decay, ts_delta, multiply

import pandas as pd
import numpy as np

def factor_5991(data, **kwargs):
    """
    数学表达式: ts_decay_exp_window(ts_std_dev(returns, 7), 4, factor = 0.8) * jump_decay(ts_delta(close, 3), d = 5, sensitivity = 0.6, force = 0.2)
    中文描述: 该因子结合了短期收益率波动率的指数衰减和近期价格跳跃的衰减贡献。首先，计算过去7天的日收益率标准差，并应用4天窗口的指数衰减加权平均，赋予近期波动率更高权重。然后，计算过去3天收盘价的变化，并应用jump_decay操作符，平滑价格跳跃并计算其衰减贡献。最后，将衰减后的波动率与衰减后的价格跳跃贡献相乘。

    创新点：
    1. 结合了短期波动率的衰减和价格跳跃的衰减贡献，试图捕捉在波动率和价格变动同时发生时的市场动态。
    2. 使用jump_decay操作符处理价格变化，相比简单的差值更能识别和量化价格的非连续性变动及其影响。
    3. 参数设置（如窗口大小、衰减因子、jump_decay参数）经过调整，以期更好地捕捉短期市场特征。

    应用场景：可能适用于识别在市场波动和价格出现显著跳跃后，潜在的趋势延续或反转机会。
    """
    # 1. 计算 ts_std_dev(returns, 7)
    data_ts_std_dev = ts_std_dev(data['returns'], d = 7)
    # 2. 计算 ts_decay_exp_window(ts_std_dev(returns, 7), 4, factor = 0.8)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_std_dev, d = 4, factor = 0.8)
    # 3. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], d = 3)
    # 4. 计算 jump_decay(ts_delta(close, 3), d = 5, sensitivity = 0.6, force = 0.2)
    data_jump_decay = jump_decay(data_ts_delta_close, d = 5, sensitivity = 0.6, force = 0.2)
    # 5. 计算 ts_decay_exp_window(ts_std_dev(returns, 7), 4, factor = 0.8) * jump_decay(ts_delta(close, 3), d = 5, sensitivity = 0.6, force = 0.2)
    factor = multiply(data_ts_decay_exp_window, data_jump_decay)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()