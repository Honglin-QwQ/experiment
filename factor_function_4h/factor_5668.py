import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import s_log_1p, ts_delta, ts_max

def factor_5668(data, **kwargs):
    """
    因子名称: factor_0007_66383
    数学表达式: ts_max(ts_delta(s_log_1p(vol), d=1), d=10)
    中文描述: 该因子首先对交易量进行对数变换，然后计算每日对数交易量的变化量，最后取过去10天内该变化量的最大值。该因子旨在捕捉交易量变化的峰值，通过对数变换降低异常值的影响，并使用最大值来识别交易量快速增长的潜在转折点。相较于历史因子，该因子简化了计算逻辑，直接关注交易量变化的峰值，更易于捕捉市场情绪的快速变化。
    因子应用场景：
    1. 交易量峰值识别：用于识别交易量快速增长的时间点，可能预示着市场情绪的转变。
    2. 转折点预测：结合其他因子，用于预测股票价格的潜在转折点。
    """
    # 1. 计算 s_log_1p(vol)
    data_s_log_1p_vol = s_log_1p(data['vol'])
    # 2. 计算 ts_delta(s_log_1p(vol), d=1)
    data_ts_delta = ts_delta(data_s_log_1p_vol, d=1)
    # 3. 计算 ts_max(ts_delta(s_log_1p(vol), d=1), d=10)
    factor = ts_max(data_ts_delta, d=10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()