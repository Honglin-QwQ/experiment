import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, subtract, ts_min, multiply, adv, ts_std_dev

def factor_5800(data, **kwargs):
    """
    因子名称: VolatilityAdjustedOpenLowRatio_89023
    数学表达式: divide(subtract(open, ts_min(low, 30)), multiply(adv(vol, 30), ts_std_dev(close, 30)))
    中文描述: 该因子计算开盘价与过去30天最低价的差值，并用过去30天平均成交量和过去30天收盘价标准差的乘积进行标准化。它旨在捕捉开盘价相对于近期低点的强势程度，同时考虑成交量的放大效应和市场的波动性。当开盘价远高于近期低点，且成交量和波动性较大时，因子值较高，可能预示着强劲的市场动能。创新点在于引入了波动率作为标准化的一个维度，使得因子更能适应不同波动环境下的市场表现。此外，将时间窗口调整为30天，以捕捉更中期的趋势。
    因子应用场景：
    1. 强势程度：捕捉开盘价相对于近期低点的强势程度。
    2. 市场动能：预示着强劲的市场动能。
    """
    # 1. 计算 ts_min(low, 30)
    data_ts_min_low = ts_min(data['low'], d = 30)
    # 2. 计算 subtract(open, ts_min(low, 30))
    data_subtract = subtract(data['open'], data_ts_min_low)
    # 3. 计算 adv(vol, 30)
    data_adv_vol = adv(data['vol'], d = 30)
    # 4. 计算 ts_std_dev(close, 30)
    data_ts_std_dev_close = ts_std_dev(data['close'], d = 30)
    # 5. 计算 multiply(adv(vol, 30), ts_std_dev(close, 30))
    data_multiply = multiply(data_adv_vol, data_ts_std_dev_close)
    # 6. 计算 divide(subtract(open, ts_min(low, 30)), multiply(adv(vol, 30), ts_std_dev(close, 30)))
    factor = divide(data_subtract, data_multiply)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()