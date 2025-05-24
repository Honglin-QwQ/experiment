import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import divide
from operators import ts_decay_linear
from operators import ts_rank

def factor_5761(data, **kwargs):
    """
    因子名称: High_Low_Rank_Ratio_Decay_31355
    数学表达式: divide(ts_decay_linear(ts_rank(high, 10), 5), ts_decay_linear(ts_rank(low, 10), 5))
    中文描述: 该因子计算过去10天最高价排名的5天线性衰减平均值与过去10天最低价排名的5天线性衰减平均值之比。它结合了时间序列排名和线性衰减的概念，旨在捕捉近期高价和低价相对强度的动态变化。当比值较高时，可能表明近期价格倾向于在高位，显示出上涨动能；反之，比值较低可能表明近期价格倾向于在低位，显示出下行压力。这可以帮助投资者识别短期价格趋势的持续性或潜在反转。
    因子应用场景：
    1. 趋势识别：用于识别价格趋势，比值较高可能预示上涨趋势，比值较低可能预示下跌趋势。
    2. 动量分析：捕捉高价和低价的相对强度，辅助判断市场动量。
    3. 反转信号：当比值极端时，可能暗示趋势反转的可能性。
    """
    # 1. 计算 ts_rank(high, 10)
    data_ts_rank_high = ts_rank(data['high'], d = 10)
    # 2. 计算 ts_decay_linear(ts_rank(high, 10), 5)
    data_ts_decay_linear_high = ts_decay_linear(data_ts_rank_high, d = 5)
    # 3. 计算 ts_rank(low, 10)
    data_ts_rank_low = ts_rank(data['low'], d = 10)
    # 4. 计算 ts_decay_linear(ts_rank(low, 10), 5)
    data_ts_decay_linear_low = ts_decay_linear(data_ts_rank_low, d = 5)
    # 5. 计算 divide(ts_decay_linear(ts_rank(high, 10), 5), ts_decay_linear(ts_rank(low, 10), 5))
    factor = divide(data_ts_decay_linear_high, data_ts_decay_linear_low)

    # 删除中间变量
    del data_ts_rank_high
    del data_ts_decay_linear_high
    del data_ts_rank_low
    del data_ts_decay_linear_low

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()