import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank
from operators import ts_corr
from operators import ts_std_dev
from operators import ts_rank
from operators import ts_delta
import pandas as pd

def factor_6018(data, **kwargs):
    """
    数学表达式: rank(ts_corr(vwap, ts_std_dev(vwap, 10), 5)) + ts_rank(ts_delta(vwap, 20), 15)
    中文描述: 《VWAP波动率排名动量因子：结合价格趋势、波动性和时间序列排名》
    该因子由两部分组成：
    1. 第一部分：计算VWAP与过去10天VWAP标准差在过去5天内的相关系数，然后对这个相关系数进行横截面排名。
    2. 第二部分：计算VWAP在过去20天内的变化量，然后对这个变化量在过去15天内进行时间序列排名。
    最终，将两部分的数值相加。
    因子应用场景：
    该因子通过结合VWAP的趋势、波动率以及不同时间维度的排名信息，旨在捕捉更复杂和持续的市场动量，可用于识别具有稳定趋势和动量特征的股票。
    """
    # 1. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], d = 10)
    # 2. 计算 ts_corr(vwap, ts_std_dev(vwap, 10), 5)
    data_ts_corr = ts_corr(data['vwap'], data_ts_std_dev_vwap, d = 5)
    # 3. 计算 rank(ts_corr(vwap, ts_std_dev(vwap, 10), 5))
    factor1 = rank(data_ts_corr, rate = 2)
    # 4. 计算 ts_delta(vwap, 20)
    data_ts_delta_vwap = ts_delta(data['vwap'], d = 20)
    # 5. 计算 ts_rank(ts_delta(vwap, 20), 15)
    factor2 = ts_rank(data_ts_delta_vwap, d = 15)
    # 6. 计算 rank(ts_corr(vwap, ts_std_dev(vwap, 10), 5)) + ts_rank(ts_delta(vwap, 20), 15)
    factor = factor1 + factor2

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()