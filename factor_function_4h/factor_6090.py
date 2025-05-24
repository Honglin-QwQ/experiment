import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delay, divide

def factor_6090(data, **kwargs):
    """
    因子名称: VolumeVolatilityTrendRatio_59949
    数学表达式: divide(ts_std_dev(vol, 12), ts_std_dev(ts_delay(vol, 1), 12))
    中文描述: 该因子计算当前成交量在过去12天内的标准差与前一日成交量在过去12天内的标准差之比。它旨在捕捉成交量波动性的短期趋势变化。如果该比率大于1，说明近期成交量波动性有所增加，可能预示着市场活跃度或不确定性上升；如果小于1，则说明成交量波动性趋于平缓。这可以用于识别潜在的价格突破或趋势反转信号。
    因子应用场景：
    1. 波动性趋势判断：用于判断成交量波动性是增加还是减少的趋势。
    2. 市场活跃度评估：比率大于1可能表明市场活跃度上升。
    3. 潜在信号识别：结合其他因子，辅助识别潜在的价格突破或趋势反转信号。
    """
    # 1. 计算 ts_std_dev(vol, 12)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], 12)
    # 2. 计算 ts_delay(vol, 1)
    data_ts_delay_vol = ts_delay(data['vol'], 1)
    # 3. 计算 ts_std_dev(ts_delay(vol, 1), 12)
    data_ts_std_dev_ts_delay_vol = ts_std_dev(data_ts_delay_vol, 12)
    # 4. 计算 divide(ts_std_dev(vol, 12), ts_std_dev(ts_delay(vol, 1), 12))
    factor = divide(data_ts_std_dev_vol, data_ts_std_dev_ts_delay_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()