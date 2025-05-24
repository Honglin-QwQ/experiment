import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_min_diff, multiply

def factor_5915(data, **kwargs):
    """
    因子名称: VolWeightedMinDiffRatio_64974
    数学表达式: divide(ts_min_diff(open * vol, 48), ts_min_diff(close * vol, 77))
    中文描述: 该因子是参考因子的创新性改进，将开盘价和收盘价分别与各自的成交量相乘，计算过去48天成交量加权开盘价与该期间最低成交量加权开盘价差值，与过去77天成交量加权收盘价与该期间最低成交量加权收盘价差值的比值。通过引入成交量加权，该因子创新性地反映了不同交易时段价格变化的市场认可程度，成交量越大，价格变化对因子的影响越大。较高的值可能表明开盘阶段的成交量加权价格相对于其历史低点更强势，而收盘阶段相对较弱，反之亦然。这有助于捕捉市场情绪在不同交易时段的差异，并可能提供更具市场基础的交易信号。
    因子应用场景：
    1. 市场情绪分析：用于捕捉市场情绪在开盘和收盘阶段的差异。
    2. 交易信号：提供基于成交量加权价格变化的交易信号。
    """
    # 1. 计算 open * vol
    open_vol = multiply(data['open'], data['vol'])
    # 2. 计算 ts_min_diff(open * vol, 48)
    ts_min_diff_open_vol = ts_min_diff(open_vol, d=48)
    # 3. 计算 close * vol
    close_vol = multiply(data['close'], data['vol'])
    # 4. 计算 ts_min_diff(close * vol, 77)
    ts_min_diff_close_vol = ts_min_diff(close_vol, d=77)
    # 5. 计算 divide(ts_min_diff(open * vol, 48), ts_min_diff(close * vol, 77))
    factor = divide(ts_min_diff_open_vol, ts_min_diff_close_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()