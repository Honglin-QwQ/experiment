import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, multiply, subtract,divide

def factor_0052(data, **kwargs):
    """
    数学表达式: (-1 * ts_delta((((close - low) - (high - close)) / (close - low)), 9))
    中文描述: 该因子计算过去9天内，每日价格波动中，收盘价相对于当日最高价和最低价位置的变化幅度，并取反。它衡量了价格重心在过去一段时间内的变化方向，可能反映了市场情绪或趋势的转变。
    应用场景包括：
    1. 短线择时：当因子值快速上升时，可能预示着买盘力量增强，可以考虑买入；反之，因子值快速下降时，可能预示着卖盘力量增强，可以考虑卖出。
    2. 趋势跟踪：结合其他趋势指标，可以辅助判断趋势的强弱和持续性。例如，因子值持续为正，可能表明上涨趋势较强。
    3. 捕捉反转：极端高或低的因子值可能预示着短期超买或超卖，从而寻找潜在的反转机会。
    """
    # 1. 计算 (close - low)
    close_minus_low = subtract(data['close'], data['low'])
    # 2. 计算 (high - close)
    high_minus_close = subtract(data['high'], data['close'])
    # 3. 计算 ((close - low) - (high - close))
    diff_minus_diff = subtract(close_minus_low, high_minus_close)
    # 4. 计算 (((close - low) - (high - close)) / (close - low))
    ratio = divide(diff_minus_diff, close_minus_low)
    # 5. 计算 ts_delta((((close - low) - (high - close)) / (close - low)), 9)
    ts_delta_result = ts_delta(ratio, d=9)
    # 6. 计算 -1 * ts_delta((((close - low) - (high - close)) / (close - low)), 9)
    factor = multiply(-1, ts_delta_result)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()