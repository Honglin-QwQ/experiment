import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_kurtosis, abs, ts_zscore, divide
import pandas as pd

def factor_6019(data, **kwargs):
    """
    因子名称: Volume_Price_Kurtosis_Zscore_Ratio_76994
    数学表达式: divide(ts_kurtosis(volume, 60), abs(ts_zscore(((high + low) / 2), 20)))
    中文描述: 该因子结合了成交量的峰度信息和中价的Z分数信息。它计算了过去60天成交量的峰度，用以衡量成交量分布的尖峰程度，高峰度可能意味着交易量的异常波动或集中。同时，计算了过去20天中价（最高价加最低价除以2）的Z分数，用以衡量当前中价相对于其近期均值的偏离程度，绝对值较大的Z分数表示价格偏离均值较大。最后，将成交量峰度除以中价Z分数的绝对值。该因子旨在捕捉市场中成交量异常集中且价格偏离近期均值较大的情况，可能预示着市场情绪的剧烈波动或潜在的价格反转。分母使用Z分数的绝对值，避免了负值的影响，并强调了偏离幅度。创新点在于结合了描述数据分布形态的峰度与衡量偏离程度的Z分数，并将两者进行比值，形成一个综合性的指标，用于识别市场中的“异常”状态。
    因子应用场景：
    1. 异常波动识别：用于识别成交量异常波动且价格偏离均值较大的股票。
    2. 情绪反转预测：可能预示市场情绪的剧烈波动或潜在的价格反转。
    """
    # 1. 计算 ts_kurtosis(volume, 60)
    volume_kurtosis = ts_kurtosis(data['vol'], 60)
    # 2. 计算 (high + low) / 2
    mid_price = (data['high'] + data['low']) / 2
    # 3. 计算 ts_zscore(((high + low) / 2), 20)
    mid_price_zscore = ts_zscore(mid_price, 20)
    # 4. 计算 abs(ts_zscore(((high + low) / 2), 20))
    abs_mid_price_zscore = abs(mid_price_zscore)
    # 5. 计算 divide(ts_kurtosis(volume, 60), abs(ts_zscore(((high + low) / 2), 20)))
    factor = divide(volume_kurtosis, abs_mid_price_zscore)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()