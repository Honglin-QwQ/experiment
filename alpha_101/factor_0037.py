import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_rank, multiply

def factor_0037(data, **kwargs):
    """
    数学表达式: (-1 * rank(ts_rank(close, 10))) * rank((close / open))
    中文描述: 该因子首先计算过去10天收盘价的时间序列排名，然后对排名取负数，再计算每日收盘价与开盘价的比率，并对该比率进行排名，最后将这两个排名相乘。该因子旨在捕捉短期价格动量和日内价格变化之间的关系，负的时间序列排名意味着价格在过去10天表现越差，该部分值越大，而收盘价与开盘价的比率排名越高，意味着当日价格上涨幅度越大，该部分值越大，因此，该因子可能反映了短期下跌后当日反弹的股票。
    因子应用场景包括：
    1. 寻找超跌反弹机会：选取因子值较高的股票，可能预示着短期内有反弹潜力。
    2. 构建动量反转策略：结合其他动量指标，该因子可以作为反转策略的一部分，捕捉市场情绪变化。
    3. 量化选股：将该因子与其他基本面或技术指标结合，构建多因子选股模型，提高选股效果。
    """
    # 1. 计算 ts_rank(close, 10)
    ts_rank_close_10 = ts_rank(data['close'], d = 10)
    # 2. 计算 rank(ts_rank(close, 10))
    rank_ts_rank_close_10 = rank(ts_rank_close_10, rate = 2)
    # 3. 计算 -1 * rank(ts_rank(close, 10))
    negative_rank_ts_rank_close_10 = -1 * rank_ts_rank_close_10
    # 4. 计算 close / open
    close_over_open = data['close'] / data['open']
    # 5. 计算 rank(close / open)
    rank_close_over_open = rank(close_over_open, rate = 2)
    # 6. 计算 (-1 * rank(ts_rank(close, 10))) * rank((close / open))
    factor = multiply(negative_rank_ts_rank_close_10, rank_close_over_open, filter = False)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()