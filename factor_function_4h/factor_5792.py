import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness
from operators import ts_delta
import pandas as pd

def factor_5792(data, **kwargs):
    """
    因子名称: Volatility_Skew_Divergence_60047
    数学表达式: ts_skewness(ts_delta(low, 3), 66) - ts_skewness(ts_delta(high, 3), 66)
    中文描述: 该因子计算了过去66天内，最低价3日差值的偏度与最高价3日差值的偏度之差。它旨在捕捉市场下行波动（由最低价变动衡量）和上行波动（由最高价变动衡量）之间的不对称性。当该因子为正时，表示下行波动比上行波动更偏向于极端负值（即出现更大幅度的下跌），可能预示着市场恐慌或潜在的卖压；当因子为负时，表示上行波动比下行波动更偏向于极端正值（即出现更大幅度的上涨），可能预示着市场乐观或潜在的买盘。这种偏度的差异可以作为判断市场情绪、识别潜在趋势反转或增强现有波动率因子的补充信号。创新点在于同时考虑了最低价和最高价的变动偏度，并计算其差值，以更精细地捕捉市场波动的不对称性。
    因子应用场景：
    1. 市场情绪判断：通过因子值的正负来判断市场情绪，正值可能代表恐慌或卖压，负值可能代表乐观或买盘。
    2. 趋势反转识别：该因子可以作为识别潜在趋势反转的信号。
    3. 波动率因子补充：增强现有波动率因子，提供更精细的市场波动不对称性信息。
    """
    # 1. 计算 ts_delta(low, 3)
    data_ts_delta_low = ts_delta(data['low'], 3)
    # 2. 计算 ts_skewness(ts_delta(low, 3), 66)
    data_ts_skewness_low = ts_skewness(data_ts_delta_low, 66)
    # 3. 计算 ts_delta(high, 3)
    data_ts_delta_high = ts_delta(data['high'], 3)
    # 4. 计算 ts_skewness(ts_delta(high, 3), 66)
    data_ts_skewness_high = ts_skewness(data_ts_delta_high, 66)
    # 5. 计算 ts_skewness(ts_delta(low, 3), 66) - ts_skewness(ts_delta(high, 3), 66)
    factor = data_ts_skewness_low - data_ts_skewness_high

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()