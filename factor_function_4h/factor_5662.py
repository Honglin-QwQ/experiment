import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, multiply, ts_delta, ts_arg_max, log, divide, ts_delay

def factor_5662(data, **kwargs):
    """
    因子名称: factor_0003_60510
    数学表达式: ts_zscore(multiply(ts_delta(ts_arg_max(vwap, 10), 2), log(divide(high, ts_delay(low, 5)))), 20)
    中文描述: 本因子结合了VWAP最大值位置变化、最高价与过去最低价的比率以及时间序列Z-score，旨在捕捉价格动量和潜在的趋势反转信号。
    首先，计算过去10天VWAP最大值位置的2日变化量，并将其与最高价和5日前最低价之比的对数相乘，以此来衡量价格的相对强度。
    然后，对该乘积计算20日Z-score，以标准化该指标并识别其相对于历史均值的偏离程度。
    该因子的创新点在于结合了价格动量、相对价格强度和统计标准化，可以用于识别超买或超卖的情况，并预测短期价格趋势。
    因子应用场景：
    1. 识别超买超卖情况：当因子值远高于或低于0时，可能表明股票处于超买或超卖状态。
    2. 预测短期价格趋势：结合其他技术指标，可以辅助判断短期价格趋势的反转点。
    """
    # 1. 计算 ts_arg_max(vwap, 10)
    data_ts_arg_max_vwap = ts_arg_max(data['vwap'], d = 10)
    # 2. 计算 ts_delta(ts_arg_max(vwap, 10), 2)
    data_ts_delta = ts_delta(data_ts_arg_max_vwap, d = 2)
    # 3. 计算 ts_delay(low, 5)
    data_ts_delay_low = ts_delay(data['low'], d = 5)
    # 4. 计算 divide(high, ts_delay(low, 5))
    data_divide = divide(data['high'], data_ts_delay_low)
    # 5. 计算 log(divide(high, ts_delay(low, 5)))
    data_log = log(data_divide)
    # 6. 计算 multiply(ts_delta(ts_arg_max(vwap, 10), 2), log(divide(high, ts_delay(low, 5))))
    data_multiply = multiply(data_ts_delta, data_log)
    # 7. 计算 ts_zscore(multiply(ts_delta(ts_arg_max(vwap, 10), 2), log(divide(high, ts_delay(low, 5)))), 20)
    factor = ts_zscore(data_multiply, d = 20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()