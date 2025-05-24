import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log_diff, ts_corr, rank

def factor_5804(data, **kwargs):
    """
    数学表达式: rank(ts_corr(vwap, log_diff(vwap), 10))
    中文描述: 该因子计算过去10天内VWAP与其对数差分之间的相关性，并对该相关性进行排名。参考了VWAP及其对数差分因子，并在此基础上引入了时间序列相关性分析和排名。创新点在于不再直接使用VWAP与log_diff(VWAP)的乘积，而是分析它们之间的动态关系（相关性），并通过排名来衡量这种关系的相对强弱。高排名可能表明VWAP与其短期变化趋势有较强的正相关性，可能预示着趋势的持续；低排名可能表明相关性较弱或为负，可能预示着趋势的减弱或反转。该因子旨在捕捉VWAP的短期动量与波动性之间的相互作用。
    因子应用场景：
    1. 趋势识别：识别VWAP与其短期变化趋势的联动关系。
    2. 动量分析：捕捉VWAP的短期动量与波动性之间的相互作用。
    """
    # 1. 计算 log_diff(vwap)
    data_log_diff_vwap = log_diff(data['vwap'])
    # 2. 计算 ts_corr(vwap, log_diff(vwap), 10)
    data_ts_corr = ts_corr(data['vwap'], data_log_diff_vwap, 10)
    # 3. 计算 rank(ts_corr(vwap, log_diff(vwap), 10))
    factor = rank(data_ts_corr, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()