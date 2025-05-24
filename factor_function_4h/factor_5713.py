import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, log, multiply, ts_std_dev, divide
import pandas as pd
import numpy as np

def factor_5713(data, **kwargs):
    """
    因子名称: LogVolumeWeightedPriceSkewnessRatio_88345
    数学表达式: divide(ts_skewness(log(multiply(close, vol)), 15), ts_std_dev(log(vol), 20))
    中文描述: 该因子计算对数化成交量加权收盘价在过去15天的偏度，并将其除以对数化成交量在过去20天的标准差。它旨在捕捉对数化价量结合信号的非对称性相对于对数化成交量波动的比率。与直接使用乘积和原始偏度不同，这里对价格和成交量进行了对数处理，以平滑极端值的影响，并通过比率来衡量单位成交量波动所带来的对数化价量信号的偏度。偏度为正的比率可能表明对数化价量信号上涨伴随对数化成交量波动放大，偏度为负的比率则反之。这是一种创新的价量结合方式，通过对数变换和比率来衡量市场情绪和趋势的非线性特征，可用于识别潜在的市场反转或加速信号。
    因子应用场景：
    1. 识别市场情绪：通过观察比率的正负，判断市场是倾向于上涨还是下跌。
    2. 趋势反转信号：当比率出现极端值时，可能预示着趋势即将反转。
    3. 量价关系分析：用于衡量成交量波动对价格偏度的影响，辅助判断趋势的可靠性。
    """
    # 1. 计算 multiply(close, vol)
    data_multiply = multiply(data['close'], data['vol'])
    # 2. 计算 log(multiply(close, vol))
    data_log_multiply = log(data_multiply)
    del data_multiply
    # 3. 计算 ts_skewness(log(multiply(close, vol)), 15)
    data_ts_skewness = ts_skewness(data_log_multiply, d=15)
    del data_log_multiply
    # 4. 计算 log(vol)
    data_log_vol = log(data['vol'])
    # 5. 计算 ts_std_dev(log(vol), 20)
    data_ts_std_dev = ts_std_dev(data_log_vol, d=20)
    del data_log_vol
    # 6. 计算 divide(ts_skewness(log(multiply(close, vol)), 15), ts_std_dev(log(vol), 20))
    factor = divide(data_ts_skewness, data_ts_std_dev)
    del data_ts_skewness
    del data_ts_std_dev

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()