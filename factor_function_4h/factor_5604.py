import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, multiply, ts_mean, divide, ts_delay, ts_median

def factor_5604(data, **kwargs):
    """
    因子名称: factor_0002_16049
    数学表达式: ts_delta(multiply(ts_mean(divide(vol, ts_delay(vol, 5)), 20), ts_median(ts_mean(divide(vol, ts_delay(vol, 5)), 20), 20)), 5)
    中文描述: 该因子是对历史因子factor_0001的改进，旨在更精确地捕捉成交量变化对价格趋势的影响。它首先计算过去20天内每日成交量与5日前成交量的比值的平均值，然后计算这些平均值的20日中位数，旨在衡量成交量变化的稳定性和活跃度。最后，计算该乘积的5日差分，以衡量成交量变化速率的短期变化。相较于直接使用adv20，该因子使用成交量比率的均值，能更好地反映成交量变化的相对强度，并减少了绝对成交量大小的影响。创新点在于使用成交量比率均值和中位数的乘积，结合了成交量变化的速度和稳定性，从而更全面地评估市场情绪和交易活动。
    """
    # 1. 计算 ts_delay(vol, 5)
    data_ts_delay_vol = ts_delay(data['vol'], 5)
    # 2. 计算 divide(vol, ts_delay(vol, 5))
    data_divide = divide(data['vol'], data_ts_delay_vol)
    # 3. 计算 ts_mean(divide(vol, ts_delay(vol, 5)), 20)
    data_ts_mean = ts_mean(data_divide, 20)
    # 4. 计算 ts_median(ts_mean(divide(vol, ts_delay(vol, 5)), 20), 20)
    data_ts_median = ts_median(data_ts_mean, 20)
    # 5. 计算 multiply(ts_mean(divide(vol, ts_delay(vol, 5)), 20), ts_median(ts_mean(divide(vol, ts_delay(vol, 5)), 20), 20))
    data_multiply = multiply(data_ts_mean, data_ts_median)
    # 6. 计算 ts_delta(multiply(ts_mean(divide(vol, ts_delay(vol, 5)), 20), ts_median(ts_mean(divide(vol, ts_delay(vol, 5)), 20), 20)), 5)
    factor = ts_delta(data_multiply, 5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()