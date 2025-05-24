import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, multiply, ts_delta

def factor_5745(data, **kwargs):
    """
    因子名称: VWAP_LowPrice_Momentum_Decay_91728
    数学表达式: ts_decay_linear(multiply(ts_delta(vwap, 5), ts_delta(low, 5)), 10)
    中文描述: 该因子结合了VWAP和最低价的短期动量，并应用线性衰减。首先，计算过去5天VWAP和最低价的差值（即短期动量），然后将这两个动量相乘。最后，对乘积结果在过去10天内应用线性衰减。这个因子旨在捕捉短期价格和成交量加权价格动量的联合效应，并通过衰减赋予近期数据更高的权重，以反映市场情绪的最新变化。当VWAP和最低价都呈现积极的短期动量时，因子值较高，可能预示着上涨趋势的延续；反之，则可能预示着下跌趋势。相较于参考因子，该因子创新性地结合了两个不同的价格指标的短期动量，并通过乘法和衰减增加了复杂性和对近期数据的敏感性。
    因子应用场景：
    1. 短期趋势识别：当因子值较高时，表明VWAP和最低价都呈现积极的短期动量，可能预示着上涨趋势的延续。
    2. 市场情绪变化：通过衰减赋予近期数据更高的权重，反映市场情绪的最新变化。
    """
    # 1. 计算 ts_delta(vwap, 5)
    data_ts_delta_vwap = ts_delta(data['vwap'], 5)
    # 2. 计算 ts_delta(low, 5)
    data_ts_delta_low = ts_delta(data['low'], 5)
    # 3. 计算 multiply(ts_delta(vwap, 5), ts_delta(low, 5))
    data_multiply = multiply(data_ts_delta_vwap, data_ts_delta_low)
    # 4. 计算 ts_decay_linear(multiply(ts_delta(vwap, 5), ts_delta(low, 5)), 10)
    factor = ts_decay_linear(data_multiply, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()