import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_std_dev, divide, inverse, rank

def factor_6046(data, **kwargs):
    """
    因子名称: VWAP_Skewness_Volatility_Ratio_Ranked_Inverse_10633
    数学表达式: rank(inverse(divide(ts_skewness(vwap, 25), ts_std_dev(vwap, 15))))
    中文描述: 该因子基于对参考因子 'VolumeWeightedPriceVolatilitySkewnessRatio' 的改进建议，衡量成交量加权平均价（VWAP）的偏度与标准差之比，并对其进行截面排序和取倒数。首先计算过去25天VWAP的偏度，捕捉价格分布的极端情况。然后计算过去15天VWAP的标准差，衡量价格波动性。将偏度除以标准差得到偏度波动性比率。接着，对该比率取倒数，并进行截面排名。该因子创新性地结合了偏度、波动性和截面排名，并通过取倒数来调整因子的预测方向，使其与未来收益率呈现正相关关系的可能性增加。相较于参考因子，该因子通过截面排名降低了异常值的影响，通过取倒数调整了预测方向，并使用了不同的时间窗口，增强了因子的稳定性和预测能力。改进建议中提到的反向使用、截面排序和调整时间窗口的操作符（rank, inverse）被有效应用。
    因子应用场景：
    1. 识别价格分布的极端情况。
    2. 衡量价格波动性。
    3. 调整因子的预测方向，使其与未来收益率呈现正相关关系的可能性增加。
    """
    # 1. 计算 ts_skewness(vwap, 25)
    data_ts_skewness = ts_skewness(data['vwap'], d = 25)
    # 2. 计算 ts_std_dev(vwap, 15)
    data_ts_std_dev = ts_std_dev(data['vwap'], d = 15)
    # 3. 计算 divide(ts_skewness(vwap, 25), ts_std_dev(vwap, 15))
    data_divide = divide(data_ts_skewness, data_ts_std_dev)
    # 4. 计算 inverse(divide(ts_skewness(vwap, 25), ts_std_dev(vwap, 15)))
    data_inverse = inverse(data_divide)
    # 5. 计算 rank(inverse(divide(ts_skewness(vwap, 25), ts_std_dev(vwap, 15))))
    factor = rank(data_inverse, rate = 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()