import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_delta, sign, subtract, adv, multiply
import pandas as pd

def factor_5684(data, **kwargs):
    """
    数学表达式: rank(multiply(ts_delta(close, 3), sign(subtract(vol, adv(vol, 10)))))
    中文描述: 该因子旨在捕捉价格动量与成交量变化方向之间的关系，并对结果进行排序，以消除异常值的影响。首先计算收盘价的3日差值，反映短期价格动量。
            然后，计算成交量与10日平均成交量的差值，并取其符号，表示成交量相对于平均水平是增加还是减少。
            将价格动量与成交量变化方向相乘，如果价格上涨且成交量增加，或者价格下跌且成交量减少，则因子值为正，反之为负。
            最后，对因子值进行排序，得到每个交易日内股票的相对排名。创新点在于简化了原因子的表达式，移除了Z-score，并使用成交量变化方向代替成交量变化幅度，从而减少了对异常值的敏感性。
    因子应用场景：
    1. 趋势识别：当因子值较高时，表明价格上涨且成交量增加，或者价格下跌且成交量减少，可能意味着当前趋势较强且稳定。
    2. 市场同步性分析：因子有助于识别市场中价格变化与成交量同步性较高的股票，这些股票可能对市场整体趋势更为敏感。
    """
    # 1. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], d=3)
    # 2. 计算 adv(vol, 10)
    data_adv_vol = adv(data['vol'], d=10)
    # 3. 计算 subtract(vol, adv(vol, 10))
    data_subtract_vol_adv_vol = subtract(data['vol'], data_adv_vol)
    # 4. 计算 sign(subtract(vol, adv(vol, 10)))
    data_sign_subtract_vol_adv_vol = sign(data_subtract_vol_adv_vol)
    # 5. 计算 multiply(ts_delta(close, 3), sign(subtract(vol, adv(vol, 10))))
    data_multiply = multiply(data_ts_delta_close, data_sign_subtract_vol_adv_vol)
    # 6. 计算 rank(multiply(ts_delta(close, 3), sign(subtract(vol, adv(vol, 10)))))
    factor = rank(data_multiply, rate=2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()