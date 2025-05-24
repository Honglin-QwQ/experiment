import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5756(data, **kwargs):
    """
    因子名称: Volume_Weighted_Price_Momentum_Anomaly_94149
    数学表达式: ts_zscore(ts_covariance(ts_returns(vwap, 3), vol, 5), 20) - ts_zscore(ts_covariance(ts_returns(vwap, 3), amount, 5), 20)
    中文描述: 该因子旨在捕捉成交量加权平均价（VWAP）短期动量与成交量和交易额之间的异常关系。首先，计算过去3天VWAP的收益率，这代表了VWAP的短期动量。然后，计算该VWAP动量与成交量在过去5天内的协方差，以及VWAP动量与交易额在过去5天内的协方差。接着，分别计算这两个协方差序列在过去20天内的Z分数。最后，用VWAP动量与成交量协方差的Z分数减去VWAP动量与交易额协方差的Z分数。正值可能表示VWAP的短期上涨伴随着成交量和交易额的同步增加，暗示趋势的持续性。负值则可能表示VWAP的短期下跌伴随着成交量和交易额的增加，暗示潜在的抄底或反弹机会。相较于参考因子，创新点在于引入了VWAP的短期动量，并分别考察了其与成交量和交易额的协方差，通过Z分数标准化后进行比较，以更精细地捕捉价格、成交量和交易额之间的动态关系。改进建议中提到的引入动量因素和尝试不同时间窗口的思路也体现在了该因子的构建中。
    因子应用场景：
    1. 趋势识别：用于识别VWAP短期动量与成交量和交易额之间关系，判断趋势持续性。
    2. 反转机会：寻找VWAP短期下跌伴随成交量和交易额增加的情况，辅助判断潜在的抄底或反弹机会。
    """
    # 1. 计算 ts_returns(vwap, 3)
    data_ts_returns_vwap = ts_returns(data['vwap'], 3)
    # 2. 计算 ts_covariance(ts_returns(vwap, 3), vol, 5)
    data_ts_covariance_vol = ts_covariance(data_ts_returns_vwap, data['vol'], 5)
    # 3. 计算 ts_covariance(ts_returns(vwap, 3), amount, 5)
    data_ts_covariance_amount = ts_covariance(data_ts_returns_vwap, data['amount'], 5)
    # 4. 计算 ts_zscore(ts_covariance(ts_returns(vwap, 3), vol, 5), 20)
    data_ts_zscore_vol = ts_zscore(data_ts_covariance_vol, 20)
    # 5. 计算 ts_zscore(ts_covariance(ts_returns(vwap, 3), amount, 5), 20)
    data_ts_zscore_amount = ts_zscore(data_ts_covariance_amount, 20)
    # 6. 计算 ts_zscore(ts_covariance(ts_returns(vwap, 3), vol, 5), 20) - ts_zscore(ts_covariance(ts_returns(vwap, 3), amount, 5), 20)
    factor = subtract(data_ts_zscore_vol, data_ts_zscore_amount)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()