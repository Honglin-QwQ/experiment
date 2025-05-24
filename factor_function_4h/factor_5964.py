import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, multiply, ts_delta, divide

def factor_5964(data, **kwargs):
    """
    数学表达式: divide(ts_std_dev(multiply(close, vol), 10), ts_std_dev(multiply(ts_delta(close, 1), vol), 10))
    中文描述: 该因子计算过去10天内成交量加权收盘价的标准差与过去10天内成交量加权日收盘价变化的标准差之比。分子反映了成交量对收盘价绝对水平波动的影响，分母反映了成交量对日价格变动波动的影响。高因子值可能表明成交量更多地影响价格水平的波动而非日内变动，或者日内变动在成交量加权下相对稳定。这可能用于识别在成交量驱动下价格波动模式的变化，潜在地捕捉趋势的稳定或反转信号。创新点在于结合了成交量对价格水平和价格变化的双重加权，并计算其波动性比率，提供了对市场动能和波动结构的新视角。
    因子应用场景：
    1. 波动性分析：用于识别成交量对价格波动的影响模式。
    2. 趋势识别：捕捉成交量驱动下价格波动模式的变化，潜在地捕捉趋势的稳定或反转信号。
    """
    # 1. 计算 multiply(close, vol)
    data_multiply_close_vol = multiply(data['close'], data['vol'])
    # 2. 计算 ts_std_dev(multiply(close, vol), 10)
    data_ts_std_dev_multiply_close_vol = ts_std_dev(data_multiply_close_vol, 10)
    # 3. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 4. 计算 multiply(ts_delta(close, 1), vol)
    data_multiply_ts_delta_close_vol = multiply(data_ts_delta_close, data['vol'])
    # 5. 计算 ts_std_dev(multiply(ts_delta(close, 1), vol), 10)
    data_ts_std_dev_multiply_ts_delta_close_vol = ts_std_dev(data_multiply_ts_delta_close_vol, 10)
    # 6. 计算 divide(ts_std_dev(multiply(close, vol), 10), ts_std_dev(multiply(ts_delta(close, 1), vol), 10))
    factor = divide(data_ts_std_dev_multiply_close_vol, data_ts_std_dev_multiply_ts_delta_close_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()