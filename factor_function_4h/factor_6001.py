import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_rank, ts_entropy, ts_corr

def factor_6001(data, **kwargs):
    """
    因子名称: TS_Entropy_Rank_Ratio_VWAP_Corr_34347
    数学表达式: divide(ts_rank(ts_entropy(vol, 20), 30), ts_corr(vwap, vol, 10))
    中文描述: 该因子计算了短期（20天）成交量时间序列熵的时间序列排名（30天窗口）与短期（10天）VWAP与成交量相关性的比值。该因子旨在捕捉短期成交量信息含量排名与短期价量关系强弱的相对变化。当短期成交量熵排名相对于短期价量相关性较高时，可能预示着短期市场交易行为的不确定性增强，而价量关系趋同性相对减弱。这结合了时间序列熵、时间序列排名和时间序列相关性分析，提供了一个更动态和相对的视角来评估市场信息含量和价量关系的变化。相较于参考因子，创新点在于将成交量熵的排名与VWAP和成交量相关性进行比值计算，从而更直接地衡量信息的不确定性与市场趋同性之间的相对强度。
    因子应用场景：
    1. 市场不确定性评估：该因子可用于评估市场短期交易行为的不确定性，当因子值较高时，可能预示着市场信息含量较高，但价量关系趋同性减弱。
    2. 价量关系分析：通过分析成交量熵排名与价量相关性的比值，可以更全面地了解市场中的价量关系，辅助判断趋势的稳定性和可持续性。
    """
    # 1. 计算 ts_entropy(vol, 20)
    data_ts_entropy = ts_entropy(data['vol'], d = 20)
    # 2. 计算 ts_rank(ts_entropy(vol, 20), 30)
    data_ts_rank = ts_rank(data_ts_entropy, d = 30)
    # 3. 计算 ts_corr(vwap, vol, 10)
    data_ts_corr = ts_corr(data['vwap'], data['vol'], d = 10)
    # 4. 计算 divide(ts_rank(ts_entropy(vol, 20), 30), ts_corr(vwap, vol, 10))
    factor = divide(data_ts_rank, data_ts_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()