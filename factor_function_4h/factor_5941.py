import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_delay, ts_decay_linear

import pandas as pd

def factor_5941(data, **kwargs):
    """
    因子名称: VWAP_Price_Momentum_Decay_Ratio_51822
    数学表达式: divide(ts_decay_linear(divide(vwap, ts_delay(vwap, 1)), 10), ts_decay_linear(divide(close, ts_delay(close, 1)), 10))
    中文描述: 该因子计算过去10天VWAP日收益率的线性衰减加权平均值与过去10天收盘价日收益率的线性衰减加权平均值的比值。参考了divide, ts_delay和ts_decay_linear运算符，以及vwap和close数据。创新点在于结合了价格动量（日收益率）和线性衰减加权平均，试图捕捉VWAP和收盘价动量中近期数据的更重要影响，并分析两者动量衰减的相对强度。这可能用于识别市场动量结构的细微变化或潜在的动量反转信号。该因子在结构上借鉴了历史输出中比率的思想，并在分子分母中引入了更复杂的动量和衰减逻辑，以提高预测能力和捕捉市场动态变化。
    因子应用场景：
    1. 动量分析：用于识别VWAP和收盘价动量之间的相对强度，可能预示着趋势的加速或减速。
    2. 反转信号：当因子值极端时，可能表明市场过度反应，从而产生潜在的反转机会。
    3. 市场结构分析：用于分析市场动量结构的细微变化，帮助理解市场参与者的行为。
    """
    # 1. 计算 divide(vwap, ts_delay(vwap, 1))
    vwap_ratio = divide(data['vwap'], ts_delay(data['vwap'], 1))
    # 2. 计算 ts_decay_linear(divide(vwap, ts_delay(vwap, 1)), 10)
    vwap_decay = ts_decay_linear(vwap_ratio, 10)
    # 3. 计算 divide(close, ts_delay(close, 1))
    close_ratio = divide(data['close'], ts_delay(data['close'], 1))
    # 4. 计算 ts_decay_linear(divide(close, ts_delay(close, 1)), 10)
    close_decay = ts_decay_linear(close_ratio, 10)
    # 5. 计算 divide(ts_decay_linear(divide(vwap, ts_delay(vwap, 1)), 10), ts_decay_linear(divide(close, ts_delay(close, 1)), 10))
    factor = divide(vwap_decay, close_decay)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()