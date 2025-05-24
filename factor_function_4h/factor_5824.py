import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_std_dev, divide
import pandas as pd

def factor_5824(data, **kwargs):
    """
    因子名称: Volume_Volatility_Skew_Ratio_71570
    数学表达式: divide(ts_skewness(vol, 120), ts_std_dev(vol, 120))
    中文描述: 该因子计算过去120天成交量偏度与成交量标准差的比值。成交量偏度衡量成交量分布的非对称性，标准差衡量成交量的波动性。这个比值可以反映成交量异常波动的方向和强度相对于其整体波动水平。正值表示成交量分布右偏，可能存在异常放量；负值表示左偏，可能存在异常缩量。这可以用于识别市场情绪的极端变化和潜在的流动性风险。相对于参考因子仅关注成交量的变化或均值，本因子通过结合偏度和标准差，提供了更全面的成交量分布特征信息。
    因子应用场景：
    1. 识别市场情绪的极端变化
    2. 潜在的流动性风险预警
    3. 异常放量或缩量识别
    """
    # 1. 计算 ts_skewness(vol, 120)
    data_ts_skewness_vol = ts_skewness(data['vol'], d = 120)
    # 2. 计算 ts_std_dev(vol, 120)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], d = 120)
    # 3. 计算 divide(ts_skewness(vol, 120), ts_std_dev(vol, 120))
    factor = divide(data_ts_skewness_vol, data_ts_std_dev_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()