import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import kth_element
from operators import ts_max_diff
from operators import ts_std_dev
from operators import multiply
import pandas as pd

def factor_5850(data, **kwargs):
    """
    因子名称: Volatility_Weighted_Open_Diff_17171
    数学表达式: multiply(ts_max_diff(kth_element(open, 7, k=1), 45), ts_std_dev(kth_element(open, 7, k=1), 4))
    中文描述: 《波动加权开盘价差异因子：捕捉市场开盘情绪与波动》
    
    因子逻辑:
    这个因子首先提取过去7天中每日开盘价的第一个记录，这有助于处理潜在的数据缺失。然后，计算这个提取出的值与过去45天中该值的最大值的差值，这捕捉了当前开盘价相对于近期高点的相对位置。同时，计算过去4天中提取出的开盘价的波动性。最后，将这两部分结果相乘，得到最终的因子值。
    
    因子应用场景：
    这个因子结合了开盘价的相对强度和短期波动性。ts_max_diff部分衡量了当前开盘价相对于过去较长一段时间内最高开盘价的差异，反映了开盘时的相对强弱。ts_std_dev部分则衡量了过去几天开盘价的波动性，反映了市场在开盘时情绪的不确定性或活跃度。将这两者相乘，旨在捕捉那种在开盘时表现出一定相对强度（或弱势）并且伴随有较高短期波动的股票。
    """
    # 1. 计算 kth_element(open, 7, k=1)
    data_kth_element = kth_element(data['open'], d=7, k=1)
    
    # 2. 计算 ts_max_diff(kth_element(open, 7, k=1), 45)
    data_ts_max_diff = ts_max_diff(data_kth_element, d=45)
    
    # 3. 计算 ts_std_dev(kth_element(open, 7, k=1), 4)
    data_ts_std_dev = ts_std_dev(data_kth_element, d=4)
    
    # 4. 计算 multiply(ts_max_diff(kth_element(open, 7, k=1), 45), ts_std_dev(kth_element(open, 7, k=1), 4))
    factor = multiply(data_ts_max_diff, data_ts_std_dev)
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()