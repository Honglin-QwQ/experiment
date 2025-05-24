import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import if_else, ts_delta, multiply, ts_rank, ts_zscore, subtract

def factor_5572(data, **kwargs):
    """
    因子名称: factor_innovative_003_30446
    数学表达式: if_else(ts_delta(close, d=5) > 0, multiply(ts_rank(close, d=5), ts_zscore(multiply(vol, close), d=5)), subtract(ts_rank(close, d=5), ts_zscore(multiply(vol, close), d=5)))
    中文描述: 该因子旨在衡量价格趋势与成交量之间的关系，并结合了时间序列分析和横截面分析。与之前的因子相比，该因子引入了条件判断，当过去5天收盘价上涨时，采用价格排名和成交额Z-score的乘积，当收盘价下跌时，采用价格排名和成交额Z-score的差值。这种设计使得因子能够根据市场趋势自适应地调整计算方式，从而更准确地捕捉市场情绪和交易活跃度。该因子的创新之处在于根据价格趋势动态调整因子计算逻辑，以更全面地评估市场情绪和交易活跃度，同时捕捉价格趋势。该因子可用于识别价格趋势与成交量之间的背离或一致性，从而辅助交易决策。
    因子应用场景：
    1. 趋势识别：根据价格趋势动态调整因子计算逻辑，更全面地评估市场情绪和交易活跃度，同时捕捉价格趋势。
    2. 市场情绪分析：识别价格趋势与成交量之间的背离或一致性，从而辅助交易决策。
    """
    # 1. 计算 ts_delta(close, d=5)
    ts_delta_close = ts_delta(data['close'], d=5)

    # 2. 计算 multiply(vol, close)
    multiply_vol_close = multiply(data['vol'], data['close'])

    # 3. 计算 ts_zscore(multiply(vol, close), d=5)
    ts_zscore_multiply_vol_close = ts_zscore(multiply_vol_close, d=5)

    # 4. 计算 ts_rank(close, d=5)
    ts_rank_close = ts_rank(data['close'], d=5)

    # 5. 计算 multiply(ts_rank(close, d=5), ts_zscore(multiply(vol, close), d=5))
    multiply_ts_rank_ts_zscore = multiply(ts_rank_close, ts_zscore_multiply_vol_close)

    # 6. 计算 subtract(ts_rank(close, d=5), ts_zscore(multiply(vol, close), d=5))
    subtract_ts_rank_ts_zscore = subtract(ts_rank_close, ts_zscore_multiply_vol_close)

    # 7. 计算 if_else(ts_delta(close, d=5) > 0, multiply(ts_rank(close, d=5), ts_zscore(multiply(vol, close), d=5)), subtract(ts_rank(close, d=5), ts_zscore(multiply(vol, close), d=5)))
    factor = if_else(ts_delta_close > 0, multiply_ts_rank_ts_zscore, subtract_ts_rank_ts_zscore)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()