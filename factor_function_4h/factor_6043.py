import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import rank
from operators import ts_entropy
from operators import ts_corr
from operators import ts_mean
from operators import adv
from operators import divide
import pandas as pd

def factor_6043(data, **kwargs):
    """
    因子名称: VolEntropyPriceCorrRatio_10949
    数学表达式: divide(rank(ts_entropy(vol, 15)), max(ts_corr(close, open, 15), ts_mean(adv(30), 15)))
    中文描述: 该因子旨在捕捉交易量波动与价格日内趋势及长期交易量之间的相对关系。首先，计算过去15天成交量的信息熵并进行排名，衡量交易量的混乱程度。然后，取过去15天收盘价与开盘价相关性以及过去30天平均交易量的15天均值中的最大值。最后，将成交量信息熵的排名除以这个最大值。这个因子通过比例关系来量化交易量不确定性相对于价格趋势和长期交易活动强度的相对重要性，可能用于识别在不同市场环境下表现独特的股票。
    因子应用场景：
    1. 市场波动性评估：用于评估交易量信息熵相对于价格趋势和长期交易量的重要性，从而判断市场波动性。
    2. 股票选择：识别在特定市场环境下表现独特的股票，例如交易量波动性较高但价格趋势稳定的股票。
    """
    # 1. 计算 ts_entropy(vol, 15)
    data_ts_entropy = ts_entropy(data['vol'], d=15)
    # 2. 计算 rank(ts_entropy(vol, 15))
    data_rank_ts_entropy = rank(data_ts_entropy, rate=2)
    # 3. 计算 ts_corr(close, open, 15)
    data_ts_corr = ts_corr(data['close'], data['open'], d=15)
    # 4. 计算 adv(30)
    data_adv = adv(data['vol'], d=30)
    # 5. 计算 ts_mean(adv(30), 15)
    data_ts_mean = ts_mean(data_adv, d=15)
    # 6. 计算 max(ts_corr(close, open, 15), ts_mean(adv(30), 15))
    data_max = max(data_ts_corr, data_ts_mean)
    # 7. 计算 divide(rank(ts_entropy(vol, 15)), max(ts_corr(close, open, 15), ts_mean(adv(30), 15)))
    factor = divide(data_rank_ts_entropy, data_max)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()