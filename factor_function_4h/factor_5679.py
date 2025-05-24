import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_delta, log, multiply

def factor_5679(data, **kwargs):
    """
    因子名称: factor_0003_53502
    数学表达式: ts_zscore(ts_delta(high, 1) * log(vol), 19)
    中文描述: 本因子是对高价变化率与成交量取对数后的乘积进行Z-score标准化。首先计算每日最高价的变化量（ts_delta(high, 1)），然后将成交量取对数，旨在降低极端成交量对因子的影响，再将两者相乘，旨在放大高价变化且成交活跃的信号。最后，对这个乘积计算过去19天的Z-score（ts_zscore(..., 19)）。该因子旨在识别高价变化幅度相对于历史波动率的异常程度，并结合成交量信息，可以用于发现短期内价格异动且市场关注度高的情况，并评估这种异动是否显著超出常态。相比于factor_0002，本因子使用成交量的对数，可以减弱异常成交量对因子的影响，提高因子的稳健性。
    因子应用场景：
    1. 识别高价变化幅度相对于历史波动率的异常程度。
    2. 结合成交量信息，发现短期内价格异动且市场关注度高的情况。
    3. 评估价格异动是否显著超出常态。
    """
    # 1. 计算 ts_delta(high, 1)
    data_ts_delta_high = ts_delta(data['high'], d = 1)
    # 2. 计算 log(vol)
    data_log_vol = log(data['vol'])
    # 3. 计算 ts_delta(high, 1) * log(vol)
    data_multiply = multiply(data_ts_delta_high, data_log_vol)
    # 4. 计算 ts_zscore(ts_delta(high, 1) * log(vol), 19)
    factor = ts_zscore(data_multiply, d = 19)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()