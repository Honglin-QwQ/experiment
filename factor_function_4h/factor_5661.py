import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_scale, ts_covariance, ts_rank

def factor_5661(data, **kwargs):
    """
    因子名称: factor_0001_51540
    数学表达式: ts_scale(ts_covariance(close, ts_rank(vol, d=10), d=5), d=20, constant=-1)
    中文描述: 该因子计算收盘价与成交量排名的协方差，并对其进行时间序列缩放。首先，计算过去10天成交量的排名，然后计算收盘价与成交量排名在过去5天内的协方差，最后将该协方差在过去20天内进行时间序列缩放，并减去1作为常数调整。该因子旨在捕捉价格与成交量变化之间的关系，并进行标准化处理，可能用于识别价格趋势的可持续性。
    因子应用场景：
    1. 趋势识别：捕捉价格与成交量变化之间的关系，标准化处理可能用于识别价格趋势的可持续性。
    2. 量价关系分析：分析成交量排名与收盘价之间的协方差，可能揭示市场参与者对价格趋势的认可程度。
    """
    # 1. 计算 ts_rank(vol, d=10)
    data_ts_rank_vol = ts_rank(data['vol'], d=10)
    # 2. 计算 ts_covariance(close, ts_rank(vol, d=10), d=5)
    data_ts_covariance = ts_covariance(data['close'], data_ts_rank_vol, d=5)
    # 3. 计算 ts_scale(ts_covariance(close, ts_rank(vol, d=10), d=5), d=20, constant=-1)
    factor = ts_scale(data_ts_covariance, d=20, constant=-1)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()