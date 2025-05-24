import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5940(data, **kwargs):
    """
    因子名称: VolumeVolatility_PriceCorrelation_Ratio_84490
    数学表达式: divide(ts_std_dev(vol, 90), abs(ts_corr(close, vol, 30)))
    中文描述: 该因子旨在捕捉长期交易量波动性与短期价格-交易量相关性之间的关系。首先，它计算了过去90天交易量的标准差，衡量了长期交易量的波动程度。
            然后，计算了过去30天收盘价与交易量的相关性的绝对值，衡量了短期内价格和交易量变动的同步性。最后，将长期交易量标准差除以短期价格-交易量相关性的绝对值。
            这个因子试图识别那些在长期内交易量波动较大，但在短期内价格和交易量同步性较低的股票。这可能暗示着长期资金的活跃度较高，但短期市场情绪并不完全支持当前的价格走势，可能是一个潜在的反转信号。
            相较于参考因子，创新点在于使用了长期（90天）的交易量波动性，并将其与短期（30天）的价量相关性进行比值计算，而不是直接使用交易量变化量。
            这是一种新的组合方式，旨在从不同时间维度捕捉交易量和价格信息，并探索它们之间的非线性关系，以期获得更稳定的预测能力。
    因子应用场景：
    1. 反转信号识别：因子值较高可能暗示潜在的反转机会。
    2. 交易量分析：用于识别交易量波动较大但价格和交易量同步性较低的股票。
    """
    # 1. 计算 ts_std_dev(vol, 90)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], d = 90)
    # 2. 计算 ts_corr(close, vol, 30)
    data_ts_corr_close_vol = ts_corr(data['close'], data['vol'], d = 30)
    # 3. 计算 abs(ts_corr(close, vol, 30))
    data_abs_ts_corr_close_vol = abs(data_ts_corr_close_vol)
    # 4. 计算 divide(ts_std_dev(vol, 90), abs(ts_corr(close, vol, 30)))
    factor = divide(data_ts_std_dev_vol, data_abs_ts_corr_close_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()