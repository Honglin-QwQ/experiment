import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import multiply, ts_rank, divide, subtract, add, ts_std_dev

def factor_5925(data, **kwargs):
    """
    因子名称: VolatilityAdjustedVolumeFlow_61178
    数学表达式: multiply(ts_rank(divide(subtract(tbase, tquote), add(tbase, tquote)), 10), divide(volume, ts_std_dev(close, 20)))
    中文描述: 该因子旨在衡量在考虑价格波动性的情况下，主动买卖力量的相对强度。它首先计算主动买入量和主动卖出量（通过tbase和tquote的差值与总和的比值来近似）在过去10天内的排名，以捕捉近期资金流动的相对趋势。然后，将当前成交量除以过去20天收盘价的标准差，用以衡量成交量相对于价格波动性的强度。最后，将资金流排名的结果与成交量波动性调整项相乘。相较于参考因子，创新点在于引入了主动买卖量（tbase和tquote）来更精细地衡量资金流，并结合了收盘价的波动性来调整成交量的影响，使得因子更能反映在不同市场波动环境下的量价关系。该因子可用于识别在特定波动水平下，具有较强资金流入且成交活跃的股票。
    因子应用场景：
    1. 识别在特定波动水平下，具有较强资金流入且成交活跃的股票。
    2. 量化主动买卖力量的相对强度。
    3. 辅助判断股票的买卖时机。
    """
    # 1. 计算 subtract(tbase, tquote)
    data_subtract = subtract(data['tbase'], data['tquote'])
    # 2. 计算 add(tbase, tquote)
    data_add = add(data['tbase'], data['tquote'])
    # 3. 计算 divide(subtract(tbase, tquote), add(tbase, tquote))
    data_divide_1 = divide(data_subtract, data_add)
    # 4. 计算 ts_rank(divide(subtract(tbase, tquote), add(tbase, tquote)), 10)
    data_ts_rank = ts_rank(data_divide_1, d = 10)
    # 5. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], d = 20)
    # 6. 计算 divide(volume, ts_std_dev(close, 20))
    data_divide_2 = divide(data['vol'], data_ts_std_dev)
    # 7. 计算 multiply(ts_rank(divide(subtract(tbase, tquote), add(tbase, tquote)), 10), divide(volume, ts_std_dev(close, 20)))
    factor = multiply(data_ts_rank, data_divide_2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()