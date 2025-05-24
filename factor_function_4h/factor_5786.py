import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_kurtosis, ts_std_dev, divide
import pandas as pd

def factor_5786(data, **kwargs):
    """
    因子名称: VolumeVolatilityKurtosisRatio_54510
    数学表达式: divide(ts_kurtosis(vol, 30), ts_std_dev(vol, 60))
    中文描述: 该因子计算了过去30天成交量的峰度与过去60天成交量标准差的比值。成交量峰度衡量了成交量分布的尖峰程度，高峰度可能意味着存在异常的交易日，成交量远高于平均水平。成交量标准差则衡量了成交量的波动性。通过计算峰度与标准差的比值，该因子旨在捕捉成交量异常波动的相对强度，并与长期成交量波动性进行比较。如果比值较高，可能意味着近期成交量出现了显著的尖峰，相对于其长期波动性而言更为突出。这可能预示着市场情绪的短期剧烈变化或特定事件的影响。相较于参考因子，该因子结合了成交量的峰度和标准差，从不同的统计角度分析成交量特征，并使用比值结构进行创新。改进方向上，该因子简化了结构，避免了相关性计算，直接关注成交量自身的统计特征，并尝试通过调整时间窗口来寻找更有效的组合。
    因子应用场景：
    1. 识别成交量异常波动：该因子可以帮助识别成交量出现异常尖峰的情况，可能预示着市场情绪的短期剧烈变化或特定事件的影响。
    2. 波动性分析：通过与长期成交量波动性进行比较，可以评估近期成交量波动的相对强度。
    """
    # 1. 计算 ts_kurtosis(vol, 30)
    data_ts_kurtosis = ts_kurtosis(data['vol'], 30)
    # 2. 计算 ts_std_dev(vol, 60)
    data_ts_std_dev = ts_std_dev(data['vol'], 60)
    # 3. 计算 divide(ts_kurtosis(vol, 30), ts_std_dev(vol, 60))
    factor = divide(data_ts_kurtosis, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()