import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_corr, ts_std_dev
import pandas as pd

def factor_6030(data, **kwargs):
    """
    因子名称: Volume_Price_Correlation_Volatility_Ratio_36449
    数学表达式: divide(ts_corr(close, volume, 20), ts_std_dev(close, 30))
    中文描述: 该因子旨在捕捉价格与成交量相关性相对于近期价格波动率的相对强度。它首先计算过去20个交易日收盘价和成交量的相关系数，以衡量价量之间的同步程度。然后，计算过去30个交易日收盘价的标准差，以衡量价格的波动性。最后，将价量相关系数除以价格标准差。该因子认为，在价格波动率较低时，即使是中等的价量相关性也可能具有更强的信号意义。创新点在于：1. 直接使用了收盘价和成交量的相关性，简化了参考因子中复杂的加权平均和排名逻辑；2. 将价量相关性与价格自身的波动率相结合，提供了一个标准化的衡量指标；3. 结合了评估报告中提出的简化逻辑和关注量价关系的建议，并使用了ts_corr和ts_std_dev操作符。该因子可能适用于识别在相对稳定市场环境下，价量关系出现异常变化的股票。
    因子应用场景：
    1. 识别在价格波动率较低时，价量关系出现异常变化的股票。
    2. 辅助判断市场稳定环境下，量价关系对股票的影响。
    """
    # 1. 计算 ts_corr(close, volume, 20)
    data_ts_corr = ts_corr(data['close'], data['vol'], 20)
    # 2. 计算 ts_std_dev(close, 30)
    data_ts_std_dev = ts_std_dev(data['close'], 30)
    # 3. 计算 divide(ts_corr(close, volume, 20), ts_std_dev(close, 30))
    factor = divide(data_ts_corr, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()