import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_max, ts_min, ts_corr, rank, sigmoid, ts_skewness
import pandas as pd

def factor_5691(data, **kwargs):
    """
    因子名称: factor_0003_91425
    数学表达式: ts_delta(ts_max(high, 5), 20) * ts_delta(ts_min(low, 5), 20) * rank(ts_corr(close, vol, 10)) * sigmoid(ts_skewness(close, 20))
    中文描述: 本因子在history_output的基础上，引入了sigmoid(ts_skewness(close, 20))，旨在捕捉价格偏度对因子表现的影响。ts_skewness(close, 20)计算过去20天收盘价的偏度，衡量价格分布的不对称性。sigmoid函数将偏度值转换为0到1之间的值，用于平滑偏度对因子值的影响。通过将偏度信息融入因子，可以增强因子对市场情绪的捕捉能力，从而提高因子的预测能力。sigmoid函数的引入，使得因子对偏度的反应更加平滑，避免了极端偏度值对因子表现的过度影响。
    因子应用场景：
    1. 市场情绪捕捉：通过结合价格偏度，增强因子对市场情绪的捕捉能力。
    2. 趋势预测：利用价格偏度信息，提高因子对未来趋势的预测能力。
    3. 风险管理：通过平滑偏度影响，降低极端市场波动对因子表现的影响。
    """
    # 1. 计算 ts_max(high, 5)
    data_ts_max = ts_max(data['high'], d=5)
    # 2. 计算 ts_delta(ts_max(high, 5), 20)
    data_ts_delta_max = ts_delta(data_ts_max, d=20)
    # 3. 计算 ts_min(low, 5)
    data_ts_min = ts_min(data['low'], d=5)
    # 4. 计算 ts_delta(ts_min(low, 5), 20)
    data_ts_delta_min = ts_delta(data_ts_min, d=20)
    # 5. 计算 ts_corr(close, vol, 10)
    data_ts_corr = ts_corr(data['close'], data['vol'], d=10)
    # 6. 计算 rank(ts_corr(close, vol, 10))
    data_rank = rank(data_ts_corr, rate=2)
    # 7. 计算 ts_skewness(close, 20)
    data_ts_skewness = ts_skewness(data['close'], d=20)
    # 8. 计算 sigmoid(ts_skewness(close, 20))
    data_sigmoid = sigmoid(data_ts_skewness)
    # 9. 计算 ts_delta(ts_max(high, 5), 20) * ts_delta(ts_min(low, 5), 20) * rank(ts_corr(close, vol, 10)) * sigmoid(ts_skewness(close, 20))
    factor = data_ts_delta_max * data_ts_delta_min * data_rank * data_sigmoid

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()