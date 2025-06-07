import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract, multiply, divide, ts_decay_linear, rank, ts_arg_max

def factor_0056(data, **kwargs):
    """
    数学表达式: (0 - (1 * ((close - vwap) / ts_decay_linear(rank(ts_arg_max(close, 30)), 2)))) 
    中文描述: 该因子计算的是负的成交量加权平均价(vwap)偏离收盘价程度的线性衰减排名，数值越大，说明收盘价相对于成交量加权平均价的偏离程度在过去一段时间内排名越靠后，可能预示着价格反转；应用场景包括：1. 短期反转策略：寻找因子值较高的股票，预期价格将回调至成交量加权平均价附近；2. 趋势跟踪策略：结合其他趋势指标，过滤掉短期价格偏离较大的股票；3. 量价关系分析：用于识别量价背离的股票，辅助判断趋势的可靠性。
    """
    # 1. 计算 (close - vwap)
    close_minus_vwap = subtract(data['close'], data['vwap'])
    # 2. 计算 ts_arg_max(close, 30)
    ts_arg_max_close = ts_arg_max(data['close'], 30)
    # 3. 计算 rank(ts_arg_max(close, 30))
    rank_ts_arg_max_close = rank(ts_arg_max_close)
    # 4. 计算 ts_decay_linear(rank(ts_arg_max(close, 30)), 2)
    ts_decay_linear_rank_ts_arg_max_close = ts_decay_linear(rank_ts_arg_max_close, 2)
    # 5. 计算 (close - vwap) / ts_decay_linear(rank(ts_arg_max(close, 30)), 2)
    division_result = divide(close_minus_vwap, ts_decay_linear_rank_ts_arg_max_close)
    # 6. 计算 1 * ((close - vwap) / ts_decay_linear(rank(ts_arg_max(close, 30)), 2))
    multiplication_result = multiply(1, division_result)
    # 7. 计算 0 - (1 * ((close - vwap) / ts_decay_linear(rank(ts_arg_max(close, 30)), 2)))
    factor = subtract(0, multiplication_result)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()