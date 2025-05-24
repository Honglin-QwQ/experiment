import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_delta, divide, ts_std_dev, ts_max_diff

def factor_5715(data, **kwargs):
    """
    数学表达式: divide(ts_rank(ts_delta(close, 5), 10), ts_std_dev(ts_max_diff(open, 104), 20))
    中文描述: 该因子旨在捕捉价格动量与基于开盘价历史偏离的波动率之间的关系。它计算了过去5天收盘价变化的10日时间序列排名，并将其除以过去20天内开盘价最大差（ts_max_diff(open, 104)）的标准差。
    因子应用场景：
    该因子可能用于识别那些在短期内表现出强劲价格上涨动量，且这种动量相对于开盘价历史偏离所体现的波动性较低的股票。高因子值可能预示着更可持续的上涨趋势，可用于动量策略。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 2. 计算 ts_rank(ts_delta(close, 5), 10)
    data_ts_rank = ts_rank(data_ts_delta_close, 10)
    # 3. 计算 ts_max_diff(open, 104)
    data_ts_max_diff = ts_max_diff(data['open'], 104)
    # 4. 计算 ts_std_dev(ts_max_diff(open, 104), 20)
    data_ts_std_dev = ts_std_dev(data_ts_max_diff, 20)
    # 5. 计算 divide(ts_rank(ts_delta(close, 5), 10), ts_std_dev(ts_max_diff(open, 104), 20))
    factor = divide(data_ts_rank, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()