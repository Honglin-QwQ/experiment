import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd
import numpy as np

def factor_5613(data, **kwargs):
    """
    因子名称: factor_volume_price_correlation_change_25878
    数学表达式: ts_delta(ts_corr(log(vol), close, 5), 5)
    中文描述: 该因子旨在衡量成交量与价格相关性的变化。首先，计算过去5天成交量（取对数）与收盘价的相关性，然后计算该相关性在过去5天内的变化。
            创新之处在于关注相关性的变化而非相关性本身，这可以捕捉量价关系的动态变化。该因子适用于识别趋势反转和市场情绪变化，
            当相关性变化剧烈时，可能预示着趋势即将发生转变。对成交量取对数，可以降低成交量极端值的影响，使得因子对成交量变化更加敏感。
    因子应用场景：
    1. 趋势反转识别：当因子值剧烈变化时，可能预示着市场趋势即将发生转变。
    2. 市场情绪分析：该因子可以帮助分析市场情绪的变化，尤其是在量价关系出现异常波动时。
    """
    # 1. 计算 log(vol)
    data['log_vol'] = log(data['vol'])
    # 2. 计算 ts_corr(log(vol), close, 5)
    data['corr_log_vol_close'] = ts_corr(data['log_vol'], data['close'], 5)
    # 3. 计算 ts_delta(ts_corr(log(vol), close, 5), 5)
    factor = ts_delta(data['corr_log_vol_close'], 5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    data = data.drop(columns=['log_vol', 'corr_log_vol_close'])
    return data.sort_index()