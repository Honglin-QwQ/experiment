import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delta, log, ts_rank, sigmoid, ts_skewness, multiply

def factor_5621(data, **kwargs):
    """
    因子名称: factor_innovative_price_volume_momentum_v2_58212
    数学表达式: multiply(ts_std_dev(ts_delta(log(close/open),3), 15), ts_rank(vol,7), ts_delta(close, 5), sigmoid(ts_skewness(ts_delta(close, 1), 10)))
    中文描述: 该因子结合了价格波动率、成交量排名、价格动量和偏度，旨在捕捉市场短期价格变化与成交量和价格趋势之间的关系。首先，计算每日收盘价与开盘价之比的对数，并计算其3日差分，然后计算该差分序列的15日标准差，以衡量价格波动率。同时，计算过去7日成交量的排名。此外，计算过去5日的收盘价差值，以衡量价格动量。最重要的是，引入了收盘价一日差分的10日偏度，并使用sigmoid函数进行转换，以衡量价格动量的偏斜程度，并将其转化为0到1之间的值。最后，将价格波动率、成交量排名、价格动量和偏度相乘，以识别价格波动较大、成交量较高且具有价格趋势和偏度的股票。这种结合可能反映了市场对短期价格变动的强烈反应，并结合了价格趋势，从而提供潜在的交易信号。相比于之前的版本，该版本调整了波动率计算的窗口期，并引入了偏度来衡量价格动量的偏斜程度，从而更好地捕捉市场情绪。
    因子应用场景：
    1. 短期价格波动识别：用于识别价格波动较大的股票。
    2. 成交量确认：结合成交量排名，筛选出成交量活跃的股票。
    3. 价格动量跟踪：通过价格差值，捕捉价格的短期趋势。
    4. 市场情绪偏斜度量：通过偏度，衡量市场情绪的非对称性。
    """
    # 1. 计算 log(close/open)
    data_log_close_open = log(data['close'] / data['open'])
    # 2. 计算 ts_delta(log(close/open), 3)
    data_ts_delta_log_close_open = ts_delta(data_log_close_open, 3)
    # 3. 计算 ts_std_dev(ts_delta(log(close/open), 3), 15)
    data_ts_std_dev = ts_std_dev(data_ts_delta_log_close_open, 15)
    # 4. 计算 ts_rank(vol, 7)
    data_ts_rank_vol = ts_rank(data['vol'], 7)
    # 5. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 6. 计算 ts_delta(close, 1)
    data_ts_delta_close_1 = ts_delta(data['close'], 1)
    # 7. 计算 ts_skewness(ts_delta(close, 1), 10)
    data_ts_skewness = ts_skewness(data_ts_delta_close_1, 10)
    # 8. 计算 sigmoid(ts_skewness(ts_delta(close, 1), 10))
    data_sigmoid = sigmoid(data_ts_skewness)
    # 9. 计算 multiply(ts_std_dev(ts_delta(log(close/open),3), 15), ts_rank(vol,7), ts_delta(close, 5), sigmoid(ts_skewness(ts_delta(close, 1), 10)))
    factor = multiply(data_ts_std_dev, data_ts_rank_vol, data_ts_delta_close, data_sigmoid)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()