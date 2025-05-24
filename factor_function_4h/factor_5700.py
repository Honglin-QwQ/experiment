import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_delta, ts_std_dev

def factor_5700(data, **kwargs):
    """
    因子名称: VolumeVolatilityDeltaRatio_35815
    数学表达式: divide(ts_delta(ts_std_dev(vol, 120), 240), ts_delta(ts_std_dev(close, 120), 240))
    中文描述: 该因子计算了过去120天成交量标准差在过去240天的变化量与过去120天收盘价标准差在过去240天的变化量之比。它旨在捕捉成交量波动性相对于价格波动性的长期变化趋势。当成交量波动性增长快于价格波动性时，可能预示着市场情绪的剧烈变化或潜在的趋势反转。创新点在于结合了两个不同指标（成交量和收盘价）的波动性，并考察了它们在长期时间窗口内的相对变化，以识别市场结构的变化。
    因子应用场景：
    1. 市场情绪监测：用于监测成交量波动性相对于价格波动性的变化，辅助判断市场情绪。
    2. 趋势反转识别：当成交量波动性增长快于价格波动性时，可能预示潜在的趋势反转。
    """
    # 1. 计算 ts_std_dev(vol, 120)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], 120)
    # 2. 计算 ts_delta(ts_std_dev(vol, 120), 240)
    data_ts_delta_vol = ts_delta(data_ts_std_dev_vol, 240)
    # 3. 计算 ts_std_dev(close, 120)
    data_ts_std_dev_close = ts_std_dev(data['close'], 120)
    # 4. 计算 ts_delta(ts_std_dev(close, 120), 240)
    data_ts_delta_close = ts_delta(data_ts_std_dev_close, 240)
    # 5. 计算 divide(ts_delta(ts_std_dev(vol, 120), 240), ts_delta(ts_std_dev(close, 120), 240))
    factor = divide(data_ts_delta_vol, data_ts_delta_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()