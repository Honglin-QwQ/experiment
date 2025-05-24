import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_arg_min

def factor_5770(data, **kwargs):
    """
    因子名称: ts_arg_min_close_vol_ratio_68737
    数学表达式: ts_arg_min(divide(close, vol), 14)
    中文描述: 该因子计算过去14天内收盘价与成交量比率的最低点出现的天数。收盘价与成交量的比率可以视为反映单位交易量所对应的价格水平。该因子通过识别这个比率的最低点，旨在发现市场在过去两周内单位交易成本最低的时点。这可能预示着潜在的买入机会，因为低比率可能意味着在较低价格水平上发生了相对较高的交易量，或者在特定价格水平上交易量相对较低，这两种情况都可能提供独特的交易信号。相较于参考因子，该因子创新性地结合了价格和成交量信息，并利用ts_arg_min运算符来捕捉极值出现的时间位置，而不是简单的价格或成交量的极值位置或排名。
    因子应用场景：
    1. 寻找潜在买入机会：当因子值较小时，可能意味着在较低价格水平上发生了相对较高的交易量，预示着潜在的买入机会。
    2. 交易成本分析：通过识别单位交易成本最低的时点，辅助分析市场交易成本的变动趋势。
    """
    # 1. 计算 divide(close, vol)
    data_divide = divide(data['close'], data['vol'])
    # 2. 计算 ts_arg_min(divide(close, vol), 14)
    factor = ts_arg_min(data_divide, d = 14)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()