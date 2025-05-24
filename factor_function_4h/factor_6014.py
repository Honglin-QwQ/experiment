import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract, divide, ts_sum, multiply, sqrt, power, ts_mean, ts_std_dev

def factor_6014(data, **kwargs):
    """
    因子名称: VolWeightedPriceVolatilityDeviation_34247
    数学表达式: subtract(divide(ts_sum(multiply(vol, sqrt(power(subtract(close, ts_mean(close, 5)), 2))), 10), ts_sum(vol, 10)), ts_std_dev(close, 10))
    中文描述: 该因子计算的是过去10天内，基于成交量加权的收盘价与5日均线偏差的平方根的平均值，与过去10天收盘价标准差之间的差值。成交量加权突显了高成交量时的价格波动对因子的影响，而减去标准差则对纯粹的价格波动进行了调整。当因子值为正时，可能表明高成交量时的价格波动相对较大，市场情绪波动剧烈；当因子值为负时，可能表明高成交量时的价格波动相对平缓。这可以用于识别市场情绪的异常波动或衡量价格波动的质量。
    因子应用场景：
    1. 市场情绪识别：正值可能表明高成交量时的价格波动较大，市场情绪波动剧烈。
    2. 价格波动质量评估：衡量价格波动的质量，帮助识别异常波动。
    """
    # 1. 计算 ts_mean(close, 5)
    data_ts_mean_close = ts_mean(data['close'], 5)
    # 2. 计算 subtract(close, ts_mean(close, 5))
    data_subtract_close_ts_mean_close = subtract(data['close'], data_ts_mean_close)
    # 3. 计算 power(subtract(close, ts_mean(close, 5)), 2)
    data_power_subtract_close_ts_mean_close = power(data_subtract_close_ts_mean_close, 2)
    # 4. 计算 sqrt(power(subtract(close, ts_mean(close, 5)), 2))
    data_sqrt_power_subtract_close_ts_mean_close = sqrt(data_power_subtract_close_ts_mean_close)
    # 5. 计算 multiply(vol, sqrt(power(subtract(close, ts_mean(close, 5)), 2)))
    data_multiply_vol_sqrt_power_subtract_close_ts_mean_close = multiply(data['vol'], data_sqrt_power_subtract_close_ts_mean_close)
    # 6. 计算 ts_sum(multiply(vol, sqrt(power(subtract(close, ts_mean(close, 5)), 2))), 10)
    data_ts_sum_multiply_vol_sqrt_power_subtract_close_ts_mean_close = ts_sum(data_multiply_vol_sqrt_power_subtract_close_ts_mean_close, 10)
    # 7. 计算 ts_sum(vol, 10)
    data_ts_sum_vol = ts_sum(data['vol'], 10)
    # 8. 计算 divide(ts_sum(multiply(vol, sqrt(power(subtract(close, ts_mean(close, 5)), 2))), 10), ts_sum(vol, 10))
    data_divide_ts_sum_multiply_vol_sqrt_power_subtract_close_ts_mean_close_ts_sum_vol = divide(data_ts_sum_multiply_vol_sqrt_power_subtract_close_ts_mean_close, data_ts_sum_vol)
    # 9. 计算 ts_std_dev(close, 10)
    data_ts_std_dev_close = ts_std_dev(data['close'], 10)
    # 10. 计算 subtract(divide(ts_sum(multiply(vol, sqrt(power(subtract(close, ts_mean(close, 5)), 2))), 10), ts_sum(vol, 10)), ts_std_dev(close, 10))
    factor = subtract(data_divide_ts_sum_multiply_vol_sqrt_power_subtract_close_ts_mean_close_ts_sum_vol, data_ts_std_dev_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()