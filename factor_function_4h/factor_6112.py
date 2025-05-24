import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_rank, multiply, subtract, ts_delay, ts_sum, max, abs, ts_std_dev

def factor_6112(data, **kwargs):
    """
    因子名称: VolatilityMomentumATRRatio_61313
    数学表达式: divide(ts_rank(multiply(subtract(divide(close, ts_delay(close, 20)), 1), ts_sum(max(subtract(high, low), abs(subtract(high, ts_delay(close, 1))), abs(subtract(low, ts_delay(close, 1)))), 14)), 10), ts_rank(ts_std_dev(open, 90), 20))
    中文描述: 该因子旨在捕捉结合价格动量和真实波动幅度的短期市场动态与中长期开盘价波动性的相对关系。它首先计算过去20天的价格动量（当前收盘价相对于20天前收盘价的变化率），然后计算14天的平均真实范围（ATR），并将动量与ATR相乘。这个乘积代表了考虑了真实波动幅度的价格趋势强度。接着，计算这个乘积的10日时间序列排名，以衡量短期趋势和波动结合强度的相对位置。同时，计算过去90天开盘价标准差的20日时间序列排名，以衡量中长期开盘价波动性的相对稳定性。最后，将短期动量-ATR乘积的排名除以中长期开盘价标准差的排名。较高的比值可能表明近期市场在考虑真实波动的情况下具有较强的趋势，而中长期开盘价波动相对稳定，这可能预示着市场情绪的变化或潜在的交易机会。相较于参考因子，该因子创新性地引入了价格动量和ATR，更全面地衡量了短期市场动态，并通过比值的方式比较了不同时间窗口和不同指标（动量/ATR与标准差）的相对排名，以期发现更复杂的市场结构和交易信号。同时，该因子利用了改进建议中提到的结合价格趋势和更稳健的波动率计算方法（ATR）的思想。
    因子应用场景：
    1. 趋势识别：当因子值较高时，可能表明近期市场在考虑真实波动的情况下具有较强的趋势，而中长期开盘价波动相对稳定。
    2. 波动性分析：通过比较短期动量-ATR乘积的排名与中长期开盘价标准差的排名，可以分析市场波动性的结构性变化。
    3. 交易信号：该因子可能用于识别潜在的交易机会，尤其是在较高比值出现时，可能预示着市场情绪的变化。
    """

    # 1. 计算 divide(close, ts_delay(close, 20))
    data_ts_delay_close = ts_delay(data['close'], 20)
    data_divide_close_ts_delay_close = divide(data['close'], data_ts_delay_close)

    # 2. 计算 subtract(divide(close, ts_delay(close, 20)), 1)
    data_subtract_divide_ts_delay = subtract(data_divide_close_ts_delay_close, 1)

    # 3. 计算 subtract(high, low)
    data_subtract_high_low = subtract(data['high'], data['low'])

    # 4. 计算 ts_delay(close, 1)
    data_ts_delay_close_1 = ts_delay(data['close'], 1)

    # 5. 计算 subtract(high, ts_delay(close, 1))
    data_subtract_high_ts_delay_close_1 = subtract(data['high'], data_ts_delay_close_1)

    # 6. 计算 abs(subtract(high, ts_delay(close, 1)))
    data_abs_subtract_high_ts_delay_close_1 = abs(data_subtract_high_ts_delay_close_1)

    # 7. 计算 subtract(low, ts_delay(close, 1))
    data_subtract_low_ts_delay_close_1 = subtract(data['low'], data_ts_delay_close_1)

    # 8. 计算 abs(subtract(low, ts_delay(close, 1)))
    data_abs_subtract_low_ts_delay_close_1 = abs(data_subtract_low_ts_delay_close_1)

    # 9. 计算 max(subtract(high, low), abs(subtract(high, ts_delay(close, 1))), abs(subtract(low, ts_delay(close, 1))))
    data_max_atr = max(data_subtract_high_low, data_abs_subtract_high_ts_delay_close_1, data_abs_subtract_low_ts_delay_close_1)

    # 10. 计算 ts_sum(max(subtract(high, low), abs(subtract(high, ts_delay(close, 1))), abs(subtract(low, ts_delay(close, 1)))), 14)
    data_ts_sum_max_atr = ts_sum(data_max_atr, 14)

    # 11. 计算 multiply(subtract(divide(close, ts_delay(close, 20)), 1), ts_sum(max(subtract(high, low), abs(subtract(high, ts_delay(close, 1))), abs(subtract(low, ts_delay(close, 1)))), 14))
    data_multiply_momentum_atr = multiply(data_subtract_divide_ts_delay, data_ts_sum_max_atr)

    # 12. 计算 ts_rank(multiply(subtract(divide(close, ts_delay(close, 20)), 1), ts_sum(max(subtract(high, low), abs(subtract(high, ts_delay(close, 1))), abs(subtract(low, ts_delay(close, 1)))), 14)), 10)
    data_ts_rank_momentum_atr = ts_rank(data_multiply_momentum_atr, 10)

    # 13. 计算 ts_std_dev(open, 90)
    data_ts_std_dev_open = ts_std_dev(data['open'], 90)

    # 14. 计算 ts_rank(ts_std_dev(open, 90), 20)
    data_ts_rank_std_dev_open = ts_rank(data_ts_std_dev_open, 20)

    # 15. 计算 divide(ts_rank(multiply(subtract(divide(close, ts_delay(close, 20)), 1), ts_sum(max(subtract(high, low), abs(subtract(high, ts_delay(close, 1))), abs(subtract(low, ts_delay(close, 1)))), 14)), 10), ts_rank(ts_std_dev(open, 90), 20))
    factor = divide(data_ts_rank_momentum_atr, data_ts_rank_std_dev_open)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()