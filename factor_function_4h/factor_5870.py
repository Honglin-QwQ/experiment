import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import if_else, and_operator, divide, ts_std_dev, ts_mean, subtract, ts_delta

def factor_5870(data, **kwargs):
    """
    因子名称: Volatility_Breakout_Mean_Reversion_14322
    数学表达式: if_else(and_operator(divide(ts_std_dev(close, 10), ts_mean(close, 10)) > 0.02, close > ts_mean(close, 20)), subtract(0, divide(ts_delta(close, 1), close)), 0)
    中文描述: 该因子结合了波动率突破和均值回归的思想。首先，它判断近10天的收盘价标准差与均值之比（衡量波动率）是否超过0.02，并且当前收盘价是否高于近20天的均值。如果这两个条件都满足（视为波动率突破且价格处于相对高位），则计算当前收盘价相对于前一日收盘价的百分比变化（即收益率）的负数。否则，因子值为0。这个因子旨在捕捉在波动率放大且价格上涨后的潜在均值回归机会，当因子值为负时，可能预示着短期回调的可能。
    因子应用场景：
    1. 波动率突破识别：用于识别波动率显著增加的股票。
    2. 均值回归策略：在股价突破后，寻找均值回归的机会。
    3. 短期回调预测：因子值为负时，可能预示着短期回调的可能。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], 10)
    # 2. 计算 ts_mean(close, 10)
    data_ts_mean_10 = ts_mean(data['close'], 10)
    # 3. 计算 divide(ts_std_dev(close, 10), ts_mean(close, 10))
    data_divide = divide(data_ts_std_dev, data_ts_mean_10)
    # 4. 计算 divide(ts_std_dev(close, 10), ts_mean(close, 10)) > 0.02
    condition1 = data_divide > 0.02
    # 5. 计算 ts_mean(close, 20)
    data_ts_mean_20 = ts_mean(data['close'], 20)
    # 6. 计算 close > ts_mean(close, 20)
    condition2 = data['close'] > data_ts_mean_20
    # 7. 计算 and_operator(divide(ts_std_dev(close, 10), ts_mean(close, 10)) > 0.02, close > ts_mean(close, 20))
    data_and_operator = and_operator(condition1, condition2)
    # 8. 计算 ts_delta(close, 1)
    data_ts_delta = ts_delta(data['close'], 1)
    # 9. 计算 divide(ts_delta(close, 1), close)
    data_divide_delta_close = divide(data_ts_delta, data['close'])
    # 10. 计算 subtract(0, divide(ts_delta(close, 1), close))
    data_subtract = subtract(0, data_divide_delta_close)
    # 11. 计算 if_else(and_operator(divide(ts_std_dev(close, 10), ts_mean(close, 10)) > 0.02, close > ts_mean(close, 20)), subtract(0, divide(ts_delta(close, 1), close)), 0)
    factor = if_else(data_and_operator, data_subtract, 0)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()