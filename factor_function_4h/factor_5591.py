import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_min_diff, multiply, divide

def factor_5591(data, **kwargs):
    """
    因子名称: factor_volatility_adjusted_ts_min_diff_83399
    数学表达式: multiply(close, ts_min_diff(divide(close, ts_std_dev(close, 20)), 77), filter=True)
    中文描述: 本因子旨在捕捉经过波动率调整后的收盘价与一段时间内最低波动率调整收盘价之间的差异。首先，通过将收盘价除以其20日标准差，对收盘价进行波动率调整，目的是标准化不同股票或同一股票不同时期的价格波动性。然后，计算调整后的收盘价与过去77天内最低调整收盘价的差值。最后，将这个差值乘以原始收盘价，以放大那些当前价格较高，且相对其波动率调整后的历史低点有较大差异的股票的信号。该因子适用于识别那些在经历了一段低波动率时期后，价格开始显著上涨的股票，可能预示着潜在的趋势反转或加速上涨的机会。
    因子应用场景：
    1. 趋势反转识别：用于识别经历低波动率后价格开始显著上涨的股票。
    2. 波动率标准化：通过波动率调整，使得不同股票或同一股票不同时期的价格波动性可以比较。
    """
    # 1. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], 20)
    # 2. 计算 divide(close, ts_std_dev(close, 20))
    data_divide = divide(data['close'], data_ts_std_dev)
    # 3. 计算 ts_min_diff(divide(close, ts_std_dev(close, 20)), 77)
    data_ts_min_diff = ts_min_diff(data_divide, 77)
    # 4. 计算 multiply(close, ts_min_diff(divide(close, ts_std_dev(close, 20)), 77), filter=True)
    factor = multiply(data['close'], data_ts_min_diff, filter=True)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()