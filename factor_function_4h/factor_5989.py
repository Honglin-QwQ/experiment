import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import multiply, ts_kurtosis

def factor_5989(data, **kwargs):
    """
    数学表达式: multiply(returns, ts_kurtosis(vol, 30))
    中文描述: 该因子结合了日收益率（returns）和过去30天成交量的峰度（ts_kurtosis(vol, 30)）。它通过将当前收益率与成交量分布的尖峰程度相乘，试图捕捉在成交量异常波动时期可能出现的放大收益或损失。当成交量分布高度集中（高峰度）时，该因子会放大当前收益率的影响。这可能有助于识别由市场情绪剧烈变化导致的短期价格动量。
    因子应用场景：
    1. 波动率放大：用于识别成交量峰度较高时，收益率的放大效应。
    2. 市场情绪识别：通过成交量峰度与收益率的相互作用，辅助判断市场情绪。
    """
    # 1. 计算 ts_kurtosis(vol, 30)
    data_ts_kurtosis = ts_kurtosis(data['vol'], 30)
    # 2. 计算 multiply(returns, ts_kurtosis(vol, 30))
    factor = multiply(data['returns'], data_ts_kurtosis)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()