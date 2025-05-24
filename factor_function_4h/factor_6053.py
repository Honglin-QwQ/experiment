import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_corr, ts_std_dev, divide, subtract, multiply

def factor_6053(data, **kwargs):
    """
    因子名称: VolatilitySkewVolumeCorrelation_96904
    数学表达式: multiply(ts_skewness(divide(subtract(high, low), open), 15), ts_corr(vol, ts_std_dev(close, 10), 7))
    中文描述: 该因子旨在捕捉市场波动性、成交量与价格波动率之间的复杂关系。它首先计算过去15天日内波动范围（最高价-最低价）与开盘价之比的偏度，衡量日内波动相对开盘价的非对称性。偏度为正则表示相对较大的日内波动倾向于出现在上涨时，反之亦然。然后，计算过去7天成交量与收盘价在过去10天内的标准差的相关性，反映成交量是否与短期价格波动率同步。最后将这两个指标相乘。因子值较高可能表示在相对日内波动偏向某一方向的同时，成交量与短期价格波动率呈现正相关，可能预示着趋势的加强或反转。相较于参考因子，创新点在于：1. 使用日内波动范围与开盘价的比值来衡量波动性，而非简单的收盘/开盘比值，更能体现日内价格的剧烈程度。2. 计算成交量与收盘价的短期标准差的相关性，关注成交量与价格波动率的关联，而非日内波动幅度。3. 调整了时间窗口参数，使用了更长的窗口（15天）计算偏度，以捕捉更稳定的波动性特征，同时使用较短的窗口（7天和10天）计算相关性和标准差，以反映近期的市场动态。这些改进旨在提高因子的预测能力和稳定性。
    因子应用场景：
    1. 波动性分析：用于识别市场波动性与成交量之间的关系。
    2. 趋势预测：因子值较高可能预示着趋势的加强或反转。
    """
    # 1. 计算 subtract(high, low)
    data_subtract = subtract(data['high'], data['low'])
    # 2. 计算 divide(subtract(high, low), open)
    data_divide = divide(data_subtract, data['open'])
    # 3. 计算 ts_skewness(divide(subtract(high, low), open), 15)
    data_ts_skewness = ts_skewness(data_divide, d=15)
    # 4. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], d=10)
    # 5. 计算 ts_corr(vol, ts_std_dev(close, 10), 7)
    data_ts_corr = ts_corr(data['vol'], data_ts_std_dev, d=7)
    # 6. 计算 multiply(ts_skewness(divide(subtract(high, low), open), 15), ts_corr(vol, ts_std_dev(close, 10), 7))
    factor = multiply(data_ts_skewness, data_ts_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()