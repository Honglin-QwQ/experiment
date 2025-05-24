import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_quantile, divide
import pandas as pd

def factor_5836(data, **kwargs):
    """
    因子名称: Volatility_Quantile_Correlation_81650
    数学表达式: ts_corr(ts_quantile(high/low-1, 20, driver='uniform'), ts_quantile(close, 60, driver='gaussian'), 10)
    中文描述: 该因子结合了波动率和收盘价的时间序列分位数信息，并计算它们在短期内的相关性。首先，计算每日的振幅 (high/low - 1) 并获取其过去20天的均匀分布分位数。同时，计算收盘价在过去60天的高斯分布分位数。最后，计算这两个分位数序列在过去10天的相关性。这个因子旨在捕捉市场在不同时间尺度上的价格变动和波动性之间的动态关系，通过分位数转换引入非线性特征，并利用相关性衡量其同步性，可能用于识别潜在的价格反转或趋势延续信号。
    因子应用场景：
    1. 波动性分析：用于识别市场波动性与价格变化之间的关系。
    2. 趋势预测：可能用于识别潜在的价格反转或趋势延续信号。
    """
    # 1. 计算 high/low - 1
    data['amplitude'] = divide(data['high'], data['low']) - 1
    # 2. 计算 ts_quantile(high/low-1, 20, driver='uniform')
    data_ts_quantile_amplitude = ts_quantile(data['amplitude'], d=20, driver='uniform')
    # 3. 计算 ts_quantile(close, 60, driver='gaussian')
    data_ts_quantile_close = ts_quantile(data['close'], d=60, driver='gaussian')
    # 4. 计算 ts_corr(ts_quantile(high/low-1, 20, driver='uniform'), ts_quantile(close, 60, driver='gaussian'), 10)
    factor = ts_corr(data_ts_quantile_amplitude, data_ts_quantile_close, d=10)
    # 5. 删除中间变量
    del data['amplitude']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()