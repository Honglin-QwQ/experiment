import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5775(data, **kwargs):
    """
    因子名称: VolumeKurtosisAvgCorrelationRatio_71985
    数学表达式: divide(ts_corr(ts_kurtosis(vol, 45), adv(vol, 30), 15), ts_corr(ts_kurtosis(vol, 90), adv(vol, 60), 30))
    中文描述: 该因子计算了两个不同时间窗口下，成交量峰度与平均成交量之间相关性的比值。分子计算了过去45天成交量峰度与过去30天平均成交量在最近15天的相关性，旨在捕捉短期市场情绪异常波动与中期成交量趋势的关系。分母计算了过去90天成交量峰度与过去60天平均成交量在最近30天的相关性，反映了长期市场行为的关联性。通过计算这两个相关性的比值，该因子旨在识别短期市场行为与长期趋势的相对强度。如果比值较高，可能意味着短期内的成交量异常波动与中期趋势高度相关，市场情绪短期爆发显著；如果比值较低，可能意味着短期内的异常波动与长期趋势关联较弱，或者长期趋势更加稳定。相较于原始因子，该因子通过引入不同时间尺度的相关性比较，提供了更丰富的市场动态信息，并尝试通过比值关系来量化短期与长期趋势的相对重要性，具有结构和逻辑上的创新性。改进方向上，该因子尝试通过改变时间窗口参数并计算比值来寻找更有效的组合，并避免了rank函数的直接使用，以简化表达式并降低过度拟合风险。
    因子应用场景：
    1. 市场情绪分析：用于识别短期市场情绪与中期成交量趋势的关系。
    2. 长期趋势识别：用于识别短期市场行为与长期趋势的相对强度。
    """
    # 1. 计算 ts_kurtosis(vol, 45)
    data_ts_kurtosis_vol_45 = ts_kurtosis(data['vol'], d = 45)
    # 2. 计算 adv(vol, 30)
    data_adv_vol_30 = adv(data['vol'], d = 30)
    # 3. 计算 ts_corr(ts_kurtosis(vol, 45), adv(vol, 30), 15)
    data_ts_corr_numerator = ts_corr(data_ts_kurtosis_vol_45, data_adv_vol_30, d = 15)
    # 4. 计算 ts_kurtosis(vol, 90)
    data_ts_kurtosis_vol_90 = ts_kurtosis(data['vol'], d = 90)
    # 5. 计算 adv(vol, 60)
    data_adv_vol_60 = adv(data['vol'], d = 60)
    # 6. 计算 ts_corr(ts_kurtosis(vol, 90), adv(vol, 60), 30)
    data_ts_corr_denominator = ts_corr(data_ts_kurtosis_vol_90, data_adv_vol_60, d = 30)
    # 7. 计算 divide(ts_corr(ts_kurtosis(vol, 45), adv(vol, 30), 15), ts_corr(ts_kurtosis(vol, 90), adv(vol, 60), 30))
    factor = divide(data_ts_corr_numerator, data_ts_corr_denominator)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()