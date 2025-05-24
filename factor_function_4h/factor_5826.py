import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import scale, subtract, ts_rank, winsorize, ts_std_dev
import pandas as pd

def factor_5826(data, **kwargs):
    """
    因子名称: Volatility_Weighted_Volume_Rank_Ratio_Improved_35535
    数学表达式: scale(subtract(ts_rank(winsorize(vol, 0.05), 15), ts_std_dev(close, 15)))
    中文描述: 该因子是基于对原有因子Volatility_Weighted_Volume_Rank_Ratio的改进。原始因子计算过去10天成交量的时间序列排名与过去10天收盘价标准差的比值，并表现出微弱的负向预测能力。改进后的因子首先对成交量进行缩尾处理（winsorize），以减少极端值的影响，然后在更长的15天时间窗口内计算缩尾后成交量的时间序列排名和收盘价的标准差。最后，计算这两个指标的差值，并进行标准化（scale）。通过计算差值而非比值，并进行标准化，旨在更直接地衡量成交量相对活跃度与价格波动性的关系，并消除量纲影响，使其更适合与其他因子组合。时间窗口的调整和缩尾处理旨在提高因子的稳健性和预测能力。标准化后的因子值与预测收益率可能呈现正相关关系，因子值越高可能预示着未来收益率越高。
    因子应用场景：
    1. 衡量成交量相对活跃度与价格波动性的关系。
    2. 提高因子的稳健性和预测能力。
    """
    # 1. 对成交量进行缩尾处理（winsorize）
    data_winsorize_vol = winsorize(data['vol'], std = 0.05)
    # 2. 计算缩尾后成交量的时间序列排名
    data_ts_rank = ts_rank(data_winsorize_vol, d = 15)
    # 3. 计算收盘价的标准差
    data_ts_std_dev = ts_std_dev(data['close'], d = 15)
    # 4. 计算两个指标的差值
    data_subtract = subtract(data_ts_rank, data_ts_std_dev)
    # 5. 进行标准化（scale）
    factor = scale(data_subtract)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()