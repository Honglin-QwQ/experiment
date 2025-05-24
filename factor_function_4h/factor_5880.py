import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_entropy, adv
import pandas as pd

def factor_5880(data, **kwargs):
    """
    因子名称: VolumeWeightedPriceChangeEntropyRatio_17828
    数学表达式: divide(ts_entropy(divide(close - open, adv(vol, 10) + 0.001), 15), ts_entropy(divide(high - low, adv(vol, 10) + 0.001), 15))
    中文描述: 该因子计算的是基于平均成交量的价格变化信息熵比率。分子是过去15天内，每日收盘价减去开盘价除以10日平均成交量的熵，衡量了每日价格波动方向相对于平均成交量分布的无序程度。分母是过去15天内，每日最高价减去最低价除以10日平均成交量的熵，衡量了每日价格波动幅度相对于平均成交量分布的无序程度。该因子通过比较这两个熵值，试图捕捉在考虑平均成交量影响下，价格方向性波动与价格幅度波动在分布上的相对无序关系。相较于原因子使用偏度，该因子使用信息熵来衡量分布的复杂性和不确定性，并采用平均成交量进行标准化，以提高因子的稳健性。如果因子值较高，可能意味着在给定的平均成交量下，价格的方向性变化（上涨或下跌）的分布比价格整体波动的分布更无序，这可能预示着市场的不确定性或潜在的趋势变化。创新点在于引入信息熵作为衡量价格波动复杂性的指标，并结合平均成交量进行标准化，提供了一个新的视角来衡量价格波动的无序性。
    因子应用场景：
    1. 市场不确定性评估：用于评估市场价格波动方向和幅度相对于成交量的无序程度，值越高可能表示市场不确定性增加。
    2. 趋势变化预警：因子值变化可能预示潜在的市场趋势变化，尤其是在成交量相对稳定的情况下。
    """
    # 1. 计算 adv(vol, 10)
    data_adv_vol = adv(data['vol'], 10)
    # 2. 计算 adv(vol, 10) + 0.001
    data_adv_vol_plus = data_adv_vol + 0.001
    # 3. 计算 close - open
    data_close_minus_open = data['close'] - data['open']
    # 4. 计算 divide(close - open, adv(vol, 10) + 0.001)
    data_price_change_ratio = divide(data_close_minus_open, data_adv_vol_plus)
    # 5. 计算 ts_entropy(divide(close - open, adv(vol, 10) + 0.001), 15)
    data_ts_entropy_numerator = ts_entropy(data_price_change_ratio, 15)
    # 6. 计算 high - low
    data_high_minus_low = data['high'] - data['low']
    # 7. 计算 divide(high - low, adv(vol, 10) + 0.001)
    data_price_range_ratio = divide(data_high_minus_low, data_adv_vol_plus)
    # 8. 计算 ts_entropy(divide(high - low, adv(vol, 10) + 0.001), 15)
    data_ts_entropy_denominator = ts_entropy(data_price_range_ratio, 15)
    # 9. 计算 divide(ts_entropy(divide(close - open, adv(vol, 10) + 0.001), 15), ts_entropy(divide(high - low, adv(vol, 10) + 0.001), 15))
    factor = divide(data_ts_entropy_numerator, data_ts_entropy_denominator)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()