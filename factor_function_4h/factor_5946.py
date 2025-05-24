import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5946(data, **kwargs):
    """
    因子名称: VolatilityAdjustedVolumePeak_45196
    数学表达式: divide(ts_max(adv(vol, 20), 26), ts_std_dev(adv(vol, 20), 26))
    中文描述: 该因子通过计算过去26天内，过去20天平均成交量的最高值，并将其除以过去26天内过去20天平均成交量的标准差来衡量市场关注度的峰值相对于其波动性的强度。它结合了参考因子中的时间序列最大值和平均成交量概念，并引入了标准差进行波动性调整，以识别在市场热度达到峰值时，其波动性相对较低的情况，这可能预示着更稳定的上涨趋势或潜在的交易机会。高因子值表示在最高平均成交量时期，成交量的波动性相对较低。
    因子应用场景：
    1. 识别市场关注度峰值：用于识别成交量在一段时间内达到峰值，且波动性较低的股票。
    2. 波动性调整：通过标准差调整，可以筛选出成交量峰值相对稳定的股票，可能预示着更可靠的趋势。
    3. 潜在交易机会：高因子值可能表示市场对该股票的关注度较高，且波动性相对较低，可能存在交易机会。
    """
    # 1. 计算 adv(vol, 20)
    data_adv = adv(data['vol'], d = 20)
    # 2. 计算 ts_max(adv(vol, 20), 26)
    data_ts_max = ts_max(data_adv, d = 26)
    # 3. 计算 ts_std_dev(adv(vol, 20), 26)
    data_ts_std_dev = ts_std_dev(data_adv, d = 26)
    # 4. 计算 divide(ts_max(adv(vol, 20), 26), ts_std_dev(adv(vol, 20), 26))
    factor = divide(data_ts_max, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()