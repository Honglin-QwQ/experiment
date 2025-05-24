import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, log, ts_delta, ts_arg_max, multiply

def factor_5858(data, **kwargs):
    """
    因子名称: Volatility_Momentum_Divergence_12072
    数学表达式: multiply(ts_std_dev(log(close), 10), ts_delta(ts_arg_max(low, 30), 5))
    中文描述: 该因子结合了短期价格波动率和长期最低价位置变化。首先，计算过去10天收盘价对数收益率的标准差，衡量短期波动性。然后，计算过去30天最低价出现最大值的相对位置，并计算该位置在过去5天内的变化。最后，将短期波动率与长期最低价最大值位置的变化相乘。其创新点在于结合了不同时间尺度的价格信息，并使用了对数收益率的标准差和最大值位置的相对变化，试图捕捉波动率与长期支撑位变化之间的潜在背离或共振，可能用于识别市场情绪的转变或趋势的潜在反转。
    因子应用场景：
    1. 识别市场情绪的转变或趋势的潜在反转。
    2. 结合不同时间尺度的价格信息，捕捉波动率与长期支撑位变化之间的潜在背离或共振。
    """
    # 1. 计算 log(close)
    data_log_close = log(data['close'])
    # 2. 计算 ts_std_dev(log(close), 10)
    data_ts_std_dev = ts_std_dev(data_log_close, d = 10)
    # 3. 计算 ts_arg_max(low, 30)
    data_ts_arg_max = ts_arg_max(data['low'], d = 30)
    # 4. 计算 ts_delta(ts_arg_max(low, 30), 5)
    data_ts_delta = ts_delta(data_ts_arg_max, d = 5)
    # 5. 计算 multiply(ts_std_dev(log(close), 10), ts_delta(ts_arg_max(low, 30), 5))
    factor = multiply(data_ts_std_dev, data_ts_delta)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()