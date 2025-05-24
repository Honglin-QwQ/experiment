import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_weighted_decay, ts_delta, sigmoid, ts_zscore, multiply

def factor_5574(data, **kwargs):
    """
    数学表达式: ts_rank(ts_weighted_decay(ts_delta(amount, 3), k = 0.3), 10) * sigmoid(ts_zscore(ts_delta(close, 5), 10))
    中文描述: 该因子旨在结合量价信息，捕捉市场动量。它首先计算过去3天交易额变化的时间加权衰减值，并对其进行排序，以衡量成交量的动量。同时，计算过去5天收盘价变化的Z-score，并通过sigmoid函数将其转换为0到1之间的值，以衡量价格的动量。最后，将成交量动量和价格动量相乘，得到最终的因子值。该因子的创新之处在于，它将成交量和价格的动量结合起来，并通过sigmoid函数对价格动量进行非线性转换，从而更灵敏地捕捉市场情绪的转变。
    因子应用场景：
    1. 动量捕捉：用于识别成交量和价格均呈现上涨趋势的股票。
    2. 市场情绪：结合sigmoid函数，可以更灵敏地捕捉市场情绪的转变。
    """
    # 1. 计算 ts_delta(amount, 3)
    data_ts_delta_amount = ts_delta(data['amount'], 3)
    # 2. 计算 ts_weighted_decay(ts_delta(amount, 3), k = 0.3)
    data_ts_weighted_decay = ts_weighted_decay(data_ts_delta_amount, k = 0.3)
    # 3. 计算 ts_rank(ts_weighted_decay(ts_delta(amount, 3), k = 0.3), 10)
    data_ts_rank = ts_rank(data_ts_weighted_decay, d = 10)
    # 4. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 5. 计算 ts_zscore(ts_delta(close, 5), 10)
    data_ts_zscore = ts_zscore(data_ts_delta_close, d = 10)
    # 6. 计算 sigmoid(ts_zscore(ts_delta(close, 5), 10))
    data_sigmoid = sigmoid(data_ts_zscore)
    # 7. 计算 ts_rank(ts_weighted_decay(ts_delta(amount, 3), k = 0.3), 10) * sigmoid(ts_zscore(ts_delta(close, 5), 10))
    factor = multiply(data_ts_rank, data_sigmoid)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()