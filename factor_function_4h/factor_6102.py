import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, ts_std_dev, log, divide

def factor_6102(data, **kwargs):
    """
    因子名称: PriceVolumeVolatilityDecayRatio_Enhanced_22466
    数学表达式: divide(ts_decay_linear(ts_std_dev(log(close), 10), 30), ts_decay_linear(ts_std_dev(log(vol), 30), 60))
    中文描述: 该因子是DecayedVolatilityVolumeRatio_v2因子的改进版本。它计算过去10天收盘价对数收益率标准差的30天线性衰减平均值与过去30天成交量对数标准差的60天线性衰减平均值之比。相较于原始因子，该因子通过增加ts_std_dev和ts_decay_linear的窗口期，旨在捕捉更长周期的价格和成交量波动性信息，并使用更长的衰减窗口平滑短期波动。这可能有助于提高因子的稳定性和预测能力。较高的值可能表明价格波动在相对较低的成交量波动下发生，这可能预示着趋势的脆弱性或潜在的反转。
    因子应用场景：
    1. 趋势识别：用于识别价格波动性相对于成交量波动性的变化，辅助判断趋势的强弱。
    2. 反转信号：当价格波动性远高于成交量波动性时，可能预示着潜在的反转。
    """
    # 1. 计算 log(close)
    data_log_close = log(data['close'])
    # 2. 计算 ts_std_dev(log(close), 10)
    data_ts_std_dev_log_close = ts_std_dev(data_log_close, d=10)
    # 3. 计算 ts_decay_linear(ts_std_dev(log(close), 10), 30)
    data_ts_decay_linear_price = ts_decay_linear(data_ts_std_dev_log_close, d=30)
    # 4. 计算 log(vol)
    data_log_vol = log(data['vol'])
    # 5. 计算 ts_std_dev(log(vol), 30)
    data_ts_std_dev_log_vol = ts_std_dev(data_log_vol, d=30)
    # 6. 计算 ts_decay_linear(ts_std_dev(log(vol), 30), 60)
    data_ts_decay_linear_volume = ts_decay_linear(data_ts_std_dev_log_vol, d=60)
    # 7. 计算 divide(ts_decay_linear(ts_std_dev(log(close), 10), 30), ts_decay_linear(ts_std_dev(log(vol), 30), 60))
    factor = divide(data_ts_decay_linear_price, data_ts_decay_linear_volume)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()