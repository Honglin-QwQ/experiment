import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_std_dev, ts_skewness
import pandas as pd

def factor_5930(data, **kwargs):
    """
    因子名称: Volatility_Skewness_Momentum_96379
    数学表达式: ts_corr(ts_std_dev(close, 20), ts_skewness(returns, 60), 30)
    中文描述: 该因子计算过去30天收盘价的20天滚动标准差（衡量短期波动性）与过去60天收益率的滚动偏度（衡量收益分布的非对称性）之间的相关性。创新的地方在于结合了不同时间窗口的波动性和偏度指标，并通过相关性来捕捉市场情绪和价格动量之间的复杂关系。正相关可能表明在波动加剧时，收益分布更偏向正值，可能预示着上涨动量；负相关则可能相反。该因子可用于识别市场情绪变化和潜在的价格趋势反转。
    因子应用场景：
    1. 市场情绪识别：通过波动性和偏度的相关性，识别市场情绪的变化。
    2. 趋势反转预测：寻找因子值变化与价格趋势反转之间的关系。
    """
    # 1. 计算 ts_std_dev(close, 20)
    data_ts_std_dev_close = ts_std_dev(data['close'], 20)
    # 2. 计算 ts_skewness(returns, 60)
    data_ts_skewness_returns = ts_skewness(data['returns'], 60)
    # 3. 计算 ts_corr(ts_std_dev(close, 20), ts_skewness(returns, 60), 30)
    factor = ts_corr(data_ts_std_dev_close, data_ts_skewness_returns, 30)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()