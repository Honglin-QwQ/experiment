import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import divide, ts_mean, ts_std_dev, ts_delta

def factor_5949(data, **kwargs):
    """
    因子名称: VolumeVolatilityAccelerationRatio_38418
    数学表达式: divide(ts_mean(ts_std_dev(vol, 30), 10), (ts_mean(ts_delta(vol, 5), 60) + ts_mean(ts_delta(ts_delta(vol, 5), 5), 60)))
    中文描述: 该因子是基于对原有VolumeVolatilityRatio因子的改进。它计算经过10日平滑的过去30天成交量标准差与成交量变化均值和成交量变化加速均值之和的比值。分子捕捉经过平滑的成交量短期波动性，分母则综合考虑了成交量中长期变化的平均趋势及其加速情况。通过引入波动率变化加速的概念，该因子旨在更敏感地捕捉成交量变化的动态，并对极端波动率变化具有一定的平滑作用。高值可能表示平滑后的成交量波动剧烈且缺乏明确的长期变化趋势和加速，低值则可能表示平滑后的成交量波动相对平稳且存在一定的长期变化规律或减速。这有助于识别市场情绪的稳定性和交易活动的持续性，同时对原有因子进行了创新性的改进，以期提升预测能力和稳定性。
    因子应用场景：
    1. 波动性分析：用于识别成交量波动较大但长期趋势不明显的股票。
    2. 趋势识别：用于识别成交量波动较小且具有长期趋势的股票。
    3. 市场情绪：高值可能表示市场情绪不稳定，低值可能表示市场情绪稳定。
    """
    # 1. 计算 ts_std_dev(vol, 30)
    data_ts_std_dev = ts_std_dev(data['vol'], 30)
    # 2. 计算 ts_mean(ts_std_dev(vol, 30), 10)
    data_ts_mean_std = ts_mean(data_ts_std_dev, 10)
    # 3. 计算 ts_delta(vol, 5)
    data_ts_delta1 = ts_delta(data['vol'], 5)
    # 4. 计算 ts_mean(ts_delta(vol, 5), 60)
    data_ts_mean_delta1 = ts_mean(data_ts_delta1, 60)
    # 5. 计算 ts_delta(ts_delta(vol, 5), 5)
    data_ts_delta2 = ts_delta(data_ts_delta1, 5)
    # 6. 计算 ts_mean(ts_delta(ts_delta(vol, 5), 5), 60)
    data_ts_mean_delta2 = ts_mean(data_ts_delta2, 60)
    # 7. 计算 (ts_mean(ts_delta(vol, 5), 60) + ts_mean(ts_delta(ts_delta(vol, 5), 5), 60))
    data_sum = data_ts_mean_delta1 + data_ts_mean_delta2
    # 8. 计算 divide(ts_mean(ts_std_dev(vol, 30), 10), (ts_mean(ts_delta(vol, 5), 60) + ts_mean(ts_delta(ts_delta(vol, 5), 5), 60)))
    factor = divide(data_ts_mean_std, data_sum)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()