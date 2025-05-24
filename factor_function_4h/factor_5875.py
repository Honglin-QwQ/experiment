import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_skewness

def factor_5875(data, **kwargs):
    """
    因子名称: VolumeWeightedPriceChangeSkewnessRatio_79832
    数学表达式: divide(ts_skewness(divide(close - open, vol + 0.001), 15), ts_skewness(divide(high - low, vol + 0.001), 15))
    中文描述: 该因子计算的是基于成交量的价格变化偏度比率。分子是过去15天内，每日收盘价减去开盘价除以成交量的偏度，衡量了每日价格波动方向相对于成交量分布的偏斜程度。分母是过去15天内，每日最高价减去最低价除以成交量的偏度，衡量了每日价格波动幅度相对于成交量分布的偏斜程度。该因子通过比较这两个偏度，试图捕捉在考虑成交量影响下，价格方向性波动与价格幅度波动在分布上的相对偏斜关系。如果因子值较高，可能意味着在给定的成交量下，价格的方向性变化（上涨或下跌）的分布比价格整体波动的分布更偏向某一侧，这可能预示着趋势的强度或反转。创新点在于引入偏度作为衡量价格波动质量的指标，并将其与成交量结合，提供了一个新的视角来衡量价格波动的非对称性。
    因子应用场景：
    1. 趋势识别：因子值较高可能意味着趋势较强。
    2. 反转信号：因子值异常可能预示着趋势反转。
    """
    # 1. 计算 divide(close - open, vol + 0.001)
    data_numerator_input = divide(data['close'] - data['open'], data['vol'] + 0.001)
    # 2. 计算 ts_skewness(divide(close - open, vol + 0.001), 15)
    numerator = ts_skewness(data_numerator_input, d = 15)
    # 3. 计算 divide(high - low, vol + 0.001)
    data_denominator_input = divide(data['high'] - data['low'], data['vol'] + 0.001)
    # 4. 计算 ts_skewness(divide(high - low, vol + 0.001), 15)
    denominator = ts_skewness(data_denominator_input, d = 15)
    # 5. 计算 divide(ts_skewness(divide(close - open, vol + 0.001), 15), ts_skewness(divide(high - low, vol + 0.001), 15))
    factor = divide(numerator, denominator)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()