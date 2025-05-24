import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5820(data, **kwargs):
    """
    因子名称: Volume_Weighted_ArgMax_Volatility_Ratio_13110
    数学表达式: divide(ts_std_dev(multiply(close, vol), 45), add(ts_arg_max(multiply(high, vol), 75), 1))
    中文描述: 该因子旨在捕捉成交量加权价格波动的强度与成交量加权最高价近期出现位置之间的关系。首先，计算过去45天收盘价乘以成交量的标准差，衡量成交量加权收盘价的波动性。然后，计算过去75天最高价乘以成交量最大值的相对索引（加上1避免除以零）。最后，将成交量加权收盘价的波动性除以成交量加权最高价最大值的相对索引（加1），形成因子。该因子结合了成交量信息，对价格波动和高点位置进行加权，旨在更全面地反映市场动态。较高的成交量加权波动性和较小的ts_arg_max值（近期出现成交量加权最高价）可能预示着市场处于强势或潜在的顶部区域。创新点在于引入成交量加权来捕捉价格的真实交易强度，并结合成交量加权最高价的位置，形成一个反映市场强度和潜在风险的指标。相较于参考因子，本因子在波动性和位置计算中都融入了成交量信息，增强了对市场真实交易行为的捕捉能力，并继续使用比率形式，以更直观地反映两个组成部分之间的相对关系，同时避免了对噪音敏感的ts_entropy和ts_arg_min，转而使用ts_std_dev和ts_arg_max。
    因子应用场景：
    1. 市场强度判断：用于判断市场的强势程度，较高的因子值可能表示市场处于强势状态。
    2. 潜在顶部区域识别：结合成交量信息，辅助识别潜在的顶部区域。
    """
    # 1. 计算 multiply(close, vol)
    data_multiply_close_vol = multiply(data['close'], data['vol'])
    # 2. 计算 ts_std_dev(multiply(close, vol), 45)
    data_ts_std_dev = ts_std_dev(data_multiply_close_vol, d = 45)
    # 3. 计算 multiply(high, vol)
    data_multiply_high_vol = multiply(data['high'], data['vol'])
    # 4. 计算 ts_arg_max(multiply(high, vol), 75)
    data_ts_arg_max = ts_arg_max(data_multiply_high_vol, d = 75)
    # 5. 计算 add(ts_arg_max(multiply(high, vol), 75), 1)
    data_add = add(data_ts_arg_max, 1)
    # 6. 计算 divide(ts_std_dev(multiply(close, vol), 45), add(ts_arg_max(multiply(high, vol), 75), 1))
    factor = divide(data_ts_std_dev, data_add)

    # 删除中间变量
    del data_multiply_close_vol
    del data_ts_std_dev
    del data_multiply_high_vol
    del data_ts_arg_max
    del data_add

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()