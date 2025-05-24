import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, floor, ts_decay_linear, rank

def factor_6095(data, **kwargs):
    """
    因子名称: VolFloorRatio_DecayRank_86773
    数学表达式: rank(ts_decay_linear(divide(vol, floor(vol)), 15))
    中文描述: 该因子计算每日成交量与其向下取整值的比率，并对该比率进行15天的线性衰减，最后对衰减后的结果进行横截面排名。成交量与其向下取整值的比率可以放大成交量小数部分的影响，可能反映市场在关键整数成交量附近的交易行为。通过线性衰减和排名，因子捕捉了近期成交量特性的相对强度和持续性，可能用于识别成交量结构发生变化的股票。
    因子应用场景：
    1. 成交量分析：用于识别成交量与其整数部分差异较大的股票，可能表明市场对该股票的交易兴趣集中在特定价格水平。
    2. 趋势跟踪：通过线性衰减和排名，可以捕捉成交量变化的趋势，用于辅助判断股票价格走势。
    """
    # 1. 计算 floor(vol)
    data_floor_vol = floor(data['vol'])
    # 2. 计算 divide(vol, floor(vol))
    data_divide = divide(data['vol'], data_floor_vol)
    # 3. 计算 ts_decay_linear(divide(vol, floor(vol)), 15)
    data_ts_decay_linear = ts_decay_linear(data_divide, 15)
    # 4. 计算 rank(ts_decay_linear(divide(vol, floor(vol)), 15))
    factor = rank(data_ts_decay_linear, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()