import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, divide, abs, subtract, add

def factor_6048(data, **kwargs):
    """
    数学表达式: divide(ts_rank(vol, 87), abs(subtract(divide(add(high, low), 2), close)))
    中文描述: 该因子结合了成交量的时间序列排名与日内价格波动范围，通过计算成交量在过去87天的排名与高低价均值减去收盘价的绝对值的比值。成交量排名反映了当前交易量在历史上的相对活跃度，高低价均值减收盘价的绝对值则衡量了日内价格的波动幅度或收盘价相对于日内中轴的偏离程度。将这两者结合，旨在捕捉在不同交易活跃度和日内价格结构下，市场力量的相对强弱。高因子值可能表示在相对活跃的交易环境下，收盘价显著偏离日内中轴，预示着潜在的价格动量或反转机会。创新点在于将时间序列排名与日内价格结构相结合，形成一个新的衡量市场力量的指标。
    因子应用场景：
    1. 交易活跃度与价格偏离度量：用于识别交易活跃且收盘价偏离日内价格中枢的股票。
    2. 潜在动量或反转信号：高因子值可能预示着价格动量或反转的机会。
    """
    # 1. 计算 ts_rank(vol, 87)
    data_ts_rank_vol = ts_rank(data['vol'], 87)
    # 2. 计算 add(high, low)
    data_add_high_low = add(data['high'], data['low'])
    # 3. 计算 divide(add(high, low), 2)
    data_divide_add_high_low = divide(data_add_high_low, 2)
    # 4. 计算 subtract(divide(add(high, low), 2), close)
    data_subtract_divide_add_high_low_close = subtract(data_divide_add_high_low, data['close'])
    # 5. 计算 abs(subtract(divide(add(high, low), 2), close))
    data_abs_subtract_divide_add_high_low_close = abs(data_subtract_divide_add_high_low_close)
    # 6. 计算 divide(ts_rank(vol, 87), abs(subtract(divide(add(high, low), 2), close)))
    factor = divide(data_ts_rank_vol, data_abs_subtract_divide_add_high_low_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()