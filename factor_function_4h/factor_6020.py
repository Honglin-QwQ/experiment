import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_decay_linear, ts_std_dev, divide

def factor_6020(data, **kwargs):
    """
    因子名称: Volume_Volatility_Decay_Ratio_13651
    数学表达式: divide(ts_decay_linear(vol, 20), ts_std_dev(vol, 10))
    中文描述: 该因子计算过去20天成交量的线性衰减平均值与过去10天成交量标准差的比值。它结合了成交量的趋势（衰减平均）和波动性（标准差）。较高的因子值可能表明成交量在近期呈现下降趋势但波动性相对较低，或者成交量近期下降且波动性下降更快。这可能用于识别成交量萎缩但相对稳定的阶段，或成交量下降加速且波动性下降更快的阶段。创新点在于结合了线性衰减平均和标准差，并计算其比值，以捕捉成交量趋势与波动性的相对变化。
    因子应用场景：
    1. 成交量趋势分析：用于识别成交量萎缩但相对稳定的阶段，或成交量下降加速且波动性下降更快的阶段。
    2. 波动性分析：结合成交量的趋势和波动性，辅助判断市场稳定性和风险。
    """
    # 1. 计算 ts_decay_linear(vol, 20)
    data_ts_decay_linear_vol = ts_decay_linear(data['vol'], d = 20)
    # 2. 计算 ts_std_dev(vol, 10)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], d = 10)
    # 3. 计算 divide(ts_decay_linear(vol, 20), ts_std_dev(vol, 10))
    factor = divide(data_ts_decay_linear_vol, data_ts_std_dev_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()