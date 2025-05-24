import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_weighted_decay, subtract, ts_corr, rank, ts_std_dev
import pandas as pd

def factor_6075(data, **kwargs):
    """
    因子名称: TS_Weighted_Decay_Corr_Vol_Rank_Std_Diff_64585
    数学表达式: ts_weighted_decay(subtract(ts_corr(high, vol, 15), rank(ts_std_dev(close, 40))), k=0.7)
    中文描述: 该因子首先计算过去15天最高价与成交量的相关性，然后减去过去40天收盘价标准差的横截面排名。最后，对这个差值序列应用一个带有衰减因子k=0.7的加权衰减操作。
    因子应用场景：
    该因子结合了量价关系的长期趋势、价格波动的长期稳定性以及横截面排名信息，并通过减法操作和加权衰减引入了新的计算逻辑。
    相较于参考因子，该因子调整了相关性和标准差的窗口期，并使用加权衰减代替缩放，同时调整了减法操作的位置。
    这可能用于识别那些量价关系呈现特定长期趋势，并且相对于其他股票而言，其长期价格波动性较低的股票，同时通过加权衰减更侧重近期的数据表现。
    """
    # 1. 计算 ts_corr(high, vol, 15)
    data_ts_corr = ts_corr(data['high'], data['vol'], d=15)
    # 2. 计算 ts_std_dev(close, 40)
    data_ts_std_dev = ts_std_dev(data['close'], d=40)
    # 3. 计算 rank(ts_std_dev(close, 40))
    data_rank = rank(data_ts_std_dev)
    # 4. 计算 subtract(ts_corr(high, vol, 15), rank(ts_std_dev(close, 40)))
    data_subtract = subtract(data_ts_corr, data_rank)
    # 5. 计算 ts_weighted_decay(subtract(ts_corr(high, vol, 15), rank(ts_std_dev(close, 40))), k=0.7)
    factor = ts_weighted_decay(data_subtract, k=0.7)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()