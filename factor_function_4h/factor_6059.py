import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, jump_decay
import pandas as pd

def factor_6059(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Jump_Decay_39150
    数学表达式: jump_decay(ts_std_dev(vwap, 15), d=10, sensitivity=0.8, force=0.2)
    中文描述: 该因子旨在捕捉VWAP波动率中的显著“跳跃”并对其进行衰减处理。首先，计算VWAP在过去15天的标准差作为其短期波动率。然后，使用jump_decay运算符，在过去10天的时间窗口内，识别波动率相对于历史值的显著变化（跳跃），并根据设定的敏感度和衰减强度进行平滑处理。该因子通过关注波动率的异常变动并对其进行衰减，可以帮助识别波动率的突变和随后的平稳或反转趋势。相较于参考因子，该因子创新性地引入了jump_decay运算符，直接处理波动率的“跳跃”现象，而不是简单地比较线性衰减和指数衰减，以期更有效地捕捉波动率的非线性变化特征，并根据历史评估结果，尝试使用不同的时间序列处理方式提升因子表现。
    因子应用场景：
    1. 波动率突变识别：识别VWAP波动率的突然增加，可能预示着市场情绪或交易活动的显著变化。
    2. 趋势反转预测：通过衰减跳跃的影响，可以帮助平滑波动率序列，从而更好地识别潜在的趋势反转点。
    3. 风险管理：识别波动率的异常变动，有助于评估投资组合的风险水平。
    """
    # 1. 计算 ts_std_dev(vwap, 15)
    data_ts_std_dev = ts_std_dev(data['vwap'], d=15)
    # 2. 计算 jump_decay(ts_std_dev(vwap, 15), d=10, sensitivity=0.8, force=0.2)
    factor = jump_decay(data_ts_std_dev, d=10, sensitivity=0.8, force=0.2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()