import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_corr, ts_std_dev, divide

import pandas as pd

def factor_5911(data, **kwargs):
    """
    因子名称: VolumePriceDivergenceIndex_84948
    数学表达式: ts_rank(ts_corr(vol, close, 10), 5) - ts_rank(ts_std_dev(divide(close, open), 15), 10)
    中文描述: 该因子旨在捕捉成交量与收盘价的短期相关性排名和收盘价/开盘价比值的长期波动率排名之间的差异。首先计算过去10天成交量与收盘价的时间序列相关系数，并对其进行5天时序排名。然后计算过去15天收盘价/开盘价比值的标准差，并对其进行10天时序排名。最后，用第一个排名减去第二个排名。较高的因子值可能表明成交量与价格的短期正相关性较强，而开盘价相对稳定，这可能预示着上涨趋势的持续。创新点在于结合了量价相关性的短期时序排名和价格波动率的长期时序排名，并通过相减的方式突出它们之间的相对强弱关系，以识别潜在的量价背离或协同信号。
    因子应用场景：
    1. 量价关系分析：识别成交量与价格走势之间的背离或协同效应。
    2. 趋势判断：辅助判断上涨趋势的持续性。
    """
    # 1. 计算 ts_corr(vol, close, 10)
    data_ts_corr = ts_corr(data['vol'], data['close'], d=10)
    # 2. 计算 ts_rank(ts_corr(vol, close, 10), 5)
    data_ts_rank1 = ts_rank(data_ts_corr, d=5)
    # 3. 计算 divide(close, open)
    data_divide = divide(data['close'], data['open'])
    # 4. 计算 ts_std_dev(divide(close, open), 15)
    data_ts_std_dev = ts_std_dev(data_divide, d=15)
    # 5. 计算 ts_rank(ts_std_dev(divide(close, open), 15), 10)
    data_ts_rank2 = ts_rank(data_ts_std_dev, d=10)
    # 6. 计算 ts_rank(ts_corr(vol, close, 10), 5) - ts_rank(ts_std_dev(divide(close, open), 15), 10)
    factor = data_ts_rank1 - data_ts_rank2

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()