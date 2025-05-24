import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, multiply, ts_delta

def factor_5863(data, **kwargs):
    """
    因子名称: Volumetric_Price_Momentum_Decay_70235
    数学表达式: ts_decay_exp_window(multiply(ts_delta(close, 1), vol), d=10, factor=0.75)
    中文描述: 该因子通过计算收盘价的日变化与成交量的乘积，并应用指数衰减加权平均，来衡量近期价格动量的强度，并考虑了成交量的影响。这结合了价格变动和交易活跃度，并赋予近期数据更高的权重。与参考因子相比，创新点在于结合了价格变动和成交量，并使用了指数衰减加权平均来捕捉近期趋势。高因子值可能表明近期在较高成交量下的强劲价格上涨动量，而低因子值可能表明在较高成交量下的强劲价格下跌动量。
    因子应用场景：
    1. 动量分析：用于识别近期价格动量的强度，结合成交量信息。
    2. 趋势跟踪：通过指数衰减加权平均，更关注近期趋势。
    3. 量价关系研究：考察成交量对价格动量的影响。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], d=1)
    # 2. 计算 multiply(ts_delta(close, 1), vol)
    data_multiply = multiply(data_ts_delta_close, data['vol'])
    # 3. 计算 ts_decay_exp_window(multiply(ts_delta(close, 1), vol), d=10, factor=0.75)
    factor = ts_decay_exp_window(data_multiply, d=10, factor=0.75)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()