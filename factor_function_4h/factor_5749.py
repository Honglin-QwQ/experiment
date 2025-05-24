import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5749(data, **kwargs):
    """
    因子名称: VolumeVolatilityRankRatio_96484
    数学表达式: divide(rank(ts_std_dev(volume, 10)), ts_rank(ts_decay_linear(adv(volume, 20), 10), 5))
    中文描述: 该因子计算了成交量短期波动率的排名与长期平均成交量线性衰减值的时序排名的比率。具体来说，它首先计算过去10天成交量的标准差并进行横截面排名，反映短期成交量波动的相对强度。
             然后，计算过去20天平均成交量在过去10天的线性衰减值，并对其在过去5天进行时序排名，反映长期成交量趋势的动态变化。最后，将短期波动率排名除以长期趋势时序排名。
             高因子值可能表示短期成交量波动剧烈，而长期趋势相对平稳，这可能预示着市场情绪的短期爆发或潜在的交易机会。
             该因子的创新点在于结合了成交量的短期波动特征和长期趋势特征，并通过排名和时序排名进行标准化和比较，提供了一个多维度的成交量分析视角。
    因子应用场景：
    1. 短期波动与长期趋势分析：用于识别短期成交量波动较大，但长期趋势相对平稳的股票，可能预示着潜在的交易机会。
    2. 市场情绪识别：辅助判断市场短期情绪的爆发，尤其是在长期趋势稳定的情况下，成交量短期波动可能反映了市场参与者的情绪变化。
    """
    # 1. 计算 ts_std_dev(volume, 10)
    data_ts_std_dev = ts_std_dev(data['vol'], 10)
    # 2. 计算 rank(ts_std_dev(volume, 10))
    data_rank = rank(data_ts_std_dev)
    # 3. 计算 adv(volume, 20)
    data_adv = adv(data['vol'], 20)
    # 4. 计算 ts_decay_linear(adv(volume, 20), 10)
    data_ts_decay_linear = ts_decay_linear(data_adv, 10)
    # 5. 计算 ts_rank(ts_decay_linear(adv(volume, 20), 10), 5)
    data_ts_rank = ts_rank(data_ts_decay_linear, 5)
    # 6. 计算 divide(rank(ts_std_dev(volume, 10)), ts_rank(ts_decay_linear(adv(volume, 20), 10), 5))
    factor = divide(data_rank, data_ts_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()