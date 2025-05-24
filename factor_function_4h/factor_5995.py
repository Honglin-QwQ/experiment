import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import rank
from operators import ts_decay_exp_window
from operators import divide
from operators import ts_std_dev

def factor_5995(data, **kwargs):
    """
    数学表达式: rank(ts_decay_exp_window(divide(vol, ts_std_dev(close, 10)), 15, factor=0.7))
    中文描述: 该因子计算成交量与过去10天收盘价标准差比值的15天指数衰减加权平均，并对该平均值进行排名。相较于参考因子直接计算相关性，本因子创新性地计算了成交量与价格波动性的比值，并使用指数衰减加权平均来更强调近期数据的影响。高排名表示近期成交量相对于价格波动性较高，且这种趋势在近期更为显著，可能预示着市场对当前价格波动表现出更强的交易活动。这结合了参考因子中对成交量、时间序列标准差和排名的使用，但通过引入比值和指数衰减加权平均，旨在捕捉量价关系中更具动态性和近期偏向的信号。因子值越高，可能表明该股票在近期波动中伴随的交易强度更高，适合关注近期市场活跃度较高的股票。
    因子应用场景：
    1. 量价关系分析：用于识别成交量相对于价格波动性较高的股票，可能预示着市场对当前价格波动表现出更强的交易活动。
    2. 市场活跃度监控：因子值越高，可能表明该股票在近期波动中伴随的交易强度更高，适合关注近期市场活跃度较高的股票。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], 10)
    # 2. 计算 divide(vol, ts_std_dev(close, 10))
    data_divide = divide(data['vol'], data_ts_std_dev)
    # 3. 计算 ts_decay_exp_window(divide(vol, ts_std_dev(close, 10)), 15, factor=0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_divide, 15, factor=0.7)
    # 4. 计算 rank(ts_decay_exp_window(divide(vol, ts_std_dev(close, 10)), 15, factor=0.7))
    factor = rank(data_ts_decay_exp_window, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()