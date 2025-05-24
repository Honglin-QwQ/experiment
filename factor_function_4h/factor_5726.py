import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log_diff, inverse, ts_median, multiply, rank, scale

def factor_5726(data, **kwargs):
    """
    因子名称: LogDiffHigh_VWAPMedianInverse_ScaledRank_23082
    数学表达式: scale(rank(multiply(log_diff(high), inverse(ts_median(vwap, 15)))))
    中文描述: 该因子结合了最高价的对数差分、VWAP中位数的倒数以及排名和缩放操作。它首先计算日内最高价的对数变化率，捕捉价格的相对波动。然后，计算过去15天VWAP的中位数，并取其倒数。将这两个值相乘，得到一个基础信号。接着，对这个基础信号进行排名，以消除量纲影响并突出相对表现。最后，对排名后的结果进行缩放，使其符合特定的范围或分布。该因子旨在识别那些近期最高价波动较大，同时过去一段时间内平均交易价格相对较低（中位数倒数较高）的股票，并通过排名和缩放增强信号的稳定性和可比性。相较于参考因子，创新点在于引入了排名和缩放操作，并调整了VWAP中位数的计算窗口，以期提高因子的预测能力和稳定性。同时，根据历史评估结果，该因子通过对乘积结果进行排名和缩放，间接实现了对信号的反转和波动性控制，从而有望改善之前的负相关和高波动问题。
    因子应用场景：
    1. 波动性分析：用于识别近期价格波动较大的股票。
    2. 价值发现：结合VWAP中位数倒数，寻找被低估的股票。
    3. 增强信号稳定性：通过排名和缩放，提高信号的稳定性和可比性。
    """
    # 1. 计算 log_diff(high)
    data_log_diff_high = log_diff(data['high'])
    # 2. 计算 ts_median(vwap, 15)
    data_ts_median_vwap = ts_median(data['vwap'], 15)
    # 3. 计算 inverse(ts_median(vwap, 15))
    data_inverse_ts_median_vwap = inverse(data_ts_median_vwap)
    # 4. 计算 multiply(log_diff(high), inverse(ts_median(vwap, 15)))
    data_multiply = multiply(data_log_diff_high, data_inverse_ts_median_vwap)
    # 5. 计算 rank(multiply(log_diff(high), inverse(ts_median(vwap, 15))))
    data_rank = rank(data_multiply, 2)
    # 6. 计算 scale(rank(multiply(log_diff(high), inverse(ts_median(vwap, 15)))))
    factor = scale(data_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()