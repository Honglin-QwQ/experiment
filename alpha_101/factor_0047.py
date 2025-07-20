import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_delta, ts_delay, ts_sum, divide, multiply, subtract, signed_power, indneutralize
import pandas as pd

def factor_0047(data, **kwargs):
    """
    数学表达式: (indneutralize(((ts_corr(ts_delta(close, 1), ts_delta(ts_delay(close, 1), 1), 250) * ts_delta(close, 1)) / close), IndClass.subindustry) / ts_sum(((ts_delta(close, 1) / ts_delay(close, 1))^2), 250))
    中文描述: 该因子首先计算过去250天收盘价每日变化与滞后一天收盘价每日变化的相关性，再将此相关性乘以收盘价每日变化并除以当日收盘价，然后对结果进行行业中性化处理。接着，计算过去250天收盘价每日变化百分比平方和。最后，将行业中性化后的结果除以该平方和。该因子试图捕捉行业调整后的短期价格动量与长期价格波动率的比率，可以用于识别短期价格异动较大但长期波动率较低的股票，可能应用于动量策略、反转策略或波动率交易策略中，也可用于构建风险平价组合以平衡不同股票的风险贡献。
    因子应用场景：
    1. 动量策略： 识别短期价格动量较强，但长期波动率较低的股票。
    2. 反转策略： 寻找价格短期超涨，但长期风险可控的股票。
    3. 波动率交易策略： 用于构建风险平价组合，平衡不同股票的风险贡献。
    """
    # 1. 计算 ts_delta(close, 1)
    delta_close = ts_delta(data['close'], 1)
    # 2. 计算 ts_delay(close, 1)
    delay_close = ts_delay(data['close'], 1)
    # 3. 计算 ts_delta(ts_delay(close, 1), 1)
    delta_delay_close = ts_delta(delay_close, 1)
    # 4. 计算 ts_corr(ts_delta(close, 1), ts_delta(ts_delay(close, 1), 1), 250)
    corr_delta = ts_corr(delta_close, delta_delay_close, 250)
    # 5. 计算 (ts_corr(ts_delta(close, 1), ts_delta(ts_delay(close, 1), 1), 250) * ts_delta(close, 1))
    multiply_corr_delta = multiply(corr_delta, delta_close)
    # 6. 计算 ((ts_corr(ts_delta(close, 1), ts_delta(ts_delay(close, 1), 1), 250) * ts_delta(close, 1)) / close)
    temp = divide(multiply_corr_delta, data['close'])
    # 7. 计算 indneutralize(((ts_corr(ts_delta(close, 1), ts_delta(ts_delay(close, 1), 1), 250) * ts_delta(close, 1)) / close), IndClass.subindustry)
    ind_neutralize = indneutralize(temp, data['industry'])
    # 8. 计算 (ts_delta(close, 1) / ts_delay(close, 1))
    divide_delta_delay = divide(delta_close, delay_close)
    # 9. 计算 ((ts_delta(close, 1) / ts_delay(close, 1))^2)
    power_divide_delta_delay = signed_power(divide_delta_delay, 2)
    # 10. 计算 ts_sum(((ts_delta(close, 1) / ts_delay(close, 1))^2), 250)
    sum_power = ts_sum(power_divide_delta_delay, 250)
    # 11. 计算 (indneutralize(((ts_corr(ts_delta(close, 1), ts_delta(ts_delay(close, 1), 1), 250) * ts_delta(close, 1)) / close), IndClass.subindustry) / ts_sum(((ts_delta(close, 1) / ts_delay(close, 1))^2), 250))
    factor = divide(ind_neutralize, sum_power)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()