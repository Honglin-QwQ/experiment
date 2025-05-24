import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_std_dev, multiply, divide

def factor_6035(data, **kwargs):
    """
    因子名称: Volume_Weighted_Volatility_Ratio_92646
    数学表达式: divide(ts_std_dev(multiply(close, vol), 10), ts_std_dev(multiply(close, vol), 30))
    中文描述: 该因子计算了短期（10天）和长期（30天）的成交量加权收盘价标准差的比率。成交量加权收盘价（close * vol）可以更好地反映市场实际交易活动对价格波动的影响。通过比较短期和长期的成交量加权波动率，该因子旨在捕捉市场波动性的变化趋势。当短期波动率相对于长期波动率较高时，可能预示着市场情绪的短期波动加剧或有潜在的趋势变化。该因子创新性在于结合了成交量和价格信息，并利用不同时间窗口的波动率比值来衡量市场动态。
    因子应用场景：
    1. 波动性分析：用于识别市场波动性的变化趋势，短期波动率相对于长期波动率较高时，可能预示着市场情绪的短期波动加剧或有潜在的趋势变化。
    2. 趋势判断：结合成交量和价格信息，衡量市场动态，辅助判断市场趋势。
    """
    # 1. 计算 multiply(close, vol)
    data_multiply = multiply(data['close'], data['vol'])
    # 2. 计算 ts_std_dev(multiply(close, vol), 10)
    data_ts_std_dev_short = ts_std_dev(data_multiply, d = 10)
    # 3. 计算 ts_std_dev(multiply(close, vol), 30)
    data_ts_std_dev_long = ts_std_dev(data_multiply, d = 30)
    # 4. 计算 divide(ts_std_dev(multiply(close, vol), 10), ts_std_dev(multiply(close, vol), 30))
    factor = divide(data_ts_std_dev_short, data_ts_std_dev_long)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()