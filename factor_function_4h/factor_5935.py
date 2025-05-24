import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, multiply, sign, ts_delta, tanh

def factor_5935(data, **kwargs):
    """
    因子名称: Volatility_Weighted_Price_Direction_Decay_10195
    数学表达式: ts_decay_linear(multiply(sign(ts_delta(close, 5)), tanh(vol)), 12)
    中文描述: 该因子计算过去12天内，过去5天收盘价变化方向（上涨为1，下跌为-1，不变为0）与当前交易量经过tanh函数处理后的乘积的线性衰减加权平均值。它旨在捕捉价格变动方向与交易活跃度的非线性关系，并赋予近期数据更高的权重。相较于参考因子直接相乘，本因子通过sign函数分离价格变动方向，并使用tanh函数对交易量进行非线性加权，使得因子对交易量的敏感度在一定范围内线性增加，超过一定值后增加变缓，从而更稳健地反映市场情绪和动量。正值可能表明近期价格上涨伴随交易活跃，负值则反之。该因子可以用于识别具有持续价量驱动的趋势，或作为趋势反转的早期信号。
    因子应用场景：
    1. 趋势识别：识别价格上涨或下跌趋势与交易量之间的关系。
    2. 市场情绪分析：通过量价关系判断市场情绪。
    3. 趋势反转信号：捕捉趋势可能反转的早期信号。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], d = 5)
    # 2. 计算 sign(ts_delta(close, 5))
    data_sign_ts_delta_close = sign(data_ts_delta_close)
    # 3. 计算 tanh(vol)
    data_tanh_vol = tanh(data['vol'])
    # 4. 计算 multiply(sign(ts_delta(close, 5)), tanh(vol))
    data_multiply = multiply(data_sign_ts_delta_close, data_tanh_vol)
    # 5. 计算 ts_decay_linear(multiply(sign(ts_delta(close, 5)), tanh(vol)), 12)
    factor = ts_decay_linear(data_multiply, d = 12)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()