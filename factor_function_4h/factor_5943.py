import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_std_dev, adv

def factor_5943(data, **kwargs):
    """
    因子名称: VolatilityVolumeInteraction_62958
    数学表达式: ts_corr(ts_std_dev(close, 10), adv(vol, 15), 20)
    中文描述: 该因子旨在捕捉价格波动性和平均成交量之间的短期相关性。它首先计算过去10天收盘价的标准差（衡量价格波动性），然后计算过去15天的平均成交量。接着，计算这两个时间序列在过去20天内的相关系数。因子值越高，表明在过去一段时间内，价格波动性与平均成交量呈现更强的正相关关系，反之亦然。这可能用于识别市场情绪和交易活动的协同变化。
    因子应用场景：
    1. 市场情绪分析：当因子值较高时，表明价格波动性和成交量之间存在较强的正相关性，可能反映市场情绪高涨，投资者积极参与交易。
    2. 交易活动识别：通过观察因子值的变化，可以识别市场交易活动的协同变化，例如价格波动性增加伴随着成交量放大。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev_close = ts_std_dev(data['close'], 10)
    # 2. 计算 adv(vol, 15)
    data_adv_vol = adv(data['vol'], 15)
    # 3. 计算 ts_corr(ts_std_dev(close, 10), adv(vol, 15), 20)
    factor = ts_corr(data_ts_std_dev_close, data_adv_vol, 20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()