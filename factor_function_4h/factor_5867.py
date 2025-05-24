import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_std_dev, ts_mean, divide, ts_rank

def factor_5867(data, **kwargs):
    """
    因子名称: VolatilityTrend_VolumeAdjustedRank_18388
    数学表达式: ts_rank(divide(ts_std_dev(close, 40), ts_mean(vol, 40)), 60)
    中文描述: 该因子计算过去40天收盘价标准差与过去40天平均成交量的比值的过去60天时间序列排名。收盘价标准差衡量波动率，平均成交量反映市场活跃度。该因子通过结合波动率和成交量，并对其比值进行长期排名，旨在捕捉市场情绪和波动性在历史上的相对位置。相较于参考因子，该因子简化了波动率的计算，直接使用标准差而非其差值，并调整了时间窗口以寻找更稳定的信号。较高的因子值可能表明当前波动率相对于成交量处于历史高位，可能预示着潜在的市场转折点或异常波动。
    因子应用场景：
    1. 市场情绪捕捉：通过波动率与成交量的比值排名，辅助判断市场过热或恐慌状态。
    2. 潜在转折点识别：因子值较高可能预示着市场潜在的转折点。
    3. 波动性异常检测：用于发现相对于成交量而言波动性异常高的股票。
    """
    # 1. 计算 ts_std_dev(close, 40)
    data_ts_std_dev_close = ts_std_dev(data['close'], d=40)
    # 2. 计算 ts_mean(vol, 40)
    data_ts_mean_vol = ts_mean(data['vol'], d=40)
    # 3. 计算 divide(ts_std_dev(close, 40), ts_mean(vol, 40))
    data_divide = divide(data_ts_std_dev_close, data_ts_mean_vol)
    # 4. 计算 ts_rank(divide(ts_std_dev(close, 40), ts_mean(vol, 40)), 60)
    factor = ts_rank(data_divide, d=60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()