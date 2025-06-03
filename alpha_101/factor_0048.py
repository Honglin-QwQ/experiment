import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delay, subtract, divide, multiply

def factor_0048(data, **kwargs):
    """
    数学表达式: (((((ts_delay(close, 20) - ts_delay(close, 10)) / 10) - ((ts_delay(close, 10) - close) / 10)) < (-1 * 0.1)) ? 1 : ((-1 * 1) * (close - ts_delay(close, 1))))
    中文描述: 该因子衡量了股价短期加速下跌的动能，首先计算过去20日到过去10日的股价变化与过去10日到现在的股价变化之差，并除以10进行标准化，如果这个差值小于-0.1，则因子值为1，否则因子值为负的当日股价变化。
    因子应用场景：
    1. 短线反弹策略：当因子值为1时，可能意味着股价短期下跌过快，存在反弹机会。
    2. 趋势跟踪策略：结合其他趋势指标，判断下跌趋势是否加速，辅助卖出决策。
    3. 异常检测：监控因子值，识别股价异常加速下跌的股票。
    """

    # 计算 ts_delay(close, 20)
    delay_20 = ts_delay(data['close'], d=20)

    # 计算 ts_delay(close, 10)
    delay_10 = ts_delay(data['close'], d=10)

    # 计算 (ts_delay(close, 20) - ts_delay(close, 10))
    diff_20_10 = subtract(delay_20, delay_10)

    # 计算 (ts_delay(close, 20) - ts_delay(close, 10)) / 10
    diff_20_10_normalized = divide(diff_20_10, 10)

    # 计算 (ts_delay(close, 10) - close)
    diff_10_now = subtract(delay_10, data['close'])

    # 计算 (ts_delay(close, 10) - close) / 10
    diff_10_now_normalized = divide(diff_10_now, 10)

    # 计算 ((ts_delay(close, 20) - ts_delay(close, 10)) / 10) - ((ts_delay(close, 10) - close) / 10)
    diff_normalized = subtract(diff_20_10_normalized, diff_10_now_normalized)

    # 计算 -1 * 0.1
    neg_01 = multiply(-1, 0.1)

    # 计算 close - ts_delay(close, 1)
    close_diff = subtract(data['close'], ts_delay(data['close'], d=1))

    # 计算 (-1 * 1) * (close - ts_delay(close, 1))
    neg_close_diff = multiply(-1, close_diff)

    # 计算 (((((ts_delay(close, 20) - ts_delay(close, 10)) / 10) - ((ts_delay(close, 10) - close) / 10)) < (-1 * 0.1)) ? 1 : ((-1 * 1) * (close - ts_delay(close, 1))))

    factor = (diff_normalized < neg_01).astype(int).where(lambda x: x != 0, neg_close_diff)
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()