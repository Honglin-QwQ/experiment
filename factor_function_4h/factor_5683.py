import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_delta, ts_weighted_decay, ts_rank, ts_covariance

import pandas as pd

def factor_5683(data, **kwargs):
    """
    因子名称: factor_0002_62389
    数学表达式: ts_zscore(ts_delta(ts_weighted_decay(close, k=0.2), 2), 5) * ts_rank(ts_covariance(high, ts_weighted_decay(vol, k=0.3), 5), 10)
    中文描述: 该因子结合了价格动量和价量关系，并引入了加权衰减的概念。首先，使用`ts_weighted_decay(close, k=0.2)`对收盘价进行加权衰减，k=0.2表示当日收盘价的权重为0.2，前一日收盘价的权重为0.8*0.2，以此类推，从而更强调近期价格的影响。然后，计算加权衰减后收盘价的2日差分`ts_delta(..., 2)`，再计算该差分的5日Z-score，衡量价格变化的标准化程度。同时，对成交量也进行加权衰减`ts_weighted_decay(vol, k=0.3)`，并计算最高价和加权衰减后成交量的5日协方差`ts_covariance(high, ..., 5)`，并计算其10日排名`ts_rank(..., 10)`，反映价量关系的强度。最后，将价格动量Z-score与价量关系排名相乘，旨在捕捉价格趋势和成交量支撑之间的关系。创新点在于使用加权衰减来平滑价格和成交量，并提高因子对市场微观结构变化的敏感性，同时避免直接使用kth_element可能带来的问题。
    因子应用场景：
    1. 趋势识别：该因子结合了价格动量和价量关系，可用于识别趋势。
    2. 量价关系：通过协方差和排名，可以捕捉价量关系的强度。
    """

    # 1. ts_weighted_decay(close, k=0.2)
    weighted_decay_close = ts_weighted_decay(data['close'], k=0.2)

    # 2. ts_delta(ts_weighted_decay(close, k=0.2), 2)
    delta_weighted_close = ts_delta(weighted_decay_close, d=2)

    # 3. ts_zscore(ts_delta(ts_weighted_decay(close, k=0.2), 2), 5)
    zscore_delta_weighted_close = ts_zscore(delta_weighted_close, d=5)

    # 4. ts_weighted_decay(vol, k=0.3)
    weighted_decay_vol = ts_weighted_decay(data['vol'], k=0.3)

    # 5. ts_covariance(high, ts_weighted_decay(vol, k=0.3), 5)
    covariance_high_weighted_vol = ts_covariance(data['high'], weighted_decay_vol, d=5)

    # 6. ts_rank(ts_covariance(high, ts_weighted_decay(vol, k=0.3), 5), 10)
    rank_covariance_high_weighted_vol = ts_rank(covariance_high_weighted_vol, d=10)

    # 7. ts_zscore(ts_delta(ts_weighted_decay(close, k=0.2), 2), 5) * ts_rank(ts_covariance(high, ts_weighted_decay(vol, k=0.3), 5), 10)
    factor = zscore_delta_weighted_close * rank_covariance_high_weighted_vol

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()