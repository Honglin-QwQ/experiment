import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import scale, ts_rank, ts_delta, ts_arg_max, ts_corr, sign
import pandas as pd
import numpy as np

def factor_5690(data, **kwargs):
    """
    因子名称: factor_0002_12606
    数学表达式: scale(ts_rank(ts_delta(close, 1), 5) * ts_arg_max(ts_corr(close, vol, 10), 15) * sign(ts_delta(trades,1)))
    中文描述: 该因子在factor_0001的基础上，引入了交易笔数变化的方向sign(ts_delta(trades,1))。首先，ts_rank(ts_delta(close, 1), 5)计算了过去5天内每日收盘价变化（今日收盘价与昨日收盘价之差）的排名，捕捉了短期价格动量。然后，ts_arg_max(ts_corr(close, vol, 10), 15)计算了过去15天内，收盘价和成交量在过去10天相关性达到最大值的位置。sign(ts_delta(trades,1))表示交易笔数变化的方向，当交易笔数增加时为1，减少时为-1。该因子将这三部分相乘，旨在识别出短期价格上涨动量与中期价量关系达到峰值，且交易活跃的时机。创新之处在于结合了价格变化的速度、价量相关性的时间位置和交易活跃度变化的方向，可能用于识别趋势反转或加速的节点。最后使用scale函数进行标准化。
    因子应用场景：
    1. 趋势反转识别：用于识别趋势反转的时机，尤其是在短期价格上涨动量与中期价量关系达到峰值，且交易活跃度变化的方向一致时。
    2. 交易活跃度分析：结合交易笔数变化的方向，可以更准确地判断市场的活跃程度，从而辅助交易决策。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 2. 计算 ts_rank(ts_delta(close, 1), 5)
    data_ts_rank = ts_rank(data_ts_delta_close, d = 5)
    # 3. 计算 ts_corr(close, vol, 10)
    data_ts_corr = ts_corr(data['close'], data['vol'], d = 10)
    # 4. 计算 ts_arg_max(ts_corr(close, vol, 10), 15)
    data_ts_arg_max = ts_arg_max(data_ts_corr, d = 15)
    # 5. 计算 ts_delta(trades, 1)
    data_ts_delta_trades = ts_delta(data['trades'], d = 1)
    # 6. 计算 sign(ts_delta(trades,1))
    data_sign = sign(data_ts_delta_trades)
    # 7. 计算 ts_rank(ts_delta(close, 1), 5) * ts_arg_max(ts_corr(close, vol, 10), 15) * sign(ts_delta(trades,1))
    factor = data_ts_rank * data_ts_arg_max * data_sign
    # 8. 计算 scale(ts_rank(ts_delta(close, 1), 5) * ts_arg_max(ts_corr(close, vol, 10), 15) * sign(ts_delta(trades,1)))
    factor = scale(factor)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()