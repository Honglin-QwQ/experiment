import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_max, subtract, ts_rank, signed_power, ts_delta

def factor_0083(data, **kwargs):
    """
    数学表达式: signed_power(ts_rank((vwap - ts_max(vwap, 15.3217)), 20.7127), ts_delta(close, 4.96796))
    中文描述: 这个因子首先计算过去15.3217天成交量加权平均价的最大值，然后用当前的成交量加权平均价减去这个最大值，接着计算这个差值在过去20.7127天的排序，再将这个排序结果进行平方，并保留排序结果的符号，最后计算收盘价在过去4.96796天的变化量，并将前面的带符号的平方值进行该变化量次方的运算。这个因子试图捕捉价格突破后动量的大小和方向，并结合了价格变化的速度信息。
    应用场景：
    1. 可以用于识别价格突破阻力位后，动量较强且价格上涨加速的股票，构建突破策略。
    2. 可以用于量化模型中，作为判断股票短期强势程度的因子，辅助选股。
    3. 可以结合其他技术指标，例如成交量，形成更复杂的交易信号。
    """
    # 1. 计算 ts_max(vwap, 15.3217)
    data_ts_max_vwap = ts_max(data['vwap'], d = 15.3217)
    # 2. 计算 (vwap - ts_max(vwap, 15.3217))
    data_subtract = subtract(data['vwap'], data_ts_max_vwap)
    # 3. 计算 ts_rank((vwap - ts_max(vwap, 15.3217)), 20.7127)
    data_ts_rank = ts_rank(data_subtract, d = 20.7127)
    # 4. 计算 ts_delta(close, 4.96796)
    data_ts_delta_close = ts_delta(data['close'], d = 4.96796)
    # 5. 计算 signed_power(ts_rank((vwap - ts_max(vwap, 15.3217)), 20.7127), ts_delta(close, 4.96796))
    factor = signed_power(data_ts_rank, data_ts_delta_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()