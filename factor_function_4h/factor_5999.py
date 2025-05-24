import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_decay_linear, ts_std_dev, divide

def factor_5999(data, **kwargs):
    """
    因子名称: Volume_Rank_Decay_Volatility_Ratio_16148
    数学表达式: divide(ts_rank(ts_decay_linear(volume, 30), 40), ts_std_dev(volume, 30))
    中文描述: 该因子计算过去30天成交量线性衰减加权平均值在过去40天内的排名与过去30天成交量标准差的比值。在参考因子基础上，将简单平均成交量替换为线性衰减加权平均成交量，以更强调近期成交量信息，并调整了排名和标准差的计算窗口期。高排名和低波动性可能表明近期成交量稳定且相对较高，而低排名和高波动性可能指示近期成交量不稳定且相对较低。这个因子可以用于识别近期具有稳定高交易活跃度的股票，或者捕捉近期交易量异常波动的信号，相较于简单平均更能捕捉短期市场情绪变化。
    因子应用场景：
    1. 识别近期具有稳定高交易活跃度的股票。
    2. 捕捉近期交易量异常波动的信号。
    """
    # 1. 计算 ts_decay_linear(volume, 30)
    data_ts_decay_linear = ts_decay_linear(data['vol'], 30)
    # 2. 计算 ts_rank(ts_decay_linear(volume, 30), 40)
    data_ts_rank = ts_rank(data_ts_decay_linear, 40)
    # 3. 计算 ts_std_dev(volume, 30)
    data_ts_std_dev = ts_std_dev(data['vol'], 30)
    # 4. 计算 divide(ts_rank(ts_decay_linear(volume, 30), 40), ts_std_dev(volume, 30))
    factor = divide(data_ts_rank, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()