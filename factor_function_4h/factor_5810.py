import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import inverse, ts_rank, divide, subtract, add, ts_std_dev

def factor_5810(data, **kwargs):
    """
    数学表达式: inverse(ts_rank(divide(subtract(tbase, tquote), add(tbase, tquote)), 30) * ts_std_dev(divide(tbase, add(tbase, tquote)), 15))
    中文描述: 该因子旨在衡量主动买卖净流量的长期相对强度的倒数，并结合买盘压力的短期波动性。首先，计算主动买入基础币种数量与主动买入计价币种数量（代表主动卖出）之差占主动买卖总量的比例，衡量净买卖流量，并计算其在过去30天内的排名，反映净买卖流量的长期相对强度。然后，计算主动买入基础币种数量占主动买卖总量的比例，并计算其在过去15天内的标准差，捕捉买盘压力的短期波动。将净买卖流量排名的倒数与买盘压力波动性相乘。相较于参考因子，创新点在于对净买卖流量排名取了倒数，并调整了时间窗口，将ts_rank的时间窗口调整为更长的30天，以捕捉更长期的趋势，同时将ts_std_dev的时间窗口调整为15天，以捕捉适度的短期波动。这种组合可能有助于识别那些在长期来看净买卖流量相对较弱（排名较低，倒数较高）但短期买盘压力波动较大的股票，可能预示着潜在的反转机会。
    因子应用场景：
    1. 反转机会识别：该因子可能用于识别那些在长期来看净买卖流量相对较弱，但短期买盘压力波动较大的股票，可能预示着潜在的反转机会。
    2. 量化交易：在量化交易策略中，该因子可以作为一个信号，用于筛选具有潜在反转机会的股票。
    """
    # 1. 计算 subtract(tbase, tquote)
    data_subtract = subtract(data['tbase'], data['tquote'])
    # 2. 计算 add(tbase, tquote)
    data_add = add(data['tbase'], data['tquote'])
    # 3. 计算 divide(subtract(tbase, tquote), add(tbase, tquote))
    data_divide_1 = divide(data_subtract, data_add)
    # 4. 计算 ts_rank(divide(subtract(tbase, tquote), add(tbase, tquote)), 30)
    data_ts_rank = ts_rank(data_divide_1, d=30)
    # 5. 计算 divide(tbase, add(tbase, tquote))
    data_divide_2 = divide(data['tbase'], data_add)
    # 6. 计算 ts_std_dev(divide(tbase, add(tbase, tquote)), 15)
    data_ts_std_dev = ts_std_dev(data_divide_2, d=15)
    # 7. 计算 ts_rank(divide(subtract(tbase, tquote), add(tbase, tquote)), 30) * ts_std_dev(divide(tbase, add(tbase, tquote)), 15)
    factor_temp = data_ts_rank * data_ts_std_dev
    # 8. 计算 inverse(ts_rank(divide(subtract(tbase, tquote), add(tbase, tquote)), 30) * ts_std_dev(divide(tbase, add(tbase, tquote)), 15))
    factor = inverse(factor_temp)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()