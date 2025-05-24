import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import adv, ts_delta, quantile
import pandas as pd

def factor_5583(data, **kwargs):
    """
    因子名称: factor_volume_momentum_quantile_26676
    数学表达式: quantile(ts_delta(adv(vol, 10), 20), driver='gaussian')
    中文描述: 该因子通过计算成交量平均值的变化，并使用高斯分布进行分位数转换，来捕捉成交量动量的变化。具体来说，首先计算过去10天成交量的平均值，然后计算该平均值在过去20天内的变化量，最后通过高斯分布的分位数转换来突出成交量动量的极端变化。该因子可以用于识别成交量突然增加或减少的股票，从而辅助判断股票的潜在上涨或下跌趋势。
    因子应用场景：
    1. 识别成交量突增/突降：因子值较高可能表示成交量显著增加，反之则表示成交量显著减少。
    2. 趋势判断：结合股价走势，成交量增加可能预示上涨趋势，成交量减少可能预示下跌趋势。
    """
    # 1. 计算 adv(vol, 10)
    data_adv_vol = adv(data['vol'], d = 10)
    # 2. 计算 ts_delta(adv(vol, 10), 20)
    data_ts_delta = ts_delta(data_adv_vol, d = 20)
    # 3. 计算 quantile(ts_delta(adv(vol, 10), 20), driver='gaussian')
    factor = quantile(data_ts_delta, driver='gaussian')

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()