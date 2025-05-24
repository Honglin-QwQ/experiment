import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_delta, log, divide, ts_min

def factor_5573(data, **kwargs):
    """
    因子名称: factor_volume_price_momentum_89579
    数学表达式: rank(ts_delta(close, 5)) * log(divide(vol, ts_min(vol, 20)))
    中文描述: 本因子结合了价格动量与成交量相对低位的自然对数。首先，使用ts_delta计算过去5天收盘价的变化，并使用rank进行排序，衡量价格上涨的动量。然后，计算当前成交量与过去20天最低成交量的比值，并取自然对数，用于衡量当前成交量相对于近期低点的程度。两者相乘，旨在捕捉市场价格动量与成交量放大之间的关系，可能在价格上涨初期提供交易信号。创新点在于结合了价格动量和成交量相对位置，可能在市场反弹初期提供更强的交易信号。
    因子应用场景：
    1. 价格动量捕捉：用于识别价格上涨的初期阶段，结合成交量的放大，提高信号的可靠性。
    2. 市场反弹信号：在市场经历下跌后，该因子可能有助于发现成交量开始放大、价格开始回升的股票。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], d=5)
    # 2. 计算 rank(ts_delta(close, 5))
    data_rank = rank(data_ts_delta)
    # 3. 计算 ts_min(vol, 20)
    data_ts_min = ts_min(data['vol'], d=20)
    # 4. 计算 divide(vol, ts_min(vol, 20))
    data_divide = divide(data['vol'], data_ts_min)
    # 5. 计算 log(divide(vol, ts_min(vol, 20)))
    data_log = log(data_divide)
    # 6. 计算 rank(ts_delta(close, 5)) * log(divide(vol, ts_min(vol, 20)))
    factor = data_rank * data_log

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()