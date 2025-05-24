import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, multiply, ts_skewness

def factor_5738(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Skew_Decay_39242
    数学表达式: ts_decay_linear(multiply(vwap, ts_skewness(vwap, 10)), 5)
    中文描述: 该因子结合了VWAP、其短期（10天）偏度以及线性衰减。首先计算VWAP与其10天偏度的乘积，然后对这个乘积应用5天的线性衰减。VWAP反映了成交量加权平均价格，偏度衡量了价格分布的非对称性，线性衰减则赋予近期数据更高的权重。该因子旨在捕捉成交量加权价格的非对称波动特征，并强调近期趋势的影响，可能用于识别由非对称交易活动驱动的短期价格动量或反转。
    因子应用场景：
    1. 短期价格动量识别：该因子可能用于识别由非对称交易活动驱动的短期价格动量。
    2. 价格反转识别：该因子也可能用于识别价格反转的潜在信号。
    """
    # 1. 计算 ts_skewness(vwap, 10)
    data_ts_skewness = ts_skewness(data['vwap'], 10)
    # 2. 计算 multiply(vwap, ts_skewness(vwap, 10))
    data_multiply = multiply(data['vwap'], data_ts_skewness)
    # 3. 计算 ts_decay_linear(multiply(vwap, ts_skewness(vwap, 10)), 5)
    factor = ts_decay_linear(data_multiply, 5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()