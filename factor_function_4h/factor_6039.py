import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_delta, ts_corr, ts_std_dev, ts_mean, rank

def factor_6039(data, **kwargs):
    """
    因子名称: Volume_Volatility_Skew_Momentum_21907
    数学表达式: ts_skewness(ts_delta(volume, 5), 20) * ts_corr(ts_std_dev(close, 10), ts_delta(amount, 3), 15) - ts_mean(rank(tbase), 30)
    中文描述: 该因子旨在捕捉成交量变化、价格波动率、交易额变化以及主动买入量排名之间的复杂关系，以识别市场动量。首先，计算过去5天成交量变化的20天滚动偏度，这部分衡量了成交量变化的非对称性。然后，将这个偏度值乘以过去10天收盘价标准差与过去3天交易额变化之间的15天滚动相关性，这结合了价格波动与资金流动的短期关系。最后，减去过去主动买入基础币种数量（tbase）排名的30天滚动平均值，引入了主动买入行为的长期趋势信息。该因子的创新点在于结合了偏度、相关性和排名平均值等多种统计量，从不同维度刻画市场状态，特别是引入了主动买入量的排名信息，试图捕捉更深层的交易行为特征，以期在市场中发现更微妙的交易信号。当因子值为正时，可能表明成交量变化偏度较高，价格波动与交易额变化正相关，且主动买入排名较低，可能预示着价格下跌动量；当因子值为负时，可能预示着相反的市场状态，可能预示着价格上涨动量。该因子在结构上使用了乘法和减法组合，并引入了偏度、相关性和排名平均值，相较于参考因子有显著创新，并根据历史评估结果，尝试捕捉更复杂的市场特征。
    因子应用场景：
    1. 动量识别：识别市场中潜在的上涨或下跌动量。
    2. 交易信号：为交易者提供买入或卖出信号。
    """
    # 1. 计算 ts_delta(volume, 5)
    data_ts_delta_volume = ts_delta(data['vol'], 5)
    # 2. 计算 ts_skewness(ts_delta(volume, 5), 20)
    data_ts_skewness = ts_skewness(data_ts_delta_volume, 20)
    # 3. 计算 ts_std_dev(close, 10)
    data_ts_std_dev_close = ts_std_dev(data['close'], 10)
    # 4. 计算 ts_delta(amount, 3)
    data_ts_delta_amount = ts_delta(data['amount'], 3)
    # 5. 计算 ts_corr(ts_std_dev(close, 10), ts_delta(amount, 3), 15)
    data_ts_corr = ts_corr(data_ts_std_dev_close, data_ts_delta_amount, 15)
    # 6. 计算 rank(tbase)
    data_rank_tbase = rank(data['tbase'], 2)
    # 7. 计算 ts_mean(rank(tbase), 30)
    data_ts_mean_rank_tbase = ts_mean(data_rank_tbase, 30)
    # 8. 计算 ts_skewness(ts_delta(volume, 5), 20) * ts_corr(ts_std_dev(close, 10), ts_delta(amount, 3), 15) - ts_mean(rank(tbase), 30)
    factor = data_ts_skewness * data_ts_corr - data_ts_mean_rank_tbase

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()