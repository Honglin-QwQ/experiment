import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_arg_max, ts_decay_linear, ts_std_dev, ts_delta, multiply, divide, add

def factor_5739(data, **kwargs):
    """
    因子名称: VWAP_Volatility_ArgMax_Scaled_Momentum_87537
    数学表达式: multiply(divide(ts_arg_max(vwap, 30), 30), add(ts_decay_linear(ts_std_dev(vwap, 10), 15), 1e-6), ts_delta(vwap, 7))
    中文描述: 该因子旨在捕捉VWAP的长期趋势峰值位置、短期波动性和中期动量的结合效应。它首先计算过去30天VWAP最大值出现的相对天数，并将其标准化到0到1之间（除以30）。然后计算过去10天VWAP标准差的15天线性衰减值，并在分母中加入一个小的常数1e-6以避免除以零。最后，将标准化后的最大值位置与衰减波动率的倒数以及过去7天VWAP的差值（代表中期动量）相乘。因子的创新点在于：1. 对ts_arg_max的结果进行了标准化，使其更具可比性；2. 对ts_std_dev进行了线性衰减处理，赋予近期波动率更高的权重；3. 引入了中期VWAP动量，捕捉价格趋势的持续性。该因子可能用于识别在价格达到近期高点后，结合波动率和动量判断趋势是否持续或反转的信号。
    因子应用场景：
    1. 趋势识别：识别价格达到近期高点后，结合波动率和动量判断趋势是否持续或反转的信号。
    2. 波动率分析：通过线性衰减的标准差，关注近期波动率对因子值的影响。
    3. 动量分析：结合中期动量，判断价格趋势的持续性。
    """
    # 1. 计算 ts_arg_max(vwap, 30)
    data_ts_arg_max = ts_arg_max(data['vwap'], d = 30)
    # 2. 计算 divide(ts_arg_max(vwap, 30), 30)
    data_divide = divide(data_ts_arg_max, 30)
    # 3. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev = ts_std_dev(data['vwap'], d = 10)
    # 4. 计算 ts_decay_linear(ts_std_dev(vwap, 10), 15)
    data_ts_decay_linear = ts_decay_linear(data_ts_std_dev, d = 15)
    # 5. 计算 add(ts_decay_linear(ts_std_dev(vwap, 10), 15), 1e-6)
    data_add = add(data_ts_decay_linear, 1e-6)
    # 6. 计算 ts_delta(vwap, 7)
    data_ts_delta = ts_delta(data['vwap'], d = 7)
    # 7. 计算 multiply(divide(ts_arg_max(vwap, 30), 30), add(ts_decay_linear(ts_std_dev(vwap, 10), 15), 1e-6), ts_delta(vwap, 7))
    factor = multiply(data_divide, data_add, data_ts_delta)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()