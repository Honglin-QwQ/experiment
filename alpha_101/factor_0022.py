import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_sum, ts_delta, multiply

def factor_0022(data, **kwargs):
    """
    数学表达式: (((ts_sum(high, 20) / 20) < high) ? (-1 * ts_delta(high, 2)) : 0)
    中文描述: 如果过去20天最高价的平均值小于当前最高价，则计算当前最高价与两天前最高价的差值的负值，否则为0。这个因子试图捕捉价格突破近期高点均值后的动量变化，可用于短线择时、识别突破形态和构建量化回测策略。
    因子应用场景：
    1. 短线择时：当因子值为负时，表示价格突破了近期的平均高点，并且当前最高价与两天前的最高价之差为正，可能预示着短期上涨动能。
    2. 突破形态识别：该因子可以帮助识别价格突破形态，尤其是在突破近期高点均值的情况下。
    3. 量化回测策略：该因子可以作为量化回测策略的一部分，用于评估价格突破后的表现。
    """
    import pandas as pd
    # 1. 计算 ts_sum(high, 20)
    sum_high_20 = ts_sum(data['high'], 20)
    # 2. 计算 (ts_sum(high, 20) / 20)
    avg_high_20 = sum_high_20 / 20
    # 3. 计算 (ts_sum(high, 20) / 20) < high
    condition = avg_high_20 < data['high']
    # 4. 计算 ts_delta(high, 2)
    delta_high_2 = ts_delta(data['high'], 2)
    # 5. 计算 -1 * ts_delta(high, 2)
    negative_delta_high_2 = multiply(-1, delta_high_2)
    # 6. 根据条件赋值
    factor = condition * negative_delta_high_2
    factor = factor.where(condition, 0)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()