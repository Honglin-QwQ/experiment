import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, ts_max_diff, ts_std_dev, divide, add
import pandas as pd
import numpy as np

def factor_5874(data, **kwargs):
    """
    数学表达式: divide(ts_max_diff(ts_decay_linear(vol, 10), 30), add(ts_std_dev(ts_decay_linear(vol, 5), 5), 1e-6))
    中文描述: 《波动调整的成交量动量因子：捕捉成交量相对强度与波动》
    因子应用场景：
    1. 识别成交量在近期持续放大且放大过程相对稳定的股票。
    2. 辅助判断市场关注度的提升和潜在的价格上涨动力。
    """
    # 1. 计算 ts_decay_linear(vol, 10)
    data_ts_decay_linear_vol_10 = ts_decay_linear(data['vol'], 10)
    # 2. 计算 ts_max_diff(ts_decay_linear(vol, 10), 30)
    data_ts_max_diff = ts_max_diff(data_ts_decay_linear_vol_10, 30)
    # 3. 计算 ts_decay_linear(vol, 5)
    data_ts_decay_linear_vol_5 = ts_decay_linear(data['vol'], 5)
    # 4. 计算 ts_std_dev(ts_decay_linear(vol, 5), 5)
    data_ts_std_dev = ts_std_dev(data_ts_decay_linear_vol_5, 5)
    # 5. 计算 add(ts_std_dev(ts_decay_linear(vol, 5), 5), 1e-6)
    data_add = add(data_ts_std_dev, 1e-6)
    # 6. 计算 divide(ts_max_diff(ts_decay_linear(vol, 10), 30), add(ts_std_dev(ts_decay_linear(vol, 5), 5), 1e-6))
    factor = divide(data_ts_max_diff, data_add)

    # 删除中间变量
    del data_ts_decay_linear_vol_10
    del data_ts_max_diff
    del data_ts_decay_linear_vol_5
    del data_ts_std_dev
    del data_add

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()