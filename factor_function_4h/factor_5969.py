import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5969(data, **kwargs):
    """
    因子名称: VolScale_HighVolRatio_53076
    数学表达式: divide(ts_scale(adv(vol, 20), 52, constant = -1), ts_percentage(high, 10, percentage = 0.9))
    中文描述: 该因子结合了成交量的标准化和最高价的百分位数。它首先计算过去20天的平均成交量，并在过去52天内进行缩放并偏移-1。然后，计算过去10天内最高价的90%百分位数。最后，将缩放后的平均成交量除以最高价的90%百分位数。这个因子旨在捕捉在相对高成交量时期，价格是否能够维持在较高的水平。如果缩放后的成交量较高（接近1），而最高价的90%百分位数较低，可能表明在成交量放大的情况下，价格未能有效突破高位，可能预示着潜在的卖压或顶部信号。反之，如果缩放后的成交量较低（接近-1），而最高价的90%百分位数较高，可能表明在低成交量时期，价格仍能维持在较高水平，可能预示着潜在的支撑或底部形成。创新点在于将时间序列缩放后的成交量与最高价的百分位数相结合，构建了一个新的比例关系，以更全面地衡量市场情绪和价格动能。
    因子应用场景：
    1. 识别成交量放大但价格未能有效突破高位的股票，可能预示着潜在的卖压或顶部信号。
    2. 识别成交量较低但价格仍能维持在较高水平的股票，可能预示着潜在的支撑或底部形成。
    """
    # 1. 计算 adv(vol, 20)
    data_adv_vol = adv(data['vol'], d = 20)
    # 2. 计算 ts_scale(adv(vol, 20), 52, constant = -1)
    data_ts_scale = ts_scale(data_adv_vol, d = 52, constant = -1)
    # 3. 计算 ts_percentage(high, 10, percentage = 0.9)
    data_ts_percentage = ts_percentage(data['high'], d = 10, percentage = 0.9)
    # 4. 计算 divide(ts_scale(adv(vol, 20), 52, constant = -1), ts_percentage(high, 10, percentage = 0.9))
    factor = divide(data_ts_scale, data_ts_percentage)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()