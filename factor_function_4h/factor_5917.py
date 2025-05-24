import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import scale, divide, rank, ts_delta, ts_rank

def factor_5917(data, **kwargs):
    """
    因子名称: vwap_delta_rank_ratio_scaled_14757
    数学表达式: scale(divide(rank(ts_delta(vwap, 5)), ts_rank(ts_delta(vwap, 5), 90)), 1)
    中文描述: 该因子首先计算当前VWAP与5天前VWAP的差值，然后计算该差值在截面上的排名。接着，计算该差值在过去90天时间序列上的排名。最后，将截面排名除以时间序列排名，并进行标准化。这个因子旨在捕捉短期VWAP变化在当前市场中的相对位置，并与该变化在历史上的相对位置进行比较。通过结合截面和时间序列排名，可以识别当前价格变化是普遍现象还是相对罕见的事件。标准化处理有助于因子在不同股票和时间点上的可比性。这可能用于识别具有异常短期价格动量的股票。
    因子应用场景：
    1. 短期动量识别：识别具有异常短期价格动量的股票。
    2. 市场普遍性判断：判断当前价格变化是普遍现象还是相对罕见的事件。
    """
    # 1. 计算 ts_delta(vwap, 5)
    data_ts_delta = ts_delta(data['vwap'], d = 5)
    # 2. 计算 rank(ts_delta(vwap, 5))
    data_rank = rank(data_ts_delta)
    # 3. 计算 ts_rank(ts_delta(vwap, 5), 90)
    data_ts_rank = ts_rank(data_ts_delta, d = 90)
    # 4. 计算 divide(rank(ts_delta(vwap, 5)), ts_rank(ts_delta(vwap, 5), 90))
    data_divide = divide(data_rank, data_ts_rank)
    # 5. 计算 scale(divide(rank(ts_delta(vwap, 5)), ts_rank(ts_delta(vwap, 5), 90)), 1)
    factor = scale(data_divide, scale = 1)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()