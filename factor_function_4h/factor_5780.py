import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import divide, add, floor, multiply, ts_min, adv
import pandas as pd

def factor_5780(data, **kwargs):
    """
    因子名称: VolWeightedPriceFloorRatio_19909
    数学表达式: divide(open, add(floor(open), multiply(ts_min(low, 504), divide(vol, adv(vol, 10)))))
    中文描述: 该因子计算开盘价与一个动态基准的比值。这个动态基准由开盘价的向下取整部分加上一个由过去504天的最低价和当前成交量与短期平均成交量比值加权的项组成。当开盘价相对于这个成交量加权的最低价基准较高时，因子值较大，反之亦然。这结合了对整数价位的心理效应（通过floor(open)）和基于历史最低价与成交量动态变化的支撑/阻力水平的考量。创新点在于将历史最低价与成交量信息动态结合，构建一个更具市场敏感性的基准，而不仅仅是简单的整数价位或历史极值。
    因子应用场景：
    1. 趋势识别：因子值较高时，可能表明市场对当前价格的认可度较高，趋势较强。
    2. 支撑/阻力判断：结合历史最低价和成交量信息，辅助判断支撑和阻力位。
    """
    # 1. 计算 floor(open)
    data_floor_open = floor(data['open'])
    # 2. 计算 ts_min(low, 504)
    data_ts_min = ts_min(data['low'], 504)
    # 3. 计算 adv(vol, 10)
    data_adv_vol = adv(data['vol'], 10)
    # 4. 计算 divide(vol, adv(vol, 10))
    data_divide_vol_adv = divide(data['vol'], data_adv_vol)
    # 5. 计算 multiply(ts_min(low, 504), divide(vol, adv(vol, 10)))
    data_multiply = multiply(data_ts_min, data_divide_vol_adv)
    # 6. 计算 add(floor(open), multiply(ts_min(low, 504), divide(vol, adv(vol, 10))))
    data_add = add(data_floor_open, data_multiply)
    # 7. 计算 divide(open, add(floor(open), multiply(ts_min(low, 504), divide(vol, adv(vol, 10)))))
    factor = divide(data['open'], data_add)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()