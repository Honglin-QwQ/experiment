import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import scale, divide, ts_std_dev, log, abs, subtract, ts_delay

def factor_6023(data, **kwargs):
    """
    数学表达式: scale(divide(ts_std_dev(log(vol), 30), abs(subtract(close, ts_delay(close, 1)))))
    中文描述: 该因子计算过去30天交易量对数标准差与当日收盘价相对于前一日收盘价的绝对差值的比值，并进行截面标准化。它旨在捕捉交易量波动与价格跳跃之间的关系。相较于参考因子，本因子缩短了交易量波动率的计算周期，并简化了价格变动幅度的衡量方式，使用收盘价的绝对差值来衡量价格跳跃。因子值越高，可能表明交易量波动相对于价格跳跃更为剧烈，这可能预示着市场情绪的潜在变化或趋势的强度。
    因子应用场景：
    1. 市场情绪分析：用于识别交易量波动相对于价格跳跃更为剧烈的股票，可能预示着市场情绪的潜在变化。
    2. 趋势强度判断：用于辅助判断当前趋势的强度，因子值越高可能表明趋势越强。
    """
    # 1. 计算 log(vol)
    data_log_vol = log(data['vol'])
    # 2. 计算 ts_std_dev(log(vol), 30)
    data_ts_std_dev = ts_std_dev(data_log_vol, 30)
    # 3. 计算 ts_delay(close, 1)
    data_ts_delay_close = ts_delay(data['close'], 1)
    # 4. 计算 subtract(close, ts_delay(close, 1))
    data_subtract = subtract(data['close'], data_ts_delay_close)
    # 5. 计算 abs(subtract(close, ts_delay(close, 1)))
    data_abs_subtract = abs(data_subtract)
    # 6. 计算 divide(ts_std_dev(log(vol), 30), abs(subtract(close, ts_delay(close, 1))))
    data_divide = divide(data_ts_std_dev, data_abs_subtract)
    # 7. 计算 scale(divide(ts_std_dev(log(vol), 30), abs(subtract(close, ts_delay(close, 1)))))
    factor = scale(data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()