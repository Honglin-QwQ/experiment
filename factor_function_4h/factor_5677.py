import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import zscore, divide, subtract, ts_weighted_decay, adv
import pandas as pd

def factor_5677(data, **kwargs):
    """
    因子名称: VolumeAdjustedPriceDeviationZscore_30503
    数学表达式: zscore(divide(subtract(close, ts_weighted_decay(close, k = 0.5)), adv(vol, d = 20)))
    中文描述: 该因子基于历史因子VolumeWeightedOpenPriceDeviationRanked的改进建议，简化了计算逻辑，移除了rank函数，并使用了zscore进行标准化。它衡量了收盘价相对于其近期加权衰减趋势的偏离程度，并使用过去20天的平均成交量进行调整，最后通过zscore标准化，使得因子更具有可比性。该因子旨在捕捉价格变化与成交量之间的关系，适用于震荡市和趋势反转的市场环境。
    因子应用场景：
    1. 震荡市：因子值可能在震荡市中更有效，因为它捕捉了价格的短期波动与成交量的关系。
    2. 趋势反转：当因子值出现极端值时，可能预示着趋势的反转。
    """
    # 1. 计算 ts_weighted_decay(close, k = 0.5)
    data_ts_weighted_decay = ts_weighted_decay(data['close'], k = 0.5)
    # 2. 计算 subtract(close, ts_weighted_decay(close, k = 0.5))
    data_subtract = subtract(data['close'], data_ts_weighted_decay)
    # 3. 计算 adv(vol, d = 20)
    data_adv = adv(data['vol'], d = 20)
    # 4. 计算 divide(subtract(close, ts_weighted_decay(close, k = 0.5)), adv(vol, d = 20))
    data_divide = divide(data_subtract, data_adv)
    # 5. 计算 zscore(divide(subtract(close, ts_weighted_decay(close, k = 0.5)), adv(vol, d = 20)))
    factor = zscore(data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()