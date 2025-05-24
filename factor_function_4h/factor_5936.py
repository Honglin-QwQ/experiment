import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, multiply, rank

def factor_5936(data, **kwargs):
    """
    因子名称: Volume_Weighted_Volatility_Ratio_Rank_51346
    数学表达式: rank(divide(ts_std_dev(multiply(vwap, vol), 15), ts_std_dev(multiply(vwap, vol), 45)))
    中文描述: 该因子是基于历史输出和改进建议进行创新的因子。它首先计算VWAP与成交量乘积在短期（15天）和长期（45天）内的标准差之比，然后对这个比值进行横截面排名。VWAP与成交量的乘积反映了实际交易活动对价格的影响。计算短期与长期波动率比值旨在捕捉由交易活动驱动的价格波动在不同时间尺度上的相对变化。最后进行排名操作，响应了改进建议中引入非线性操作符以增强区分度的思路。该因子旨在识别那些近期由真实交易驱动的波动强度相对于长期波动强度变化最为显著的股票，可能用于捕捉动量或反转机会。
    因子应用场景：
    1. 动量捕捉：用于识别近期交易活动驱动波动性显著高于长期平均水平的股票，可能预示着短期动量机会。
    2. 反转识别：当因子值较低时，可能表明短期波动性相对于长期较低，可能预示着超卖反弹机会。
    3. 市场情绪分析：通过观察因子在不同股票上的分布，可以了解市场对不同股票交易活动驱动的波动性的看法。
    """
    # 1. 计算 multiply(vwap, vol)
    data_multiply = multiply(data['vwap'], data['vol'])
    # 2. 计算 ts_std_dev(multiply(vwap, vol), 15)
    data_ts_std_dev_short = ts_std_dev(data_multiply, 15)
    # 3. 计算 ts_std_dev(multiply(vwap, vol), 45)
    data_ts_std_dev_long = ts_std_dev(data_multiply, 45)
    # 4. 计算 divide(ts_std_dev(multiply(vwap, vol), 15), ts_std_dev(multiply(vwap, vol), 45))
    data_divide = divide(data_ts_std_dev_short, data_ts_std_dev_long)
    # 5. 计算 rank(divide(ts_std_dev(multiply(vwap, vol), 15), ts_std_dev(multiply(vwap, vol), 45)))
    factor = rank(data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()