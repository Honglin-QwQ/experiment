import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_sum, ts_std_dev, divide, multiply, adv

def factor_0020(data, **kwargs):
    """
    数学表达式: ((((ts_sum(close, 8) / 8) + ts_std_dev(close, 8)) < (ts_sum(close, 2) / 2)) ? (-1 * 1) : (((ts_sum(close, 2) / 2) < ((ts_sum(close, 8) / 8) - ts_std_dev(close, 8))) ? 1 : (((1 < (volume / adv20)) || ((volume / adv20) == 1)) ? 1 : (-1 * 1))))
    中文描述: 该因子首先计算过去8天收盘价的平均值和标准差，如果平均值加标准差小于过去2天收盘价的平均值，则赋值为-1；否则，如果过去2天收盘价的平均值小于过去8天收盘价的平均值减去标准差，则赋值为1；如果成交量除以过去20天平均成交量大于等于1，则赋值为1，否则赋值为-1。该因子融合了短期和长期价格趋势以及成交量信息，可能用于识别趋势反转或突破，应用场景包括：1. 短线交易：寻找超卖反弹或超买回调的机会。2. 量价配合策略：验证价格趋势是否得到成交量的支持。3. 趋势跟踪：在趋势确认时加入头寸，避免假突破。
    因子应用场景：
    1. 短线交易：寻找超卖反弹或超买回调的机会。
    2. 量价配合策略：验证价格趋势是否得到成交量的支持。
    3. 趋势跟踪：在趋势确认时加入头寸，避免假突破。
    """
    # 计算过去8天收盘价的平均值
    ts_sum_close_8 = ts_sum(data['close'], 8)
    avg_close_8 = divide(ts_sum_close_8, 8)

    # 计算过去8天收盘价的标准差
    std_close_8 = ts_std_dev(data['close'], 8)

    # 计算过去2天收盘价的平均值
    ts_sum_close_2 = ts_sum(data['close'], 2)
    avg_close_2 = divide(ts_sum_close_2, 2)

    # 计算过去20天平均成交量
    adv20 = adv(data['vol'], d = 20)

    # 计算成交量除以过去20天平均成交量
    volume_ratio = divide(data['vol'], adv20)

    import numpy as np
    factor = np.where(
        (avg_close_8 + std_close_8) < avg_close_2,
        -1,
        np.where(
            avg_close_2 < (avg_close_8 - std_close_8),
            1,
            np.where(
                (1 < volume_ratio) | (volume_ratio == 1),
                1,
                -1
            )
        )
    )

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()