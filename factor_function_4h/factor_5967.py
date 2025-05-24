import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_decay_linear
import pandas as pd

def factor_5967(data, **kwargs):
    """
    因子名称: Vol_Amount_Correlation_Decay_95392
    数学表达式: ts_decay_linear(ts_corr(vol, amount, 20), 30)
    中文描述: 该因子计算过去20天内成交量(vol)与交易额(amount)的相关性，然后对这个相关性序列应用30天的线性衰减。成交量与交易额的相关性反映了市场交易活动的质量和效率，理论上两者应该高度相关。如果相关性降低，可能表明交易结构发生变化或存在异常交易。线性衰减赋予近期相关性更高的权重，使得因子更能捕捉近期市场动态。该因子结合了参考因子对成交量和长期窗口的关注，创新性在于使用了成交量与交易额的滚动相关性，并引入了时间衰减，旨在捕捉市场交易质量的短期变化趋势。这响应了改进建议中关于关注成交额与价格相关性的思路，并进一步细化到成交量与交易额的相关性，同时通过衰减处理降低噪音并关注近期表现。
    因子应用场景：
    1. 市场质量评估：用于评估市场交易活动的质量和效率，通过成交量与交易额的相关性来判断市场是否存在异常交易行为。
    2. 短期趋势捕捉：通过线性衰减处理，该因子能够捕捉市场交易质量的短期变化趋势，帮助投资者及时调整策略。
    3. 交易结构分析：当成交量与交易额的相关性降低时，可能表明交易结构发生变化，该因子可用于分析这种变化。
    """
    # 1. 计算 ts_corr(vol, amount, 20)
    data_ts_corr = ts_corr(data['vol'], data['amount'], 20)
    # 2. 计算 ts_decay_linear(ts_corr(vol, amount, 20), 30)
    factor = ts_decay_linear(data_ts_corr, 30)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()