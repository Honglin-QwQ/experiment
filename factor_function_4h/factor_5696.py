import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log_diff, ts_std_dev, ts_corr

def factor_5696(data, **kwargs):
    """
    数学表达式: ts_corr(log_diff(close), ts_std_dev(returns, 20), 10) - ts_corr(log_diff(open), ts_std_dev(returns, 50), 30)
    中文描述: 该因子旨在捕捉收盘价和开盘价对数差分与不同窗口期收益率标准差之间的相关性差异。具体而言，它计算短期（10天）收盘价对数差分与中期（20天）收益率标准差的相关性，并减去长期（30天）开盘价对数差分与长期（50天）收益率标准差的相关性。这个因子结合了价格变动（log_diff）、波动性（ts_std_dev）和时间序列相关性（ts_corr）的概念，通过比较不同时间窗口和不同价格类型（开盘价 vs 收盘价）下的价量关系，试图识别市场动量和波动性之间的背离或一致性。创新点在于同时考虑了开盘价和收盘价的对数差分，并将其与不同时间尺度的波动性指标进行关联分析，从而提供一个更细致和多维度的市场情绪和趋势信号。
    因子应用场景：
    1. 动量与波动性背离：当因子值为正时，可能表明收盘价的短期动量与中期波动性之间存在正相关关系，而开盘价的长期动量与长期波动性之间相关性较弱或负相关，这可能预示着市场动量即将发生变化。
    2. 趋势确认：如果因子值为负，可能表明开盘价的长期动量与长期波动性之间存在较强的相关性，而收盘价的短期动量与中期波动性之间的相关性较弱，这可能意味着当前趋势将持续。
    """
    # 1. 计算 log_diff(close)
    data_log_diff_close = log_diff(data['close'])
    # 2. 计算 ts_std_dev(returns, 20)
    data_ts_std_dev_returns_20 = ts_std_dev(data['returns'], 20)
    # 3. 计算 ts_corr(log_diff(close), ts_std_dev(returns, 20), 10)
    data_ts_corr_1 = ts_corr(data_log_diff_close, data_ts_std_dev_returns_20, 10)
    # 4. 计算 log_diff(open)
    data_log_diff_open = log_diff(data['open'])
    # 5. 计算 ts_std_dev(returns, 50)
    data_ts_std_dev_returns_50 = ts_std_dev(data['returns'], 50)
    # 6. 计算 ts_corr(log_diff(open), ts_std_dev(returns, 50), 30)
    data_ts_corr_2 = ts_corr(data_log_diff_open, data_ts_std_dev_returns_50, 30)
    # 7. 计算 ts_corr(log_diff(close), ts_std_dev(returns, 20), 10) - ts_corr(log_diff(open), ts_std_dev(returns, 50), 30)
    factor = data_ts_corr_1 - data_ts_corr_2

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()