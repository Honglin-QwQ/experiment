import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5978(data, **kwargs):
    """
    因子名称: VolumePriceChangeRatio_Improved_51181
    数学表达式: divide(ts_delta(divide(ts_sum(multiply(vol, divide(add(close, high, low), 3)), 5), ts_sum(vol, 5)), 3), multiply(ts_mean(divide(ts_sum(multiply(vol, divide(add(close, high, low), 3)), 5), ts_sum(vol, 5)), 15), ts_std_dev(vol, 15)))
    中文描述: 该因子是基于VolumePriceChangeRatio因子的改进版本，旨在提高其预测能力和稳定性。它首先计算5日VWAP（成交量加权平均价），然后计算该5日VWAP在过去3天内的变化量。这个变化量作为分子。分母则使用过去15天内5日VWAP的平均值乘以过去15天内成交量的标准差。通过引入VWAP，更能反映实际交易价格；计算VWAP的相对变化，增强了对价格趋势的敏感性；分母中引入成交量标准差，在高波动市场中具有一定的风险控制作用。创新点在于结合VWAP、相对变化和成交量波动，构建了一个更全面的量价关系指标。高值可能表明近期成交量驱动的价格变化异常强劲且相对稳定，预示着更可靠的趋势信号。
    因子应用场景：
    1. 趋势识别：当因子值较高时，表明近期成交量驱动的价格变化异常强劲且相对稳定，预示着更可靠的趋势信号。
    2. 风险控制：分母中引入成交量标准差，在高波动市场中具有一定的风险控制作用。
    """
    # 1. 计算 add(close, high, low)
    data_add = add(data['close'], data['high'], data['low'])
    # 2. 计算 divide(add(close, high, low), 3)
    data_divide_1 = divide(data_add, 3)
    # 3. 计算 multiply(vol, divide(add(close, high, low), 3))
    data_multiply = multiply(data['vol'], data_divide_1)
    # 4. 计算 ts_sum(multiply(vol, divide(add(close, high, low), 3)), 5)
    data_ts_sum_1 = ts_sum(data_multiply, 5)
    # 5. 计算 ts_sum(vol, 5)
    data_ts_sum_2 = ts_sum(data['vol'], 5)
    # 6. 计算 divide(ts_sum(multiply(vol, divide(add(close, high, low), 3)), 5), ts_sum(vol, 5))
    data_divide_2 = divide(data_ts_sum_1, data_ts_sum_2)
    # 7. 计算 ts_delta(divide(ts_sum(multiply(vol, divide(add(close, high, low), 3)), 5), ts_sum(vol, 5)), 3)
    data_ts_delta = ts_delta(data_divide_2, 3)
    # 8. 计算 ts_mean(divide(ts_sum(multiply(vol, divide(add(close, high, low), 3)), 5), ts_sum(vol, 5)), 15)
    data_ts_mean = ts_mean(data_divide_2, 15)
    # 9. 计算 ts_std_dev(vol, 15)
    data_ts_std_dev = ts_std_dev(data['vol'], 15)
    # 10. 计算 multiply(ts_mean(divide(ts_sum(multiply(vol, divide(add(close, high, low), 3)), 5), ts_sum(vol, 5)), 15), ts_std_dev(vol, 15))
    data_multiply_2 = multiply(data_ts_mean, data_ts_std_dev)
    # 11. 计算 divide(ts_delta(divide(ts_sum(multiply(vol, divide(add(close, high, low), 3)), 5), ts_sum(vol, 5)), 3), multiply(ts_mean(divide(ts_sum(multiply(vol, divide(add(close, high, low), 3)), 5), ts_sum(vol, 5)), 15), ts_std_dev(vol, 15)))
    factor = divide(data_ts_delta, data_multiply_2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()