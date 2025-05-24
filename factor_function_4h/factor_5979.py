import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_min, ts_std_dev, subtract, scale
import pandas as pd

def factor_5979(data, **kwargs):
    """
    因子名称: ts_min_std_diff_scaled_73020
    数学表达式: scale(subtract(ts_min(open, 54), ts_std_dev(open, 120)))
    中文描述: 该因子结合了过去54天开盘价的最小值和过去120天开盘价的标准差。通过计算这两者的差值，并进行横截面缩放，该因子旨在衡量当前市场情绪（通过开盘价最小值反映的潜在底部）与长期价格波动性之间的相对关系。负值可能表示开盘价接近长期低点，且波动性相对较高，可能预示着潜在的反转机会；正值则可能表示开盘价远离长期低点，且波动性较低，可能预示着趋势的持续。创新点在于将短期极值与长期波动性相结合，并通过缩放操作增强因子的可比性。
    因子应用场景：
    1. 反转识别：寻找负值较大的股票，可能预示着超卖反转机会。
    2. 趋势确认：寻找正值较小的股票，可能预示着趋势持续。
    """
    # 1. 计算 ts_min(open, 54)
    data_ts_min_open = ts_min(data['open'], 54)
    # 2. 计算 ts_std_dev(open, 120)
    data_ts_std_dev_open = ts_std_dev(data['open'], 120)
    # 3. 计算 subtract(ts_min(open, 54), ts_std_dev(open, 120))
    data_subtract = subtract(data_ts_min_open, data_ts_std_dev_open)
    # 4. 计算 scale(subtract(ts_min(open, 54), ts_std_dev(open, 120)))
    factor = scale(data_subtract)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()