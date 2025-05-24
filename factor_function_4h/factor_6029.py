import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_entropy, adv
import pandas as pd

def factor_6029(data, **kwargs):
    """
    因子名称: Volume_Weighted_Entropy_Ratio_60222
    数学表达式: divide(ts_entropy(vwap, 60), ts_entropy(adv(vol, 60), 60))
    中文描述: 该因子计算过去60天成交量加权平均价格（VWAP）的时间序列熵与过去60天平均成交量（ADV）的时间序列熵的比值。它旨在衡量在考虑成交量信息后，价格波动的不确定性相对于成交量波动不确定性的程度。相较于原始的ts_entropy因子，本因子通过引入成交量信息并计算熵的比值，可能更能捕捉市场在价量关系复杂性下的信息特征。较高的比值可能表明在价格波动中蕴含更多的不确定性信息，而成交量波动相对更可预测，预示着潜在的价格变动或趋势反转。
    因子应用场景：
    1. 市场波动性评估：用于评估市场价格波动相对于成交量波动的不确定性程度。
    2. 趋势反转预测：较高的比值可能预示着潜在的价格变动或趋势反转。
    3. 价量关系分析：捕捉市场在价量关系复杂性下的信息特征。
    """
    # 1. 计算 adv(vol, 60)
    data_adv_vol = adv(data['vol'], d=60)
    # 2. 计算 ts_entropy(adv(vol, 60), 60)
    data_ts_entropy_adv_vol = ts_entropy(data_adv_vol, d=60)
    # 3. 计算 ts_entropy(vwap, 60)
    data_ts_entropy_vwap = ts_entropy(data['vwap'], d=60)
    # 4. 计算 divide(ts_entropy(vwap, 60), ts_entropy(adv(vol, 60), 60))
    factor = divide(data_ts_entropy_vwap, data_ts_entropy_adv_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()