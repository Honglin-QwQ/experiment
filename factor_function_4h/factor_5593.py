import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import multiply, ts_returns, ts_corr, ts_rank, ts_delta

def factor_5593(data, **kwargs):
    """
    因子名称: factor_volume_price_momentum_enhanced_95437
    数学表达式: multiply(ts_returns(close, 5, mode = 1), ts_corr(amount, ts_returns(close, 5, mode = 1), 10), ts_rank(ts_delta(vol, 5), 5))
    中文描述: 该因子融合了价格动量、量价相关性和成交量变化动量信息，旨在捕捉趋势性行情中的量价配合异动。
            首先，使用ts_returns(close, 5, mode = 1)计算过去5天的算术收益率，反映价格动量；
            然后，使用ts_corr(amount, ts_returns(close, 5, mode = 1), 10)计算过去10天交易额与5日收益率的相关性，捕捉量价配合关系；
            同时，使用ts_delta(vol, 5)计算成交量与过去5天成交量的差值，反映成交量支撑力度；
            再使用ts_rank(..., 5)计算该差值的5日排名，标准化成交量支撑动量。
            最后，将5日收益率、量价相关性和标准化成交量支撑动量相乘，得到最终因子值。
            该因子适用于趋势性行情，可用于识别潜在的价格突破或趋势延续机会。
            相较于历史因子，该因子简化了成交量和交易额的计算方式，更关注收益率与成交额的相关性，并使用ts_rank代替ts_zscore，避免了过度标准化，同时结合了价格动量，更直接地反映了市场趋势。
    因子应用场景：
    1. 趋势识别：因子值较高可能意味着当前趋势较强且稳定。
    2. 量价配合分析：因子有助于识别量价配合关系，捕捉价格突破或趋势延续的机会。
    """
    # 1. 计算 ts_returns(close, 5, mode = 1)
    data_ts_returns = ts_returns(data['close'], 5, mode = 1)
    # 2. 计算 ts_corr(amount, ts_returns(close, 5, mode = 1), 10)
    data_ts_corr = ts_corr(data['amount'], data_ts_returns, 10)
    # 3. 计算 ts_delta(vol, 5)
    data_ts_delta = ts_delta(data['vol'], 5)
    # 4. 计算 ts_rank(ts_delta(vol, 5), 5)
    data_ts_rank = ts_rank(data_ts_delta, 5)
    # 5. 计算 multiply(ts_returns(close, 5, mode = 1), ts_corr(amount, ts_returns(close, 5, mode = 1), 10), ts_rank(ts_delta(vol, 5), 5))
    factor = multiply(data_ts_returns, data_ts_corr, data_ts_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()