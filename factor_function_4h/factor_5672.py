import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_delta, ts_std_dev

def factor_5672(data, **kwargs):
    """
    因子名称: factor_0001_58525
    数学表达式: ts_zscore(ts_delta(ts_std_dev(returns, 22), 5), 10)
    中文描述: 该因子结合了收益率的标准差和差分的概念，旨在捕捉市场波动率变化的动量。首先计算过去22天收益率的标准差，然后计算该标准差的5日差分，最后对该差分进行10日Z-score标准化。该因子试图识别波动率上升或下降的趋势，并将其标准化，以便更好地比较不同股票之间的波动率变化。
    因子应用场景：
    1. 波动率趋势识别：识别波动率上升或下降的趋势。
    2. 股票比较：标准化波动率变化，以便更好地比较不同股票之间的波动率变化。
    """
    # 1. 计算 ts_std_dev(returns, 22)
    data_ts_std_dev = ts_std_dev(data['returns'], 22)
    # 2. 计算 ts_delta(ts_std_dev(returns, 22), 5)
    data_ts_delta = ts_delta(data_ts_std_dev, 5)
    # 3. 计算 ts_zscore(ts_delta(ts_std_dev(returns, 22), 5), 10)
    factor = ts_zscore(data_ts_delta, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()