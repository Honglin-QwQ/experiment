import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, abs, subtract, ts_delay, add, signed_power
import pandas as pd
import numpy as np

def factor_5611(data, **kwargs):
    """
    因子名称: factor_trade_volume_adjusted_volatility_67269
    数学表达式: divide(ts_std_dev(abs(divide(subtract(close, ts_delay(close, 1)), ts_delay(close, 1))), 20), signed_power(add(vol, 1), 0.5))
    中文描述: 该因子旨在衡量交易量调整后的波动率。它首先计算每日收益率的绝对值，然后计算过去20天收益率标准差，最后除以交易量的平方根加1的0.5次幂。该因子的创新之处在于使用交易量作为波动率的调整因子，从而在一定程度上消除交易活跃度对波动率的影响。使用signed_power是为了防止出现负数开根号的情况。该因子可以用于识别具有更高波动率但交易相对不活跃的股票，可能表明市场关注度较低但潜在风险较高的投资标的。
    因子应用场景：
    1. 波动率分析：用于衡量交易量调整后的波动率，可以更准确地反映股票的风险水平。
    2. 交易策略：可以用于识别具有更高波动率但交易相对不活跃的股票，作为选股的参考指标。
    3. 风险管理：可以用于评估投资组合的风险，特别是在交易量较低的情况下。
    """
    # 1. 计算 subtract(close, ts_delay(close, 1))
    data_subtract = subtract(data['close'], ts_delay(data['close'], 1))
    # 2. 计算 ts_delay(close, 1)
    data_ts_delay = ts_delay(data['close'], 1)
    # 3. 计算 divide(subtract(close, ts_delay(close, 1)), ts_delay(close, 1))
    data_divide = divide(data_subtract, data_ts_delay)
    # 4. 计算 abs(divide(subtract(close, ts_delay(close, 1)), ts_delay(close, 1)))
    data_abs = abs(data_divide)
    # 5. 计算 ts_std_dev(abs(divide(subtract(close, ts_delay(close, 1)), ts_delay(close, 1))), 20)
    data_ts_std_dev = ts_std_dev(data_abs, 20)
    # 6. 计算 add(vol, 1)
    data_add = add(data['vol'], 1)
    # 7. 计算 signed_power(add(vol, 1), 0.5)
    data_signed_power = signed_power(data_add, 0.5)
    # 8. 计算 divide(ts_std_dev(abs(divide(subtract(close, ts_delay(close, 1)), ts_delay(close, 1))), 20), signed_power(add(vol, 1), 0.5))
    factor = divide(data_ts_std_dev, data_signed_power)
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()