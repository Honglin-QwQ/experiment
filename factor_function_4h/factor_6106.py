import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_6106(data, **kwargs):
    """
    因子名称: VolumeWeightedOpenDeviationRatio_93372
    数学表达式: divide(ts_mean(multiply(subtract(open, ts_delay(vwap, 1)), vol), 10), ts_std_dev(ts_returns(close, 1), 10))
    中文描述: 该因子衡量过去10天内，开盘价相对于前一日VWAP的成交量加权平均偏差，并用过去10天收盘价日收益率的标准差进行调整。分子通过计算每日(开盘价 - 前一日VWAP)与当日成交量的乘积，再计算其10日均值，捕捉了开盘价相对于近期成交均价的带权偏离程度，成交量越大，该偏离的影响越大。分母则反映了近期价格波动的剧烈程度。通过将带权开盘价偏移量除以波动率，该因子旨在提供一个波动率调整后的、考虑成交量影响的开盘价相对强弱信号。相较于参考因子和历史输出因子，该因子创新性地引入了成交量加权的概念，并使用了前一日的VWAP作为基准，同时保留了波动率调整。高因子值可能表示在成交量活跃且波动率相对较低时期，开盘价相对于前一日的成交均价显著偏高，可能预示着超买或潜在的回调；低因子值则可能表示在成交量活跃且波动率相对较低时期，开盘价显著偏低，可能预示着超卖或潜在的反弹。该因子可用于识别波动率较低且成交量活跃时期内，开盘价相对于前一日成交均价的异常偏离，从而辅助进行均值回归或反转策略。
    因子应用场景：
    1. 均值回归策略：识别开盘价相对于前一日VWAP的异常偏离，辅助进行均值回归策略。
    2. 反转策略：识别超买或超卖信号，辅助进行反转策略。
    """
    # 1. 计算 ts_delay(vwap, 1)
    data_ts_delay_vwap = ts_delay(data['vwap'], 1)
    # 2. 计算 subtract(open, ts_delay(vwap, 1))
    data_subtract = subtract(data['open'], data_ts_delay_vwap)
    # 3. 计算 multiply(subtract(open, ts_delay(vwap, 1)), vol)
    data_multiply = multiply(data_subtract, data['vol'])
    # 4. 计算 ts_mean(multiply(subtract(open, ts_delay(vwap, 1)), vol), 10)
    data_ts_mean = ts_mean(data_multiply, 10)
    # 5. 计算 ts_returns(close, 1)
    data_ts_returns = ts_returns(data['close'], 1)
    # 6. 计算 ts_std_dev(ts_returns(close, 1), 10)
    data_ts_std_dev = ts_std_dev(data_ts_returns, 10)
    # 7. 计算 divide(ts_mean(multiply(subtract(open, ts_delay(vwap, 1)), vol), 10), ts_std_dev(ts_returns(close, 1), 10))
    factor = divide(data_ts_mean, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()