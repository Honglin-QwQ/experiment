import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, add, divide, subtract, ts_scale, adv

def factor_0027(data, **kwargs):
    """
    数学表达式: ts_scale(((ts_corr(adv20, low, 5) + ((high + low) / 2)) - close))
    中文描述: 对过去20天平均成交额和最低价的相关性进行计算，加上过去最高价和最低价的均值，减去收盘价，然后对结果进行过去一段时间的标准化处理，使其数值分布在0到1之间，这个因子可能反映了成交量、价格波动与收盘价之间的关系，可以用于量化交易中寻找价格异动或超买超卖的机会，也可用于构建趋势跟踪或反转策略，或者用于识别市场情绪的变化。
    因子应用场景：
    1. 量化交易：寻找价格异动或超买超卖的机会。
    2. 趋势跟踪或反转策略：构建趋势跟踪或反转策略。
    3. 市场情绪变化：识别市场情绪的变化。
    """
    # 1. 计算 adv20
    data_adv20 = adv(data['amount'], d=20)
    # 2. 计算 ts_corr(adv20, low, 5)
    data_ts_corr = ts_corr(data_adv20, data['low'], d=5)
    # 3. 计算 (high + low) / 2
    data_high_plus_low = add(data['high'], data['low'])
    data_high_plus_low_divide_2 = divide(data_high_plus_low, 2)
    del data_high_plus_low
    # 4. 计算 ts_corr(adv20, low, 5) + ((high + low) / 2)
    data_corr_plus_mean = add(data_ts_corr, data_high_plus_low_divide_2)
    del data_ts_corr
    del data_high_plus_low_divide_2
    # 5. 计算 (ts_corr(adv20, low, 5) + ((high + low) / 2)) - close
    data_sub = subtract(data_corr_plus_mean, data['close'])
    del data_corr_plus_mean
    # 6. 计算 ts_scale(((ts_corr(adv20, low, 5) + ((high + low) / 2)) - close))
    factor = ts_scale(data_sub)
    del data_sub

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()