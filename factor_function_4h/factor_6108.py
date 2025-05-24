import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import divide, ts_quantile, ts_delta

def factor_6108(data, **kwargs):
    """
    因子名称: VolumeDeltaQuantileRatio_68670
    数学表达式: divide(ts_quantile(ts_delta(volume, 3), 240), ts_quantile(ts_delta(vol, 5), 120))
    中文描述: 该因子计算了两个不同时间窗口和滞后期的交易量变化量分位数的比值。分子是参考因子中计算的3天交易量变化量在过去240天的分位数，而分母是5天交易量变化量在过去120天的分位数。通过比较不同时间尺度下的交易量变化相对强度，可以更全面地评估市场情绪和资金流动的变化，捕捉不同周期下的市场信号。例如，分子反映了短期交易量变化的长期相对位置，而分母反映了稍长期交易量变化的短期相对位置。这种比值结构具有创新性，能够揭示不同时间维度上交易量变化的相对强弱，可能用于识别短期动量与中期趋势之间的背离或协同效应。
    因子应用场景：
    1. 市场情绪分析：通过比较不同时间窗口下的交易量变化分位数，评估市场情绪的短期和长期变化趋势。
    2. 资金流动监测：捕捉不同周期下的资金流动信号，识别资金流入和流出的加速或减速。
    3. 趋势识别：揭示短期动量与中期趋势之间的背离或协同效应，辅助判断市场趋势的可靠性。
    """
    # 1. 计算 ts_delta(volume, 3)
    data_ts_delta_volume = ts_delta(data['vol'], 3)
    # 2. 计算 ts_quantile(ts_delta(volume, 3), 240)
    data_ts_quantile_volume = ts_quantile(data_ts_delta_volume, 240)
    # 3. 计算 ts_delta(vol, 5)
    data_ts_delta_vol = ts_delta(data['vol'], 5)
    # 4. 计算 ts_quantile(ts_delta(vol, 5), 120)
    data_ts_quantile_vol = ts_quantile(data_ts_delta_vol, 120)
    # 5. 计算 divide(ts_quantile(ts_delta(volume, 3), 240), ts_quantile(ts_delta(vol, 5), 120))
    factor = divide(data_ts_quantile_volume, data_ts_quantile_vol)

    del data_ts_delta_volume
    del data_ts_quantile_volume
    del data_ts_delta_vol
    del data_ts_quantile_vol
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()