import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract, multiply, ts_rank, ts_decay_linear, ts_std_dev, rank, ts_skewness, log, adv
import pandas as pd

def factor_5823(data, **kwargs):
    """
    因子名称: VolumeVolatilityDecayRankSkew_78584
    数学表达式: subtract(multiply(ts_rank(ts_decay_linear(ts_std_dev(vol, 20), 10), 5), rank(ts_skewness(vol, 10))), log(adv(vol, 30)))
    中文描述: 该因子旨在捕捉成交量的波动性趋势、偏度以及长期平均成交量。它计算了过去20天成交量标准差的10天线性衰减值的5日时间序列排名，并乘以过去10天成交量偏度的全市场排名。最后，减去30日平均成交量的自然对数。高因子值可能表明股票近期成交量波动性呈现线性衰减趋势且排名较高，同时成交量分布向正偏（即有较多小幅上涨伴随少量大幅下跌），且长期平均成交量适中。这可能预示着市场情绪的变化和潜在的交易机会。相较于参考因子，本因子将成交量峰度替换为标准差和偏度，并调整了时间窗口和平均成交量周期，结合了波动性和分布特征，旨在捕捉更全面的成交量信息。同时，采用了建议中提到的log操作符，并调整了时间窗口以增强因子稳定性。
    因子应用场景：
    1. 市场情绪分析：可用于识别成交量波动性衰减但偏度较高的股票，可能表明市场情绪正在发生变化。
    2. 交易机会发现：结合长期平均成交量，有助于发现潜在的交易机会。
    """
    # 1. 计算 ts_std_dev(vol, 20)
    data_ts_std_dev = ts_std_dev(data['vol'], 20)
    # 2. 计算 ts_decay_linear(ts_std_dev(vol, 20), 10)
    data_ts_decay_linear = ts_decay_linear(data_ts_std_dev, 10)
    # 3. 计算 ts_rank(ts_decay_linear(ts_std_dev(vol, 20), 10), 5)
    data_ts_rank = ts_rank(data_ts_decay_linear, 5)
    # 4. 计算 ts_skewness(vol, 10)
    data_ts_skewness = ts_skewness(data['vol'], 10)
    # 5. 计算 rank(ts_skewness(vol, 10))
    data_rank = rank(data_ts_skewness, 2)
    # 6. 计算 multiply(ts_rank(ts_decay_linear(ts_std_dev(vol, 20), 10), 5), rank(ts_skewness(vol, 10)))
    data_multiply = multiply(data_ts_rank, data_rank)
    # 7. 计算 adv(vol, 30)
    data_adv = adv(data['vol'], 30)
    # 8. 计算 log(adv(vol, 30))
    data_log = log(data_adv)
    # 9. 计算 subtract(multiply(ts_rank(ts_decay_linear(ts_std_dev(vol, 20), 10), 5), rank(ts_skewness(vol, 10))), log(adv(vol, 30)))
    factor = subtract(data_multiply, data_log)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()