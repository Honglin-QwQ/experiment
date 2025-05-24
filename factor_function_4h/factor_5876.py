import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide
from operators import ts_delta
import pandas as pd

def factor_5876(data, **kwargs):
    """
    因子名称: VolWeightedPriceChangeRatio_79270
    数学表达式: divide(ts_delta(amount, 1), ts_delta(vol, 1))
    中文描述: 该因子计算每日交易额变化量与交易量变化量之比。通过比较交易额和交易量的相对变化，可以衡量单位交易量所带来的价格变化效率。当该比值较高时，可能表明市场在较低的交易量下发生了较大的价格变动，可能预示着价格趋势的强度或潜在的供需失衡。这是一种结合了交易额和交易量信息，并关注其日度变化的创新性因子。
    因子应用场景：
    1. 价格趋势判断：比值较高可能预示着价格趋势的强度或潜在的供需失衡。
    2. 交易量分析：衡量单位交易量所带来的价格变化效率。
    """
    # 1. 计算 ts_delta(amount, 1)
    data_ts_delta_amount = ts_delta(data['amount'], d = 1)
    # 2. 计算 ts_delta(vol, 1)
    data_ts_delta_vol = ts_delta(data['vol'], d = 1)
    # 3. 计算 divide(ts_delta(amount, 1), ts_delta(vol, 1))
    factor = divide(data_ts_delta_amount, data_ts_delta_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()