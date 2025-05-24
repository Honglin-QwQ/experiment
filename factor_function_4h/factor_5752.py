import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_rank, ts_decay_linear

def factor_5752(data, **kwargs):
    """
    因子名称: VWAP_Rank_Decay_Ratio_37249
    数学表达式: divide(ts_rank(vwap, 7), ts_decay_linear(vwap, 10))
    中文描述: 该因子结合了VWAP的短期排名和长期线性衰减值。首先计算过去7天VWAP的时间序列排名（ts_rank(vwap, 7)），该值反映了当前VWAP在近期内的相对位置。然后计算过去10天VWAP的线性衰减值（ts_decay_linear(vwap, 10)），该值对近期VWAP赋予更高的权重，反映了VWAP的长期趋势。最后计算短期排名与长期衰减值的比率。较高的比率可能意味着当前VWAP在短期内相对较高，但长期趋势并不强劲，这可能预示着价格的潜在回调。该因子创新性地结合了时间序列的排名信息和线性衰减，提供了对VWAP动态的独特视角，并且根据历史评估结果，简化了表达式，减少了参数数量，并使用了ts_rank和ts_decay_linear这两个在改进建议中提及的可能有助于提升因子的操作符。
    因子应用场景：
    1. 趋势反转识别：较高的比率可能意味着当前VWAP在短期内相对较高，但长期趋势并不强劲，这可能预示着价格的潜在回调。
    2. 短期强势判断：比率越高，表示短期VWAP排名越高，可能意味着短期强势。
    """
    # 1. 计算 ts_rank(vwap, 7)
    data_ts_rank = ts_rank(data['vwap'], 7)
    # 2. 计算 ts_decay_linear(vwap, 10)
    data_ts_decay_linear = ts_decay_linear(data['vwap'], 10)
    # 3. 计算 divide(ts_rank(vwap, 7), ts_decay_linear(vwap, 10))
    factor = divide(data_ts_rank, data_ts_decay_linear)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()