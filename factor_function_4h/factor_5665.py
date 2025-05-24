import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import subtract
from operators import ts_weighted_decay
from operators import divide
from operators import adv

def factor_5665(data, **kwargs):
    """
    因子名称: VolumeWeightedOpenPriceDeviation_22298
    数学表达式: divide(subtract(open, ts_weighted_decay(open, k = 0.5)), adv(vol, d = 20))
    中文描述: 该因子计算开盘价与开盘价加权衰减均值的偏差，并用过去20天成交量的平均值进行标准化。该因子的设计思路是衡量开盘价相对于其近期趋势的偏离程度，并结合成交量进行调整，以反映市场活跃度对价格偏离的影响。创新点在于结合了价格的时间序列加权衰减和成交量信息，可以更有效地识别价格的短期异动。
    因子应用场景：
    1. 短期异动识别：当因子值较高时，可能表明开盘价相对于其近期加权均值偏离较大，预示着短期内可能存在交易机会。
    2. 市场活跃度评估：结合成交量信息，可以判断价格偏离是否伴随市场活跃度的增加，从而更准确地评估价格异动的可靠性。
    """
    # 1. 计算 ts_weighted_decay(open, k = 0.5)
    data_ts_weighted_decay = ts_weighted_decay(data['open'], k = 0.5)
    # 2. 计算 subtract(open, ts_weighted_decay(open, k = 0.5))
    data_subtract = subtract(data['open'], data_ts_weighted_decay)
    # 3. 计算 adv(vol, d = 20)
    data_adv = adv(data['vol'], d = 20)
    # 4. 计算 divide(subtract(open, ts_weighted_decay(open, k = 0.5)), adv(vol, d = 20))
    factor = divide(data_subtract, data_adv)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()