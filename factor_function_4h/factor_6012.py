import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import scale, divide, ts_std_dev, log, max, subtract, abs, ts_delay

def factor_6012(data, **kwargs):
    """
    因子名称: Vol_ATR_Ratio_Scaled_35402
    数学表达式: scale(divide(ts_std_dev(log(vol), 20), max(subtract(high, low), abs(subtract(high, ts_delay(close, 1))), abs(subtract(low, ts_delay(close, 1))))))
    中文描述: 该因子计算过去20天交易量对数标准差与真实波幅（ATR）的比值，并进行截面标准化。真实波幅（ATR）是最高价与最低价之差、当前最高价与前一日收盘价绝对差、当前最低价与前一日收盘价绝对差三者中的最大值。该因子旨在捕捉交易量波动与价格波动之间的关系。因子值越高，可能表明交易量波动相对于价格波动更为剧烈，这可能预示着市场情绪的潜在变化或趋势的强度。相较于参考因子，本因子用更具鲁棒性的真实波幅（ATR）替代了最高价与其地板值乘积的差分，并缩短了成交量波动率的计算周期，同时加入了截面标准化操作以提高因子的可比性。
    因子应用场景：
    1. 交易量波动分析：用于识别交易量波动相对于价格波动更为剧烈的股票，可能预示着市场情绪的潜在变化或趋势的强度。
    2. 市场情绪监测：通过量价关系的变化，辅助判断市场情绪。
    """
    # 1. 计算 log(vol)
    data_log_vol = log(data['vol'])
    # 2. 计算 ts_std_dev(log(vol), 20)
    data_ts_std_dev = ts_std_dev(data_log_vol, 20)
    # 3. 计算 subtract(high, low)
    data_subtract_high_low = subtract(data['high'], data['low'])
    # 4. 计算 ts_delay(close, 1)
    data_ts_delay_close = ts_delay(data['close'], 1)
    # 5. 计算 subtract(high, ts_delay(close, 1))
    data_subtract_high_ts_delay_close = subtract(data['high'], data_ts_delay_close)
    # 6. 计算 abs(subtract(high, ts_delay(close, 1)))
    data_abs_subtract_high_ts_delay_close = abs(data_subtract_high_ts_delay_close)
    # 7. 计算 subtract(low, ts_delay(close, 1))
    data_subtract_low_ts_delay_close = subtract(data['low'], data_ts_delay_close)
    # 8. 计算 abs(subtract(low, ts_delay(close, 1)))
    data_abs_subtract_low_ts_delay_close = abs(data_subtract_low_ts_delay_close)
    # 9. 计算 max(subtract(high, low), abs(subtract(high, ts_delay(close, 1))), abs(subtract(low, ts_delay(close, 1))))
    data_max = max(data_subtract_high_low, data_abs_subtract_high_ts_delay_close, data_abs_subtract_low_ts_delay_close)
    # 10. 计算 divide(ts_std_dev(log(vol), 20), max(subtract(high, low), abs(subtract(high, ts_delay(close, 1))), abs(subtract(low, ts_delay(close, 1)))))
    data_divide = divide(data_ts_std_dev, data_max)
    # 11. 计算 scale(divide(ts_std_dev(log(vol), 20), max(subtract(high, low), abs(subtract(high, ts_delay(close, 1))), abs(subtract(low, ts_delay(close, 1)))))
    factor = scale(data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()