import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, max, abs, ts_delay, ts_mean

def factor_5651(data, **kwargs):
    """
    因子名称: DynamicVolatilityRatio_34296
    数学表达式: divide(ts_std_dev(max(abs(high - ts_delay(close, 1)), abs(low - ts_delay(close, 1))), 5), ts_mean(high - low, 20))
    中文描述: 该因子计算了短期波动率与长期波动率的比率。分子是过去5天内每日最高价与前一日收盘价之差的绝对值，以及每日最低价与前一日收盘价之差的绝对值，取最大值后的标准差，代表短期价格跳跃风险；分母是过去20天内每日最高价与最低价之差的均值，代表长期价格波动幅度。该因子旨在衡量短期价格波动相对于长期价格波动的程度，可以用于识别市场情绪的短期变化。当比率较高时，可能表明市场短期波动较大，存在潜在的交易机会。
    因子应用场景：
    1. 衡量短期价格波动相对于长期价格波动的程度。
    2. 识别市场情绪的短期变化。
    3. 识别市场短期波动较大的潜在交易机会。
    """
    # 1. 计算 ts_delay(close, 1)
    data_ts_delay_close = ts_delay(data['close'], 1)
    # 2. 计算 abs(high - ts_delay(close, 1))
    data_abs_high_diff = abs(data['high'] - data_ts_delay_close)
    # 3. 计算 abs(low - ts_delay(close, 1))
    data_abs_low_diff = abs(data['low'] - data_ts_delay_close)
    # 4. 计算 max(abs(high - ts_delay(close, 1)), abs(low - ts_delay(close, 1)))
    data_max_abs_diff = max(data_abs_high_diff, data_abs_low_diff)
    # 5. 计算 ts_std_dev(max(abs(high - ts_delay(close, 1)), abs(low - ts_delay(close, 1))), 5)
    data_ts_std_dev = ts_std_dev(data_max_abs_diff, 5)
    # 6. 计算 high - low
    data_high_low_diff = data['high'] - data['low']
    # 7. 计算 ts_mean(high - low, 20)
    data_ts_mean = ts_mean(data_high_low_diff, 20)
    # 8. 计算 divide(ts_std_dev(max(abs(high - ts_delay(close, 1)), abs(low - ts_delay(close, 1))), 5), ts_mean(high - low, 20))
    factor = divide(data_ts_std_dev, data_ts_mean)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()