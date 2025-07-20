import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delay, subtract, divide, multiply

def factor_0045(data, **kwargs):
    """
    数学表达式: ((0.25 < (((ts_delay(close, 20) - ts_delay(close, 10)) / 10) - ((ts_delay(close, 10) - close) / 10))) ? (-1 * 1) : (((((ts_delay(close, 20) - ts_delay(close, 10)) / 10) - ((ts_delay(close, 10) - close) / 10)) < 0) ? 1 : ((-1 * 1) * (close - ts_delay(close, 1)))))
    中文描述: 该因子衡量了股价短期动量变化趋势。首先计算过去20天到过去10天股价变化的十分之一，再减去过去10天到当前股价变化的十分之一，如果这个差值大于0.25，则因子值为-1；否则，如果这个差值小于0，则因子值为1；如果上述两个条件都不满足，则因子值为当前收盘价与前一天收盘价之差的-1倍。
    因子应用场景：
    1. 可以作为趋势反转策略的信号，当因子值为-1时，可能预示着股价上涨趋势减缓或即将反转；当因子值为1时，可能预示着股价下跌趋势减缓或即将反转。
    2. 可以与其他动量因子结合使用，提高预测准确性。
    3. 可以用于构建高频交易策略，捕捉短期价格波动。
    """
    # 计算 ts_delay(close, 20)
    ts_delay_close_20 = ts_delay(data['close'], d=20)
    # 计算 ts_delay(close, 10)
    ts_delay_close_10 = ts_delay(data['close'], d=10)

    # 计算 (ts_delay(close, 20) - ts_delay(close, 10))
    sub_1 = subtract(ts_delay_close_20, ts_delay_close_10)
    # 计算 (ts_delay(close, 20) - ts_delay(close, 10)) / 10
    div_1 = divide(sub_1, 10)

    # 计算 (ts_delay(close, 10) - close)
    sub_2 = subtract(ts_delay_close_10, data['close'])
    # 计算 (ts_delay(close, 10) - close) / 10
    div_2 = divide(sub_2, 10)

    # 计算 ((ts_delay(close, 20) - ts_delay(close, 10)) / 10) - ((ts_delay(close, 10) - close) / 10)
    diff = subtract(div_1, div_2)

    # 计算 0.25 < (((ts_delay(close, 20) - ts_delay(close, 10)) / 10) - ((ts_delay(close, 10) - close) / 10))
    condition_1 = diff > 0.25

    # 计算 ((((ts_delay(close, 20) - ts_delay(close, 10)) / 10) - ((ts_delay(close, 10) - close) / 10)) < 0)
    condition_2 = diff < 0

    # 计算 -1 * 1
    value_1 = multiply(-1, 1)

    # 计算 close - ts_delay(close, 1)
    close_delay = ts_delay(data['close'], d=1)
    sub_3 = subtract(data['close'], close_delay)

    # 计算 (-1 * 1) * (close - ts_delay(close, 1))
    value_3 = multiply(value_1, sub_3)

    # 根据条件赋值
    factor = data['close'].copy()  # 初始化factor，避免出现未赋值的情况
    factor[condition_1] = value_1
    factor[~condition_1 & condition_2] = 1
    factor[~(condition_1 | condition_2)] = value_3

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()