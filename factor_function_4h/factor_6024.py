import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import inverse, scale, divide, ts_rank, adv, ts_min_diff
import pandas as pd

def factor_6024(data, **kwargs):
    """
    数学表达式: inverse(scale(divide(ts_rank(adv(vol, 20), 23), ts_min_diff(open, 48))))
    中文描述: 该因子是对先前因子的改进版本，旨在提升其预测能力并反转方向。它首先计算过去20天平均成交量在过去23天内的排名，并将其除以当前开盘价与过去48天最低开盘价的差值。然后对结果进行标准化处理，最后取其倒数。这样做是为了将原先的负相关关系转化为正相关关系，并利用倒数运算放大因子值较小的股票的信号，同时通过标准化消除量纲影响。较高因子值可能表明成交量排名相对较高，但开盘价相对于近期最低点上涨有限，或者成交量排名较低但开盘价相对于近期最低点有显著上涨，这些情况在取倒数和标准化后可能转化为积极信号。创新点在于结合了时间序列排名、时间序列差值、标准化和倒数运算，构建了一个多维度的因子，并试图通过数学变换改变因子的预测方向和信号强度。
    因子应用场景：
    1. 反转策略：用于识别可能被低估的股票，这些股票的成交量排名可能较低，但开盘价相对于近期最低点有显著上涨。
    2. 信号放大：通过倒数运算，放大因子值较小的股票的信号，使其在投资组合中获得更大的权重。
    3. 多因子模型：与其他因子结合使用，提高模型的预测能力和稳定性。
    """
    # 1. 计算 adv(vol, 20)
    data_adv_vol = adv(data['vol'], d = 20)
    # 2. 计算 ts_rank(adv(vol, 20), 23)
    data_ts_rank = ts_rank(data_adv_vol, d = 23)
    # 3. 计算 ts_min_diff(open, 48)
    data_ts_min_diff = ts_min_diff(data['open'], d = 48)
    # 4. 计算 divide(ts_rank(adv(vol, 20), 23), ts_min_diff(open, 48))
    data_divide = divide(data_ts_rank, data_ts_min_diff)
    # 5. 计算 scale(divide(ts_rank(adv(vol, 20), 23), ts_min_diff(open, 48)))
    data_scale = scale(data_divide)
    # 6. 计算 inverse(scale(divide(ts_rank(adv(vol, 20), 23), ts_min_diff(open, 48))))
    factor = inverse(data_scale)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()