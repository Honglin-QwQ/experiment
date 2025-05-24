import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_delta, ts_arg_max, ts_corr, multiply

def factor_5678(data, **kwargs):
    """
    因子名称: factor_0001_81736
    数学表达式: ts_rank(ts_delta(close, 1), 5) * ts_arg_max(ts_corr(close, vol, 10), 15)
    中文描述: 该因子结合了短期价格变化趋势和中期价量相关性。首先，ts_rank(ts_delta(close, 1), 5)计算了过去5天内每日收盘价变化（今日收盘价与昨日收盘价之差）的排名，捕捉了短期价格动量。然后，ts_arg_max(ts_corr(close, vol, 10), 15)计算了过去15天内，收盘价和成交量在过去10天相关性达到最大值的位置。该因子将这两个部分相乘，旨在识别出短期价格上涨动量与中期价量关系达到峰值的时机。创新之处在于结合了价格变化的速度和价量相关性的时间位置，可能用于识别趋势反转或加速的节点。
    因子应用场景：
    1. 趋势反转识别：该因子可能用于识别趋势反转的时机，当短期价格上涨动量与中期价量关系达到峰值时，可能预示着趋势即将发生变化。
    2. 趋势加速识别：该因子也可能用于识别趋势加速的时机，当短期价格上涨动量与中期价量关系达到峰值时，可能意味着当前趋势将进一步加强。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 2. 计算 ts_rank(ts_delta(close, 1), 5)
    data_ts_rank = ts_rank(data_ts_delta_close, 5)
    # 3. 计算 ts_corr(close, vol, 10)
    data_ts_corr = ts_corr(data['close'], data['vol'], 10)
    # 4. 计算 ts_arg_max(ts_corr(close, vol, 10), 15)
    data_ts_arg_max = ts_arg_max(data_ts_corr, 15)
    # 5. 计算 ts_rank(ts_delta(close, 1), 5) * ts_arg_max(ts_corr(close, vol, 10), 15)
    factor = multiply(data_ts_rank, data_ts_arg_max)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()