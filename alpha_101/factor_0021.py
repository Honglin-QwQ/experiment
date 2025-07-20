import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_delta, rank, ts_std_dev, multiply

def factor_0021(data, **kwargs):
    """
    数学表达式: (-1 * (ts_delta(ts_corr(high, volume, 5), 5) * rank(ts_std_dev(close, 20)))) 
    中文描述: 该因子首先计算过去5天最高价和成交量的相关性，然后计算这个相关性时间序列的5日差分，再对结果进行排序，得到一个相对排名。同时，计算过去20天收盘价的标准差。最后，将相关性差分的排名乘以标准差，并取负号。这个因子试图捕捉量价关系变化的速度和价格波动率之间的关系，负号表示反向操作。
    应用场景：
    1. 可以用于识别量价背离的情况，例如，当相关性快速下降但价格波动较大时，可能预示着趋势反转。
    2. 可以作为趋势跟踪策略的辅助指标，结合其他技术指标判断趋势的强弱。
    3. 可以用于构建高频交易策略，捕捉短期内的量价异动。
    """
    # 1. 计算 ts_corr(high, volume, 5)
    data_ts_corr = ts_corr(data['high'], data['vol'], 5)
    # 2. 计算 ts_delta(ts_corr(high, volume, 5), 5)
    data_ts_delta = ts_delta(data_ts_corr, 5)
    # 3. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], 20)
    # 4. 计算 rank(ts_std_dev(close, 20))
    data_rank = rank(data_ts_std_dev, rate = 2)
    # 5. 计算 ts_delta(ts_corr(high, volume, 5), 5) * rank(ts_std_dev(close, 20))
    data_multiply = multiply(data_ts_delta, data_rank, filter=False)
    # 6. 计算 -1 * (ts_delta(ts_corr(high, volume, 5), 5) * rank(ts_std_dev(close, 20))))
    factor = multiply(-1, data_multiply, filter=False)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()