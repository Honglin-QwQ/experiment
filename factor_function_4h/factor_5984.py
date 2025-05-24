import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract, rank, ts_max_diff, ts_min_diff

def factor_5984(data, **kwargs):
    """
    因子名称: VolWeighted_PriceChange_RankDiff_53257
    数学表达式: subtract(rank(ts_max_diff(close, 10)), rank(ts_min_diff(open, 10)))
    中文描述: 该因子计算了基于成交量的加权价格变化排名差异。它首先计算过去10天收盘价最大差异的排名，然后计算过去10天开盘价最小差异的排名，最后计算这两个排名的差值。这个因子结合了价格极值变化和排名信息，旨在捕捉短期内的市场情绪和动量差异。当收盘价最大差异的排名高于开盘价最小差异的排名时，可能表明市场情绪偏向多头，反之则偏向空头。创新点在于结合了价格极值差异和排名，并使用了减法操作来突出两者之间的相对强弱。
    因子应用场景：
    1. 市场情绪分析：可用于识别市场情绪的短期变化，判断多空力量的对比。
    2. 动量交易：结合排名差异，捕捉价格动量的变化，辅助判断买卖时机。
    """
    # 1. 计算 ts_max_diff(close, 10)
    data_ts_max_diff_close = ts_max_diff(data['close'], d = 10)
    # 2. 计算 rank(ts_max_diff(close, 10))
    data_rank_ts_max_diff_close = rank(data_ts_max_diff_close)
    # 3. 计算 ts_min_diff(open, 10)
    data_ts_min_diff_open = ts_min_diff(data['open'], d = 10)
    # 4. 计算 rank(ts_min_diff(open, 10))
    data_rank_ts_min_diff_open = rank(data_ts_min_diff_open)
    # 5. 计算 subtract(rank(ts_max_diff(close, 10)), rank(ts_min_diff(open, 10)))
    factor = subtract(data_rank_ts_max_diff_close, data_rank_ts_min_diff_open)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()