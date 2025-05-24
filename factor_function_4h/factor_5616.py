import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log, adv, ts_scale, multiply
import pandas as pd
import numpy as np

def factor_5616(data, **kwargs):
    """
    因子名称: factor_volume_price_interaction_60536
    数学表达式: ts_scale(multiply(returns, log(adv(20))), 52, constant=-1)
    中文描述: 本因子旨在捕捉成交量与收益率之间的相互作用，并进行时间序列上的缩放。具体而言，它首先计算日收益率（returns）与过去20天平均成交量取对数后的乘积，然后使用ts_scale函数对该乘积在过去52天内进行缩放，并减去常数1。创新之处在于结合了收益率和成交量的对数，并通过时间序列缩放，使得因子对不同股票和不同时间段具有可比性，从而可能更好地识别市场对特定股票兴趣的变化。
    因子应用场景：
    1. 市场情绪分析：当因子值较高时，可能表明市场对该股票的兴趣增加，成交量放大且收益率较高。
    2. 趋势跟踪：该因子可能有助于识别成交量支持的上涨趋势。
    3. 异常检测：异常高的因子值可能指示市场对特定股票的异常关注。
    """
    # 1. 计算 adv(20)
    adv_20 = adv(data['vol'], d = 20)
    # 2. 计算 log(adv(20))
    log_adv_20 = log(adv_20)
    # 3. 计算 multiply(returns, log(adv(20)))
    returns_log_adv = multiply(data['returns'], log_adv_20)
    # 4. 计算 ts_scale(multiply(returns, log(adv(20))), 52, constant=-1)
    factor = ts_scale(returns_log_adv, d = 52, constant = -1)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()