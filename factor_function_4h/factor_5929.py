import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, ts_std_dev, multiply, ts_mean, abs, subtract, ts_delay, divide

def factor_5929(data, **kwargs):
    """
    因子名称: Volume_Price_Volatility_Decay_Ratio_95509
    数学表达式: divide(ts_decay_exp_window(ts_std_dev(multiply(close, vol), 10), 0.7), ts_mean(abs(subtract(close, ts_delay(close, 5))), 20))
    中文描述: 该因子旨在捕捉成交量加权价格波动性的短期指数衰减与长期价格变动绝对值均值之间的比率。首先，计算收盘价与成交量乘积（代表交易活跃度）在过去10天内的标准差，并应用0.7的指数衰减权重，以更强调近期波动。然后，计算收盘价与其5天前收盘价差值的绝对值在过去20天内的均值，反映长期价格波动的平均水平。最后，将短期衰减波动性除以长期平均波动性。创新的地方在于结合了成交量和价格的乘积来衡量活跃度波动，并使用了指数衰减来突出近期效应，同时与长期价格变动均值进行对比，试图识别短期波动相对于长期趋势的强度，可能用于捕捉价格趋势的加速或减缓信号。
    因子应用场景：
    1. 短期波动性分析：用于衡量短期成交量加权价格波动性相对于长期价格变动均值的强度。
    2. 趋势识别：可能用于捕捉价格趋势的加速或减缓信号。
    """
    # 1. 计算 multiply(close, vol)
    data_multiply = multiply(data['close'], data['vol'])
    # 2. 计算 ts_std_dev(multiply(close, vol), 10)
    data_ts_std_dev = ts_std_dev(data_multiply, 10)
    # 3. 计算 ts_decay_exp_window(ts_std_dev(multiply(close, vol), 10), 0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_std_dev, d = 6, factor = 0.7)
    # 4. 计算 ts_delay(close, 5)
    data_ts_delay = ts_delay(data['close'], d = 5)
    # 5. 计算 subtract(close, ts_delay(close, 5))
    data_subtract = subtract(data['close'], data_ts_delay)
    # 6. 计算 abs(subtract(close, ts_delay(close, 5)))
    data_abs = abs(data_subtract)
    # 7. 计算 ts_mean(abs(subtract(close, ts_delay(close, 5))), 20)
    data_ts_mean = ts_mean(data_abs, d = 20)
    # 8. 计算 divide(ts_decay_exp_window(ts_std_dev(multiply(close, vol), 10), 0.7), ts_mean(abs(subtract(close, ts_delay(close, 5))), 20))
    factor = divide(data_ts_decay_exp_window, data_ts_mean)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()