import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5755(data, **kwargs):
    """
    数学表达式: divide(ts_delta(close, 5), ts_std_dev(returns, 10))
    中文描述: 该因子衡量了过去5天收盘价变化相对于过去10天收益率波动性的比率。首先计算过去5天的收盘价差（ts_delta(close, 5)），捕捉短期价格动量。然后计算过去10天日收益率的标准差（ts_std_dev(returns, 10)），衡量短期市场波动性。最后将价格变化除以波动性，得到一个波动性调整后的价格变化指标。该因子创新点在于结合了短期价格变化和短期波动性，旨在识别在低波动环境下出现的潜在均值回归机会或在高波动环境下价格变化的相对强度。较高的因子值可能表明价格在相对较低的波动下出现了显著上涨，或者在较高波动下价格变化相对较小，这可能预示着趋势的持续或反转。
    因子应用场景：
    1. 均值回归：识别在低波动率环境下价格出现异常变动的股票，这些股票可能存在均值回归的机会。
    2. 趋势强度：在高波动率环境下，衡量价格变动的相对强度，辅助判断趋势的持续性。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], 5)
    # 2. 计算 ts_std_dev(returns, 10)
    data_ts_std_dev = ts_std_dev(data['returns'], 10)
    # 3. 计算 divide(ts_delta(close, 5), ts_std_dev(returns, 10))
    factor = divide(data_ts_delta, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()