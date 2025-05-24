import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5829(data, **kwargs):
    """
    因子名称: VolatilityAdjustedPriceChangeVolumeRatio_42679
    数学表达式: divide(ts_delta(vwap, 3), ts_rank(ts_std_dev(divide(ts_delta(close, 3), close), 25)))
    中文描述: 该因子计算了过去3天成交量加权平均价（vwap）的变动量，并将其除以过去25天内3天收盘价变动率（3天变动量除以收盘价）的时间序列排名。这旨在衡量成交量加权的价格变动相对于其自身波动性排名的强度。因子值越高，表示近期成交量加权的价格变动相对于其历史波动性排名越强。创新点在于结合了成交量加权平均价和价格变动率波动性的时间序列排名作为调整因子，更全面地捕捉了价格和成交量的动态关系，并降低了异常值对波动性衡量带来的影响。这可能用于识别在相对稳定或不稳定价格变动背景下的由成交量驱动的强劲价格趋势。
    因子应用场景：
    1. 识别成交量驱动的强劲价格趋势。
    2. 衡量成交量加权的价格变动相对于其历史波动性排名的强度。
    """
    # 1. 计算 ts_delta(vwap, 3)
    data_ts_delta_vwap = ts_delta(data['vwap'], 3)
    # 2. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], 3)
    # 3. 计算 divide(ts_delta(close, 3), close)
    data_divide_ts_delta_close_close = divide(data_ts_delta_close, data['close'])
    # 4. 计算 ts_std_dev(divide(ts_delta(close, 3), close), 25)
    data_ts_std_dev = ts_std_dev(data_divide_ts_delta_close_close, 25)
    # 5. 计算 ts_rank(ts_std_dev(divide(ts_delta(close, 3), close), 25))
    data_ts_rank = ts_rank(data_ts_std_dev)
    # 6. 计算 divide(ts_delta(vwap, 3), ts_rank(ts_std_dev(divide(ts_delta(close, 3), close), 25)))
    factor = divide(data_ts_delta_vwap, data_ts_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()