import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_mean, multiply, ts_delta, ts_skewness

def factor_5961(data, **kwargs):
    """
    数学表达式: ts_mean(multiply(ts_delta(tbase, 3), ts_skewness(vwap, 22)), 51)
    中文描述: 该因子结合了主动买入量的短期变化和VWAP的长期偏斜度。首先计算主动买入基础币种数量（tbase）在3天内的变化量，这反映了短期的买入动量。然后，将这个变化量与VWAP在过去22天内的偏斜度相乘。VWAP的偏斜度可以捕捉长期价格分布的不对称性，正偏斜度可能意味着市场在一段时间内倾向于经历较大的正向价格波动。最后，计算这个乘积在过去51天内的均值。这个均值因子旨在捕捉短期买入动量与长期价格偏斜度之间的相互作用，并平滑短期波动，以识别更稳定的趋势。创新点在于将短期主动买入量变化与长期VWAP偏斜度结合，并通过时间序列均值进行平滑和长期趋势捕捉。
    因子应用场景：
    1. 动量确认：当因子值为正且较高时，可能表明短期买入动量与长期价格正偏斜度一致，从而确认上升趋势。
    2. 趋势反转信号：因子值的显著变化可能预示趋势的反转。例如，从正值变为负值可能表明买入动量减弱，价格偏斜度减小，预示下跌趋势。
    3. 市场情绪分析：通过观察因子值，可以洞察市场参与者的情绪。高因子值可能反映乐观情绪，而低因子值可能反映悲观情绪。
    """
    # 1. 计算 ts_delta(tbase, 3)
    data_ts_delta_tbase = ts_delta(data['tbase'], 3)
    # 2. 计算 ts_skewness(vwap, 22)
    data_ts_skewness_vwap = ts_skewness(data['vwap'], 22)
    # 3. 计算 multiply(ts_delta(tbase, 3), ts_skewness(vwap, 22))
    data_multiply = multiply(data_ts_delta_tbase, data_ts_skewness_vwap)
    # 4. 计算 ts_mean(multiply(ts_delta(tbase, 3), ts_skewness(vwap, 22)), 51)
    factor = ts_mean(data_multiply, 51)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()