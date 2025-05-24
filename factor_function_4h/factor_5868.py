import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_max_diff, add, ts_std_dev, kth_element
import pandas as pd

def factor_5868(data, **kwargs):
    """
    数学表达式: divide(ts_max_diff(kth_element(open, 7, k=1), 45), add(ts_std_dev(kth_element(open, 7, k=1), 4), 1e-6))
    中文描述: 《波动缩放开盘动量因子：捕捉开盘价相对强度与波动》
    该因子首先提取过去7天中每日开盘价的第一个记录，这有助于处理潜在的数据缺失。然后，计算这个提取出的值与过去45天中该值的最大值的差值，这捕捉了当前开盘价相对于近期高点的相对位置。同时，计算过去4天中提取出的开盘价的波动性。最后，将开盘价的相对差异除以短期波动性，得到最终的因子值。分母中加上一个很小的常数（1e-6）是为了避免除以零。
    因子应用场景：
    这个因子旨在捕捉开盘价相对于近期高点的动量，并根据短期波动性进行调整。ts_max_diff部分衡量了当前开盘价相对于过去较长一段时间内最高开盘价的差异，反映了开盘时的相对强弱和动量。ts_std_dev部分则衡量了过去几天开盘价的波动性。通过将开盘价的相对差异除以波动性，该因子对动量信号进行了波动率调整。这意味着，即使开盘价相对于近期高点有较大的提升，如果这种提升伴随着非常高的波动性，因子值可能会被“惩罚”，从而降低其权重。反之，如果开盘价的提升相对稳定（波动性较低），因子值会相对较高。这种波动率调整的动量因子可能在不同市场环境下表现更稳健。
    """
    # 1. 计算 kth_element(open, 7, k=1)
    data_kth_element = kth_element(data['open'], d=7, k=1)
    # 2. 计算 ts_max_diff(kth_element(open, 7, k=1), 45)
    data_ts_max_diff = ts_max_diff(data_kth_element, d=45)
    # 3. 计算 ts_std_dev(kth_element(open, 7, k=1), 4)
    data_ts_std_dev = ts_std_dev(data_kth_element, d=4)
    # 4. 计算 add(ts_std_dev(kth_element(open, 7, k=1), 4), 1e-6)
    data_add = add(data_ts_std_dev, 1e-6)
    # 5. 计算 divide(ts_max_diff(kth_element(open, 7, k=1), 45), add(ts_std_dev(kth_element(open, 7, k=1), 4), 1e-6))
    factor = divide(data_ts_max_diff, data_add)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()