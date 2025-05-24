import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log_diff, divide, kth_element, log

def factor_5720(data, **kwargs):
    """
    因子名称: LogDiff_AdvVolRatio_29192
    数学表达式: log_diff(divide(kth_element(adv20, 5, k=1), kth_element(vol, 5, k=1)))
    中文描述: 该因子计算过去5天内第一个有效值的20日平均交易量与当前交易量的比值的对数差。它结合了长期平均交易量和短期实际交易量的信息，并通过对数差捕捉其变化率。这可能反映了市场活动在不同时间尺度上的相对变化，可用于识别交易量结构的变化或潜在的市场情绪转变。
    因子应用场景：
    1. 交易量变化分析：用于识别交易量结构的变化或潜在的市场情绪转变。
    2. 市场情绪判断：反映市场活动在不同时间尺度上的相对变化。
    """
    # 1. 计算 kth_element(adv20, 5, k=1)
    adv20 = data['amount']
    data_kth_element_adv20 = kth_element(adv20, 5, k=1)
    # 2. 计算 kth_element(vol, 5, k=1)
    data_kth_element_vol = kth_element(data['vol'], 5, k=1)
    # 3. 计算 divide(kth_element(adv20, 5, k=1), kth_element(vol, 5, k=1))
    data_divide = divide(data_kth_element_adv20, data_kth_element_vol)
    # 4. 计算 log_diff(divide(kth_element(adv20, 5, k=1), kth_element(vol, 5, k=1)))
    factor = log_diff(data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()