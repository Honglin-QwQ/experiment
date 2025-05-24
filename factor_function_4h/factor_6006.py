import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_decay_linear, ts_std_dev, subtract

def factor_6006(data, **kwargs):
    """
    因子名称: Volatility_Skew_Decay_Divergence_31019
    数学表达式: subtract(ts_skewness(vol, 60), ts_decay_linear(ts_std_dev(close, 20), 40))
    中文描述: 该因子旨在捕捉成交量偏度与短期收盘价标准差线性衰减之间的背离。首先，计算过去60天成交量的偏度，反映成交量分布的非对称性，高偏度可能意味着存在异常的大量交易日。然后，计算过去20天收盘价标准差的40天线性衰减值，反映短期价格波动性的方向和强度，并给予近期波动性更大的权重。将成交量偏度减去价格波动性的线性衰减值，如果成交量分布偏向极端值而短期价格波动性趋于下降，或者成交量分布趋于对称而短期价格波动性趋于上升，则因子值会偏离零，可能预示着市场情绪和价格行为之间的不一致，潜在地指示趋势的脆弱性或反转。创新点在于结合了成交量分布的偏度和价格波动性的线性衰减，通过差值形式捕捉两者之间的背离，提供了一个新的视角来识别市场情绪和潜在的趋势变化。该因子参考了成交量峰度（ts_kurtosis(vol, 66)）中对成交量分布形态的关注，并借鉴了历史输出中对价格趋势分析的思路，同时根据改进建议使用了ts_skewness、ts_std_dev和ts_decay_linear操作符来捕捉偏度、波动性和衰减趋势。
    因子应用场景：
    1. 市场情绪识别： 用于识别市场情绪和价格行为之间的不一致性。
    2. 趋势反转预测：潜在地指示趋势的脆弱性或反转。
    """
    # 1. 计算 ts_skewness(vol, 60)
    data_ts_skewness = ts_skewness(data['vol'], 60)
    # 2. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], 20)
    # 3. 计算 ts_decay_linear(ts_std_dev(close, 20), 40)
    data_ts_decay_linear = ts_decay_linear(data_ts_std_dev, 40)
    # 4. 计算 subtract(ts_skewness(vol, 60), ts_decay_linear(ts_std_dev(close, 20), 40))
    factor = subtract(data_ts_skewness, data_ts_decay_linear)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()