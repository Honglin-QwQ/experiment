import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import inverse
from operators import ts_weighted_decay
from operators import subtract
from operators import divide
from operators import adv

def factor_6025(data, **kwargs):
    """
    因子名称: InverseWeightedDecay_PriceVolumeDiff_19695
    数学表达式: inverse(ts_weighted_decay(subtract(divide(close, open), divide(vol, adv(vol, 20))), k=0.7))
    中文描述: 该因子计算收盘价与开盘价之比以及当前成交量与20日平均成交量之比的差值，然后对这个差值应用加权衰减（当日权重0.7），最后取其倒数。该因子结合了价格变动和成交量相对强弱的信息，并通过加权衰减赋予近期数据更高权重，取倒数旨在将负向预测转化为正向预测。这可能用于识别价格和成交量背离引起的潜在反转信号。
    因子应用场景：
    1. 反转信号识别：用于识别价格和成交量背离引起的潜在反转信号。
    2. 量价关系分析：结合价格变动和成交量相对强弱的信息，辅助判断趋势的可持续性。
    """
    # 1. 计算 divide(close, open)
    data_divide_close_open = divide(data['close'], data['open'])
    # 2. 计算 adv(vol, 20)
    data_adv_vol = adv(data['vol'], d = 20)
    # 3. 计算 divide(vol, adv(vol, 20))
    data_divide_vol_adv_vol = divide(data['vol'], data_adv_vol)
    # 4. 计算 subtract(divide(close, open), divide(vol, adv(vol, 20)))
    data_subtract = subtract(data_divide_close_open, data_divide_vol_adv_vol)
    # 5. 计算 ts_weighted_decay(subtract(divide(close, open), divide(vol, adv(vol, 20))), k=0.7)
    data_ts_weighted_decay = ts_weighted_decay(data_subtract, k=0.7)
    # 6. 计算 inverse(ts_weighted_decay(subtract(divide(close, open), divide(vol, adv(vol, 20))), k=0.7))
    factor = inverse(data_ts_weighted_decay)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()