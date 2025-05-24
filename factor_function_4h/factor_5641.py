import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5641(data, **kwargs):
    """
    数学表达式: ts_delta(signed_power(ts_max_diff(kth_element(vwap, 6, k=1), 53), 2), 5)
    中文描述: 该因子基于VWAP偏离的跨期最大差分因子的平方的差分。首先计算过去6天内VWAP的第一个有效值与过去53天内的最大VWAP值之间的差值，然后对该差值进行平方，并计算其5日差分。该因子旨在捕捉VWAP偏离程度的加速或减速变化，可能用于识别价格趋势的转折点。
    因子应用场景：
    1. 趋势转折点识别：当因子值出现显著变化时，可能预示着价格趋势即将发生转变。
    2. 短期交易策略：该因子可以用于短期交易策略，例如在因子值达到极端水平时进行反向操作。
    """
    # 1. 计算 kth_element(vwap, 6, k=1)
    data_kth_element = kth_element(data['vwap'], 6, k=1)
    # 2. 计算 ts_max_diff(kth_element(vwap, 6, k=1), 53)
    data_ts_max_diff = ts_max_diff(data_kth_element, 53)
    # 3. 计算 signed_power(ts_max_diff(kth_element(vwap, 6, k=1), 53), 2)
    data_signed_power = signed_power(data_ts_max_diff, 2)
    # 4. 计算 ts_delta(signed_power(ts_max_diff(kth_element(vwap, 6, k=1), 53), 2), 5)
    factor = ts_delta(data_signed_power, 5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()