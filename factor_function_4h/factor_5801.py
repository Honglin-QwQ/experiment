import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, divide, add, ts_rank, subtract, multiply

def factor_5801(data, **kwargs):
    """
    因子名称: VolatilityAdjustedBuyPressureFlow_70727
    数学表达式: multiply(ts_std_dev(divide(tbase, add(tbase, tquote)), 10), ts_rank(divide(subtract(tbase, tquote), add(tbase, tquote)), 20))
    中文描述: 该因子旨在衡量主动买入与卖出力量的短期波动性以及主动买卖净流量的长期相对强度。首先，计算主动买入基础币种数量占主动买卖总量的比例，并计算其在过去10天内的标准差，捕捉买盘压力的短期波动。然后，计算主动买入基础币种数量与主动买入计价币种数量（代表主动卖出）之差占主动买卖总量的比例，衡量净买卖流量，并计算其在过去20天内的排名，反映净买卖流量的长期相对强度。最后，将这两个指标相乘。该因子结合了买盘压力的波动性和净买卖流量的相对强度，旨在识别那些在买盘压力波动较大且净买卖流量有较高排名的股票，可能预示着潜在的价格上涨动能。相较于参考因子，创新点在于使用了主动买卖总量作为分母，更准确地衡量了买卖力量的相对比例，并引入了净买卖流量的概念，同时调整了时间窗口和排名计算的指标，并根据改进建议，将ts_rank的时间窗口调整为更长的20天，以捕捉更长期的趋势。
    因子应用场景：
    1. 识别买盘压力波动较大且净买卖流量排名较高的股票。
    2. 辅助判断潜在的价格上涨动能。
    """

    # 1. 计算 divide(tbase, add(tbase, tquote))
    data_add = add(data['tbase'], data['tquote'])
    data_divide1 = divide(data['tbase'], data_add)

    # 2. 计算 ts_std_dev(divide(tbase, add(tbase, tquote)), 10)
    data_ts_std_dev = ts_std_dev(data_divide1, d = 10)

    # 3. 计算 subtract(tbase, tquote)
    data_subtract = subtract(data['tbase'], data['tquote'])

    # 4. 计算 divide(subtract(tbase, tquote), add(tbase, tquote))
    data_divide2 = divide(data_subtract, data_add)

    # 5. 计算 ts_rank(divide(subtract(tbase, tquote), add(tbase, tquote)), 20)
    data_ts_rank = ts_rank(data_divide2, d = 20)

    # 6. 计算 multiply(ts_std_dev(divide(tbase, add(tbase, tquote)), 10), ts_rank(divide(subtract(tbase, tquote), add(tbase, tquote)), 20))
    factor = multiply(data_ts_std_dev, data_ts_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()