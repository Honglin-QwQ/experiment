import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_delta, ts_entropy, rank

def factor_6093(data, **kwargs):
    """
    因子名称: VolDeltaEntropyRatio_Ranked_91836
    数学表达式: rank(divide(ts_delta(vol, 5), ts_entropy(close, 60)))
    中文描述: 该因子是基于历史因子'VolPriceEntropyRatio_WeightedDelta'的改进版本。它计算过去60天内收盘价信息熵与交易量5日变化率的比值，并对结果进行全市场排名。相较于原始因子，创新点在于：1. 移除指数衰减加权平均，简化因子结构，降低参数敏感性；2. 使用交易量5日变化率，捕捉短期交易量动量；3. 对最终结果进行全市场排名，消除量纲影响，增强因子可比性，并可能捕捉市场相对强弱。该因子旨在识别交易量动量与价格混乱程度之间的相对关系，并通过排名来衡量其在市场中的相对位置，可能用于捕捉市场情绪的快速变化和潜在的相对价格趋势。
    因子应用场景：
    1. 市场情绪识别：通过交易量变化和价格信息熵的比值，识别市场情绪的快速变化。
    2. 相对强弱判断：通过全市场排名，衡量股票在市场中的相对位置，捕捉潜在的相对价格趋势。
    """
    # 1. 计算 ts_delta(vol, 5)
    data_ts_delta_vol = ts_delta(data['vol'], 5)
    # 2. 计算 ts_entropy(close, 60)
    data_ts_entropy_close = ts_entropy(data['close'], 60)
    # 3. 计算 divide(ts_delta(vol, 5), ts_entropy(close, 60))
    data_divide = divide(data_ts_delta_vol, data_ts_entropy_close)
    # 4. 计算 rank(divide(ts_delta(vol, 5), ts_entropy(close, 60)))
    factor = rank(data_divide, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()