import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_rank, divide, ts_delay

def factor_5589(data, **kwargs):
    """
    因子名称: factor_0001_21489
    数学表达式: ts_delta(ts_rank(divide(close,ts_delay(low,222)),d=10),2)
    中文描述: 该因子结合了收盘价与222天前最低价的比率的时间序列排名变化。首先，计算收盘价与222天前最低价的比率，然后计算该比率在过去10天内的排名，最后计算该排名在2天内的变化。该因子旨在捕捉长期低点支撑下的短期价格动量变化，可用于识别潜在的反转或趋势延续信号。
    因子应用场景：
    1. 反转信号：当因子值显著增加时，可能表明价格从长期低点反弹，形成潜在的反转信号。
    2. 趋势延续：在上升趋势中，因子值的小幅波动可能表明趋势的稳定延续。
    """
    # 1. 计算 ts_delay(low, 222)
    data_ts_delay_low = ts_delay(data['low'], d=222)
    # 2. 计算 divide(close, ts_delay(low, 222))
    data_divide = divide(data['close'], data_ts_delay_low)
    # 3. 计算 ts_rank(divide(close, ts_delay(low, 222)), d=10)
    data_ts_rank = ts_rank(data_divide, d=10)
    # 4. 计算 ts_delta(ts_rank(divide(close, ts_delay(low, 222)), d=10), 2)
    factor = ts_delta(data_ts_rank, d=2)

    # 删除中间变量
    del data_ts_delay_low
    del data_divide
    del data_ts_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()