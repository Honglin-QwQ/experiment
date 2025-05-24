import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import inverse, ts_min_diff, adv
import pandas as pd

def factor_5709(data, **kwargs):
    """
    因子名称: Inverse_Min_Avg_Vol_Diff_19381
    数学表达式: inverse(ts_min_diff(adv(vol, 20), 90))
    中文描述: 该因子计算过去20天平均交易量（adv20）与过去90天内adv20最小值的差值的倒数。这结合了参考因子中对最小值的关注和倒数操作，并引入了平均交易量作为衡量流动性的指标。当近期平均交易量显著高于过去低点时，差值较大，因子值较小，可能指示市场关注度提升；反之，差值较小，因子值较大，可能指示流动性低迷。通过倒数转换，放大差值接近零时的信号，捕捉流动性枯竭或异常放大的情况。该因子可用于识别流动性变化带来的潜在交易机会或风险。
    因子应用场景：
    1. 流动性风险预警：因子值异常高可能预示流动性枯竭，增加交易滑点和冲击成本的风险。
    2. 交易机会识别：因子值异常低可能指示市场关注度提升，潜在交易活跃机会。
    """
    # 1. 计算 adv(vol, 20)
    data_adv = adv(data['vol'], d = 20)
    # 2. 计算 ts_min_diff(adv(vol, 20), 90)
    data_ts_min_diff = ts_min_diff(data_adv, d = 90)
    # 3. 计算 inverse(ts_min_diff(adv(vol, 20), 90))
    factor = inverse(data_ts_min_diff)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()