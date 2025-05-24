import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_decay_linear, ts_delta, rank, ts_mean, ts_arg_max

def factor_5849(data, **kwargs):
    """
    因子名称: VolumePriceChange_DecayCorrelation_58519
    数学表达式: ts_corr(ts_decay_linear(ts_delta(volume, 3), 7), ts_delta(close, 3), 10) - rank(ts_mean(ts_arg_max(close, 30), 15))
    中文描述: 该因子旨在捕捉成交量和价格变化之间的衰减相关性，并结合价格极值位置的长期趋势。第一部分计算过去3天成交量线性衰减变化与过去3天收盘价变化在过去10天的相关性，引入线性衰减来赋予近期成交量变化更高的权重。第二部分计算过去30天收盘价最高点位置在过去15天的平均排名，反映长期价格动量的衰减。最终因子值为两者之差。创新点在于使用了`ts_decay_linear`对成交量变化进行加权，并调整了时间窗口以捕捉不同周期的市场动态，同时结合了更长期的价格极值位置信息。该因子可以用于识别在近期成交量异动后可能出现价格反转的机会，并结合极值位置的排名来衡量这种反转的强度和可持续性，相较于参考因子，通过引入衰减和调整时间窗口，试图提高因子的预测能力和稳定性。
    因子应用场景：
    1. 识别成交量异动后的价格反转机会。
    2. 衡量价格反转的强度和可持续性。
    """
    # 1. 计算 ts_delta(volume, 3)
    data_ts_delta_volume = ts_delta(data['vol'], 3)
    # 2. 计算 ts_decay_linear(ts_delta(volume, 3), 7)
    data_ts_decay_linear = ts_decay_linear(data_ts_delta_volume, 7)
    # 3. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], 3)
    # 4. 计算 ts_corr(ts_decay_linear(ts_delta(volume, 3), 7), ts_delta(close, 3), 10)
    data_ts_corr = ts_corr(data_ts_decay_linear, data_ts_delta_close, 10)
    # 5. 计算 ts_arg_max(close, 30)
    data_ts_arg_max = ts_arg_max(data['close'], 30)
    # 6. 计算 ts_mean(ts_arg_max(close, 30), 15)
    data_ts_mean = ts_mean(data_ts_arg_max, 15)
    # 7. 计算 rank(ts_mean(ts_arg_max(close, 30), 15))
    data_rank = rank(data_ts_mean, 2)
    # 8. 计算 ts_corr(ts_decay_linear(ts_delta(volume, 3), 7), ts_delta(close, 3), 10) - rank(ts_mean(ts_arg_max(close, 30), 15))
    factor = data_ts_corr - data_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()