import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import adv, ts_std_dev, divide, ts_rank
import pandas as pd

def factor_5719(data, **kwargs):
    """
    数学表达式: ts_rank(divide(adv(vol, 10), ts_std_dev(adv(vol, 10), 60)), 7)
    中文描述: 该因子旨在捕捉成交量水平与其波动性之间的相对关系，并对这种关系进行时间序列排名。它首先计算过去10天的平均成交量 (adv(vol, 10))，借鉴了参考因子 adv20 的概念，但使用了更短的窗口期以捕捉近期成交量动态。然后，计算这个平均成交量在过去60天内的标准差 (ts_std_dev(adv(vol, 10), 60))，借鉴了参考因子 ts_std_dev 的概念，并应用于平均成交量。创新点在于，该因子计算的是平均成交量与平均成交量标准差的比值 (divide(adv(vol, 10), ts_std_dev(adv(vol, 10), 60)))，而非乘积，这可以衡量在一定波动水平下成交量的相对大小。最后，使用 ts_rank(..., 7) 计算这个比值在过去7天内的排名，借鉴了参考因子 ts_rank 的概念，并使用了更短的窗口期以反映近期趋势。高因子值可能表明近期平均成交量相对其自身的波动性较高，可能预示着市场对该股票的持续关注度和相对稳定的交易活动。相较于历史输出的因子，该因子通过计算比值而非乘积来衡量成交量水平与波动性的关系，并调整了窗口期，希望能够更有效地捕捉市场特征并提升预测能力。改进建议中提到了使用相关性或回归来捕捉成交量异动与波动率的关系，以及考虑波动率的滞后效应。虽然此因子没有直接采用相关性或回归，但通过比值的方式间接衡量了成交量在波动背景下的相对强度。同时，调整窗口期也是参数优化的尝试。未来的改进可以考虑引入 ts_corr 或 ts_regression 来更直接地建模这种关系，或者使用 ts_delay 来考虑滞后效应。
    因子应用场景：
    1. 识别成交量相对其波动性较高的股票，可能预示着市场关注度较高。
    2. 用于量化交易策略中，作为判断股票活跃度和稳定性的指标。
    """
    # 1. 计算 adv(vol, 10)
    data_adv_vol = adv(data['vol'], 10)
    # 2. 计算 ts_std_dev(adv(vol, 10), 60)
    data_ts_std_dev = ts_std_dev(data_adv_vol, 60)
    # 3. 计算 divide(adv(vol, 10), ts_std_dev(adv(vol, 10), 60))
    data_divide = divide(data_adv_vol, data_ts_std_dev)
    # 4. 计算 ts_rank(divide(adv(vol, 10), ts_std_dev(adv(vol, 10), 60)), 7)
    factor = ts_rank(data_divide, 7)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()