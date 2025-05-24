import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log_diff, rank, ts_median, scale, divide

import pandas as pd
import numpy as np

def factor_5975(data, **kwargs):
    """
    因子名称: RankedLogDiffHigh_ScaledVolMedian_61405
    数学表达式: divide(rank(log_diff(high)), scale(ts_median(vol, 77)))
    中文描述: 该因子首先计算最高价的对数差分并进行横截面排名，然后计算过去77天交易量的中位数并进行横截面缩放。最后，将最高价对数差分的排名除以缩放后的交易量中位数。创新点在于结合了价格波动的相对变化（排名）和长期交易量的标准化水平，并引入了缩放操作符对交易量中位数进行处理。这可能用于识别在标准化交易量背景下，价格波动相对较强的股票，或者在价格波动排名较高时，判断其是否伴随有异常的交易量水平。相较于历史输出，该因子引入了rank和scale操作符，旨在提升因子的非线性和标准化特性，以期改善预测能力和稳定性。可以应用于捕捉价格波动与交易量的非线性关系，寻找潜在的交易机会。
    因子应用场景：
    1. 识别价格波动与交易量之间的非线性关系。
    2. 寻找在标准化交易量背景下，价格波动相对较强的股票。
    3. 判断价格波动排名较高时，是否伴随有异常的交易量水平。
    """
    # 1. 计算 log_diff(high)
    data_log_diff_high = log_diff(data['high'])
    # 2. 计算 rank(log_diff(high))
    data_rank_log_diff_high = rank(data_log_diff_high)
    # 3. 计算 ts_median(vol, 77)
    data_ts_median_vol = ts_median(data['vol'], d = 77)
    # 4. 计算 scale(ts_median(vol, 77))
    data_scale_ts_median_vol = scale(data_ts_median_vol)
    # 5. 计算 divide(rank(log_diff(high)), scale(ts_median(vol, 77)))
    factor = divide(data_rank_log_diff_high, data_scale_ts_median_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()