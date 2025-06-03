import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_min, ts_max, multiply

import pandas as pd
import numpy as np

def factor_0008(data, **kwargs):
    """
    数学表达式: ((0 < ts_min(ts_delta(close, 1), 5)) ? ts_delta(close, 1) : ((ts_max(ts_delta(close, 1), 5) < 0) ? ts_delta(close, 1) : (-1 * ts_delta(close, 1)))) 
    中文描述: 如果过去5天内每日收盘价变化量的最小值大于0，则取当日收盘价变化量；否则，如果过去5天内每日收盘价变化量的最大值小于0，则取当日收盘价变化量；否则，取当日收盘价变化量的相反数。该因子衡量了股价短期变化的趋势和反转情况，可以用于捕捉短期反转机会、识别趋势加速或减速的股票、以及作为其他量化模型的输入特征。
    因子应用场景：
    1. 短期反转：当因子值为负时，可能预示着股价短期内有反转的可能。
    2. 趋势加速/减速：通过观察因子值的变化，可以判断当前趋势是在加速还是减速。
    3. 量化模型输入：该因子可以作为其他量化模型的输入特征，提高模型的预测准确性。
    """
    # 1. 计算 ts_delta(close, 1)
    delta_close = ts_delta(data['close'], 1)
    
    # 2. 计算 ts_min(ts_delta(close, 1), 5)
    min_delta_close = ts_min(delta_close, 5)
    
    # 3. 计算 ts_max(ts_delta(close, 1), 5)
    max_delta_close = ts_max(delta_close, 5)
    
    # 4. 实现条件判断
    factor = pd.Series(index=data.index, dtype='float64')
    for i in data.index:
        if min_delta_close[i] > 0:
            factor[i] = delta_close[i]
        elif max_delta_close[i] < 0:
            factor[i] = delta_close[i]
        else:
            factor[i] = multiply(-1, delta_close[i])

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()