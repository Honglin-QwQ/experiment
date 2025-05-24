import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import if_else, ts_delta, ts_rank, divide, multiply

def factor_5592(data, **kwargs):
    """
    数学表达式: if_else(ts_delta(close, 7) > 0, close * ts_rank(vol, 7), close / ts_rank(vol, 7))
    中文描述: 该因子基于收盘价的变化趋势和成交量的排名来判断股票的买卖时机。如果过去7天收盘价是上涨的，则使用收盘价乘以成交量排名的值；如果过去7天收盘价是下跌的，则使用收盘价除以成交量排名的值。该因子融合了价格动量和成交量信息，旨在捕捉价格上涨时成交量放大，价格下跌时成交量萎缩的市场特征，从而辅助投资者决策。
    因子应用场景：
    1. 买卖时机判断：当因子值为正时，可能表示股票处于上涨趋势，是买入时机；当因子值为负时，可能表示股票处于下跌趋势，是卖出时机。
    2. 趋势判断：因子值的大小可以反映股票价格趋势的强弱。
    """
    # 1. 计算 ts_delta(close, 7)
    data_ts_delta = ts_delta(data['close'], 7)
    # 2. 计算 ts_rank(vol, 7)
    data_ts_rank = ts_rank(data['vol'], 7)
    # 3. 计算 close * ts_rank(vol, 7)
    data_multiply = multiply(data['close'], data_ts_rank)
    # 4. 计算 close / ts_rank(vol, 7)
    data_divide = divide(data['close'], data_ts_rank)
    # 5. 计算 if_else(ts_delta(close, 7) > 0, close * ts_rank(vol, 7), close / ts_rank(vol, 7))
    factor = if_else(data_ts_delta > 0, data_multiply, data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()