import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_delta, ts_std_dev, log
import pandas as pd
import numpy as np

def factor_5688(data, **kwargs):
    """
    因子名称: factor_0002_34674
    数学表达式: ts_zscore(ts_delta(ts_std_dev(log(close), 22), 5), 10)
    中文描述: 该因子基于历史因子factor_0001改进而来，factor_0001的表达式为ts_zscore(ts_delta(ts_std_dev(returns, 22), 5), 10)，该因子旨在捕捉市场波动率变化的动量。factor_0002使用log(close)代替returns，使得因子对于价格的微小变化更加敏感。首先计算过去22天收益率的标准差，然后计算该标准差的5日差分，最后对该差分进行10日Z-score标准化。该因子试图识别波动率上升或下降的趋势，并将其标准化，以便更好地比较不同股票之间的波动率变化。
    因子应用场景：
    1. 波动率趋势识别：识别波动率上升或下降的趋势。
    2. 股票比较：标准化波动率变化，便于比较不同股票之间的波动率变化。
    """
    # 1. 计算 log(close)
    data['log_close'] = log(data['close'])
    # 2. 计算 ts_std_dev(log(close), 22)
    data['std_dev'] = ts_std_dev(data['log_close'], d=22)
    # 3. 计算 ts_delta(ts_std_dev(log(close), 22), 5)
    data['delta'] = ts_delta(data['std_dev'], d=5)
    # 4. 计算 ts_zscore(ts_delta(ts_std_dev(log(close), 22), 5), 10)
    factor = ts_zscore(data['delta'], d=10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor

    del data['log_close']
    del data['std_dev']
    del data['delta']

    return data.sort_index()