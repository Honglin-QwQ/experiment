import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, ts_corr, ts_delta, adv, multiply

import pandas as pd

def factor_6104(data, **kwargs):
    """
    因子名称: VolPriceCorrelationDecay_27362
    数学表达式: ts_decay_exp_window(ts_corr(vol, close, 10), 20, factor = 0.7) * ts_delta(adv(close, 50), 100)
    中文描述: 该因子结合了短期成交量与收盘价的相关性，并通过指数衰减加权平均来平滑，然后乘以长期平均收盘价的变动。具体而言，首先计算过去10天成交量与收盘价的相关性，然后对这个相关性序列进行20天的指数衰减加权平均，衰减因子为0.7。最后，将这个衰减相关性与过去100天平均收盘价的100天变化量相乘。这个因子试图捕捉短期价量关系的动量，并结合长期价格趋势的变动，以识别潜在的交易机会。指数衰减加权平均的使用使得近期价量相关性对因子值的影响更大，而长期平均收盘价的变动则提供了宏观的市场背景信息。这是一种创新的结合短期动量和长期趋势的方法。
    因子应用场景：
    1. 短期价量关系：捕捉短期成交量与收盘价的相关性，识别潜在的交易机会。
    2. 长期价格趋势：结合长期平均收盘价的变动，提供宏观的市场背景信息。
    """
    # 1. 计算 ts_corr(vol, close, 10)
    data_ts_corr = ts_corr(data['vol'], data['close'], d = 10)
    # 2. 计算 ts_decay_exp_window(ts_corr(vol, close, 10), 20, factor = 0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_corr, d = 20, factor = 0.7)
    # 3. 计算 adv(close, 50)
    data_adv = adv(data['close'], d = 50)
    # 4. 计算 ts_delta(adv(close, 50), 100)
    data_ts_delta = ts_delta(data_adv, d = 100)
    # 5. 计算 ts_decay_exp_window(ts_corr(vol, close, 10), 20, factor = 0.7) * ts_delta(adv(close, 50), 100)
    factor = multiply(data_ts_decay_exp_window, data_ts_delta)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()