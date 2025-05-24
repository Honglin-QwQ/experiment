import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log, divide, add, multiply, ts_delta, ts_std_dev

def factor_5666(data, **kwargs):
    """
    因子名称: DynamicVolumeVolatilityRatioWeighted_LogScaled_68063
    数学表达式: divide(add(log(adv20), multiply(ts_delta(log(adv20), 5), 0.3)), ts_std_dev(log(adv20), 120))
    中文描述: 该因子在DynamicVolumeVolatilityRatioWeighted的基础上，对adv20取对数，以减小极端成交量值的影响，并调整了ts_delta的系数。具体来说，它计算过去20天平均成交量取对数（log(adv20)）与过去5天成交量取对数的变化率的加权和，然后除以过去120天平均成交量取对数的标准差。对数变换可以平滑成交量数据，减少异常值的影响，使得因子对成交量的变化更加敏感。同时，将ts_delta的系数调整为0.3，以增强短期成交量变化的影响。该因子适用于寻找流动性良好且市场关注度较高的投资标的，尤其是在市场波动较大的情况下，对数变换后的成交量数据可以提高因子的稳健性。
    因子应用场景：
    1. 流动性分析：用于识别流动性良好且市场关注度高的投资标的。
    2. 风险管理：在市场波动较大时，通过对数变换提高成交量数据的稳健性。
    3. 短期交易：增强短期成交量变化的影响，适用于短期交易策略。
    """
    # 1. 计算 adv20
    adv20 = data['vol'].rolling(window=20, min_periods=1).mean()
    # 2. 计算 log(adv20)
    log_adv20 = log(adv20)
    # 3. 计算 ts_delta(log(adv20), 5)
    ts_delta_log_adv20 = ts_delta(log_adv20, 5)
    # 4. 计算 multiply(ts_delta(log(adv20), 5), 0.3)
    multiply_ts_delta_log_adv20 = multiply(ts_delta_log_adv20, 0.3)
    # 5. 计算 add(log(adv20), multiply(ts_delta(log(adv20), 5), 0.3))
    add_log_adv20 = add(log_adv20, multiply_ts_delta_log_adv20)
    # 6. 计算 ts_std_dev(log(adv20), 120)
    ts_std_dev_log_adv20 = ts_std_dev(log_adv20, 120)
    # 7. 计算 divide(add(log(adv20), multiply(ts_delta(log(adv20), 5), 0.3)), ts_std_dev(log(adv20), 120))
    factor = divide(add_log_adv20, ts_std_dev_log_adv20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()