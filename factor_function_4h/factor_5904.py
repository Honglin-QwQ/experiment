import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5904(data, **kwargs):
    """
    因子名称: Volatility_Adjusted_Volume_Rank_Ratio_79845
    数学表达式: divide(ts_rank(adv(vol, 20), 26), ts_std_dev(ts_delta(open, 3), 66))
    中文描述: 该因子结合了成交量的相对强度和开盘价的波动性。它首先计算过去20天平均成交量在过去26天内的排名，然后将这个排名除以过去66天内3天开盘价变化的标准差。高排名表示当前成交量相对活跃，低波动性表示价格变动相对平稳。因此，该因子旨在捕捉在相对活跃的交易量背景下，价格波动较小的股票，可能指示着更稳定的趋势或机构资金的温和流入。创新点在于将成交量排名与开盘价波动性标准差进行比率计算，创造了一个新的综合衡量指标，结合了市场活跃度和价格稳定性两个维度。
    因子应用场景：
    1. 识别稳定趋势：用于识别在成交量相对活跃的情况下，价格波动较小的股票，可能预示着更稳定的上涨趋势。
    2. 机构资金流入：该因子可能捕捉到机构资金在成交量活跃但价格波动不大的股票中温和流入的情况。
    """
    # 1. 计算 adv(vol, 20)
    data_adv_vol = adv(data['vol'], d = 20)
    # 2. 计算 ts_rank(adv(vol, 20), 26)
    data_ts_rank = ts_rank(data_adv_vol, d = 26)
    # 3. 计算 ts_delta(open, 3)
    data_ts_delta_open = ts_delta(data['open'], d = 3)
    # 4. 计算 ts_std_dev(ts_delta(open, 3), 66)
    data_ts_std_dev = ts_std_dev(data_ts_delta_open, d = 66)
    # 5. 计算 divide(ts_rank(adv(vol, 20), 26), ts_std_dev(ts_delta(open, 3), 66))
    factor = divide(data_ts_rank, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()