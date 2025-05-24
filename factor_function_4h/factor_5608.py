import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_delta, ts_rank, ts_corr, ts_std_dev, adv, ts_mean, divide

def factor_5608(data, **kwargs):
    """
    因子名称: factor_0001_39835
    数学表达式: rank(ts_delta(close, 3)) + ts_rank(ts_corr(ts_std_dev(high, 5), adv20, 5), 10) + ts_mean(divide(amount, vol), 5)
    中文描述: 该因子结合了短期价格动量、成交量与价格波动相关性以及量价关系。首先计算过去3天收盘价差分的排名，然后加上过去10天平均成交量和最高价标准差相关系数的时间序列排名，最后加上过去5天交易额与交易量比值的均值。该因子旨在捕捉短期价格变化趋势、长期成交量与价格波动关系以及量价配合情况，可用于量化选股中，例如，可以结合其他因子构建多因子模型，或者用于识别具有潜在上涨动力的股票，也可用于高频交易中，预测股票的短期价格波动方向。
    因子应用场景：
    1. 量化选股：结合其他因子构建多因子模型。
    2. 趋势识别：识别具有潜在上涨动力的股票。
    3. 高频交易：预测股票的短期价格波动方向。
    """
    # 1. 计算 ts_delta(close, 3)
    data_ts_delta = ts_delta(data['close'], d=3)
    # 2. 计算 rank(ts_delta(close, 3))
    factor1 = rank(data_ts_delta)
    
    # 3. 计算 ts_std_dev(high, 5)
    data_ts_std_dev = ts_std_dev(data['high'], d=5)
    # 4. 计算 adv20
    data_adv20 = adv(data['vol'], d=20)
    # 5. 计算 ts_corr(ts_std_dev(high, 5), adv20, 5)
    data_ts_corr = ts_corr(data_ts_std_dev, data_adv20, d=5)
    # 6. 计算 ts_rank(ts_corr(ts_std_dev(high, 5), adv20, 5), 10)
    factor2 = ts_rank(data_ts_corr, d=10)
    
    # 7. 计算 divide(amount, vol)
    data_divide = divide(data['amount'], data['vol'])
    # 8. 计算 ts_mean(divide(amount, vol), 5)
    factor3 = ts_mean(data_divide, d=5)
    
    # 9. 计算 factor1 + factor2 + factor3
    factor = factor1 + factor2 + factor3

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()