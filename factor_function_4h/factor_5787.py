import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_mean, ts_std_dev, ts_delta, rank, ts_corr, ts_rank, ts_skewness

def factor_5787(data, **kwargs):
    """
    因子名称: Volatility_Flow_Momentum_51358
    数学表达式: ts_mean(ts_std_dev(ts_delta(close, 1), 10), 15) * rank(ts_corr(tbase, amount, 20)) - ts_rank(ts_skewness(low, 15), 5)
    中文描述: 该因子旨在捕捉价格波动、交易流量与低价偏度的综合动量。它首先计算收盘价日度变化的10日标准差，并取其15日均值，反映短期价格波动的长期趋势。然后乘以主动买入基础币种数量与交易额在过去20天的相关性排名，衡量买卖力量与交易规模的相关性及其相对强度。最后减去最低价在过去15天的偏度在过去5天内的排名，引入对低价极端波动的考量。高因子值可能表明价格波动趋于稳定，买入力量与交易额正相关性较强，且低价极端波动较小，可能预示着上升动能。
    因子应用场景：
    1. 波动趋势分析：用于识别价格波动趋于稳定的股票，可能预示着市场情绪的稳定。
    2. 交易流量验证：结合交易量和价格波动，验证买卖力量与价格波动的关系。
    3. 风险预警：通过低价偏度排名，预警低价极端波动风险。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta = ts_delta(data['close'], 1)
    # 2. 计算 ts_std_dev(ts_delta(close, 1), 10)
    data_ts_std_dev = ts_std_dev(data_ts_delta, 10)
    # 3. 计算 ts_mean(ts_std_dev(ts_delta(close, 1), 10), 15)
    data_ts_mean = ts_mean(data_ts_std_dev, 15)
    # 4. 计算 ts_corr(tbase, amount, 20)
    data_ts_corr = ts_corr(data['tbase'], data['amount'], 20)
    # 5. 计算 rank(ts_corr(tbase, amount, 20))
    data_rank = rank(data_ts_corr, 2)
    # 6. 计算 ts_skewness(low, 15)
    data_ts_skewness = ts_skewness(data['low'], 15)
    # 7. 计算 ts_rank(ts_skewness(low, 15), 5)
    data_ts_rank = ts_rank(data_ts_skewness, 5)
    # 8. 计算 ts_mean(ts_std_dev(ts_delta(close, 1), 10), 15) * rank(ts_corr(tbase, amount, 20)) - ts_rank(ts_skewness(low, 15), 5)
    factor = data_ts_mean * data_rank - data_ts_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()