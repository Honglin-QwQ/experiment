import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_delta, ts_std_dev, rank, ts_skewness, ts_returns, multiply

def factor_5735(data, **kwargs):
    """
    因子名称: Volatility_Skew_Momentum_Divergence_14185
    数学表达式: ts_corr(ts_delta(low, 3), ts_std_dev(ts_delta(low, 3), 66), 10) * rank(ts_skewness(ts_returns(close, 7), 30))
    中文描述: 该因子结合了低价波动率的变化趋势与短期收益的偏度信息。首先，计算过去10天内每日最低价3天变化量与其66天标准差之间的相关性，捕捉低价波动率变化的速度和方向。然后，计算过去30天收盘价7天收益率的偏度，衡量短期收益分布的对称性，并对其进行排名。最后，将这两部分相乘。因子逻辑在于，当低价波动率加速上升（相关性为正）且短期收益分布呈现负偏（排名较低，表明存在下行风险）时，因子值可能为负，预示着潜在的下行风险；反之，当低价波动率减缓或下降（相关性为负）且短期收益分布接近对称或正偏（排名较高）时，因子值可能为正，预示着市场情绪可能改善。这个因子创新性地结合了基于最低价的波动率分析和基于收盘价收益率的偏度分析，并引入了相关性和排名操作符，以捕捉市场在不同价格层面的动态和情绪变化，可用于识别市场情绪反转或持续性动量。
    因子应用场景：
    1. 识别市场情绪反转或持续性动量。
    2. 捕捉市场在不同价格层面的动态和情绪变化。
    """
    # 1. 计算 ts_delta(low, 3)
    data_ts_delta_low = ts_delta(data['low'], 3)
    # 2. 计算 ts_std_dev(ts_delta(low, 3), 66)
    data_ts_std_dev = ts_std_dev(data_ts_delta_low, 66)
    # 3. 计算 ts_corr(ts_delta(low, 3), ts_std_dev(ts_delta(low, 3), 66), 10)
    data_ts_corr = ts_corr(data_ts_delta_low, data_ts_std_dev, 10)
    # 4. 计算 ts_returns(close, 7)
    data_ts_returns_close = ts_returns(data['close'], 7)
    # 5. 计算 ts_skewness(ts_returns(close, 7), 30)
    data_ts_skewness = ts_skewness(data_ts_returns_close, 30)
    # 6. 计算 rank(ts_skewness(ts_returns(close, 7), 30))
    data_rank = rank(data_ts_skewness, 2)
    # 7. 计算 ts_corr(ts_delta(low, 3), ts_std_dev(ts_delta(low, 3), 66), 10) * rank(ts_skewness(ts_returns(close, 7), 30))
    factor = multiply(data_ts_corr, data_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()