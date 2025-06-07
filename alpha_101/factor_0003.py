import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_rank, multiply

def factor_0003(data, **kwargs):
    """
    数学表达式: (-1 * ts_rank(rank(low), 9))
    中文描述: 这个因子首先计算股票每天的最低价在所有股票中的排名百分比，然后计算这个排名百分比在过去9天内的排名，最后取负数，数值越大，说明过去9天最低价排名越靠后，即相对强度越弱，可能预示着下跌趋势，反之亦然。
    应用场景：
    1. 动量策略：结合其他动量因子，寻找短期内下跌趋势明显的股票。
    2. 逆向投资：寻找因子值较低，即过去一段时间内相对强度较强的股票，进行逆向投资。
    3. 风险控制：在量化模型中作为风险因子，规避做多近期相对强度较弱的股票。
    """
    # 1. 计算 rank(low)
    data_rank_low = rank(data['low'], rate = 2)
    # 2. 计算 ts_rank(rank(low), 9)
    data_ts_rank = ts_rank(data_rank_low, d = 9, constant = 0)
    # 3. 计算 -1 * ts_rank(rank(low), 9)
    factor = multiply(-1, data_ts_rank, filter=False)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()