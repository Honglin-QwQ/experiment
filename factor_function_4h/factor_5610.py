import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_delta, log, ts_corr, ts_std_dev, sigmoid, multiply, add

def factor_5610(data, **kwargs):
    """
    数学表达式: rank(ts_delta(close,2)) * log(ts_corr(close,high,6)) + ts_std_dev(low,240) * sigmoid(ts_delta(close,2))
    中文描述: 该因子结合了动量、波动率和价格趋势的信号。首先，计算收盘价的短期变化率（ts_delta(close,2)）并进行排名，然后乘以收盘价与最高价的6日相关性的对数，捕捉价格动量和日内价格一致性。接着，将最低价的240日标准差（ts_std_dev(low,240)）乘以收盘价短期变化率的sigmoid函数值，旨在结合长期波动率和短期价格趋势。创新点在于将不同时间尺度和不同类型的价格信息结合，通过乘法和加法运算增强了信号的强度和鲁棒性。
    因子应用场景：
    1. 动量捕捉：捕捉短期价格动量。
    2. 波动率衡量：衡量长期波动率。
    3. 趋势跟踪：跟踪价格趋势。
    """
    # 1. 计算 ts_delta(close, 2)
    ts_delta_close_2 = ts_delta(data['close'], d=2)
    # 2. 计算 rank(ts_delta(close, 2))
    rank_ts_delta_close_2 = rank(ts_delta_close_2)
    # 3. 计算 ts_corr(close, high, 6)
    ts_corr_close_high_6 = ts_corr(data['close'], data['high'], d=6)
    # 4. 计算 log(ts_corr(close, high, 6))
    log_ts_corr_close_high_6 = log(ts_corr_close_high_6)
    # 5. 计算 rank(ts_delta(close,2)) * log(ts_corr(close,high,6))
    multiply_rank_log = multiply(rank_ts_delta_close_2, log_ts_corr_close_high_6)
    # 6. 计算 ts_std_dev(low, 240)
    ts_std_dev_low_240 = ts_std_dev(data['low'], d=240)
    # 7. 计算 sigmoid(ts_delta(close, 2))
    sigmoid_ts_delta_close_2 = sigmoid(ts_delta_close_2)
    # 8. 计算 ts_std_dev(low,240) * sigmoid(ts_delta(close,2))
    multiply_std_sigmoid = multiply(ts_std_dev_low_240, sigmoid_ts_delta_close_2)
    # 9. 计算 rank(ts_delta(close,2)) * log(ts_corr(close,high,6)) + ts_std_dev(low,240) * sigmoid(ts_delta(close,2))
    factor = add(multiply_rank_log, multiply_std_sigmoid)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()