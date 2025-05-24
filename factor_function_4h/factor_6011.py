import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_corr, ts_delta

def factor_6011(data, **kwargs):
    """
    因子名称: VolPriceAccelerationCorrRank_98309
    数学表达式: ts_rank(ts_corr(delta(vol, 5), delta(delta(close, 3), 3), 20), 60)
    中文描述: 该因子计算短期成交量变化速度与价格加速度在一定时间窗口内的相关性，并对其进行时间序列排名。首先，使用delta(vol, 5)计算过去5天成交量的变化量，代表成交量变化的速度。接着，使用delta(delta(close, 3), 3)计算过去3天收盘价的加速度，代表价格变化的剧烈程度。然后，计算这两个序列在过去20天内的相关性 (ts_corr(delta(vol, 5), delta(delta(close, 3), 3), 20))。最后，对该相关性序列在过去60天内进行时间序列排名 (ts_rank(..., 60))。该因子旨在捕捉成交量变化速度与价格加速度之间的短期关系，并评估其在长期历史中的相对强度。创新点在于引入了价格加速度的概念，并结合成交量变化速度，通过相关性和排名来衡量市场情绪和动量的变化。这可能用于识别那些成交量和价格变化同步加速的股票，作为潜在的交易信号。相较于参考因子，该因子更关注变化的速度和加速度，而非简单的平均值和相关性差异，更具动态性。
    因子应用场景：
    1. 市场情绪识别：用于识别成交量和价格变化同步加速的股票，作为潜在的交易信号。
    2. 动量策略：结合成交量变化速度和价格加速度，衡量市场情绪和动量的变化。
    """
    # 1. 计算 delta(vol, 5)
    data_delta_vol = ts_delta(data['vol'], 5)
    # 2. 计算 delta(close, 3)
    data_delta_close_3 = ts_delta(data['close'], 3)
    # 3. 计算 delta(delta(close, 3), 3)
    data_delta_delta_close = ts_delta(data_delta_close_3, 3)
    # 4. 计算 ts_corr(delta(vol, 5), delta(delta(close, 3), 3), 20)
    data_ts_corr = ts_corr(data_delta_vol, data_delta_delta_close, 20)
    # 5. 计算 ts_rank(ts_corr(delta(vol, 5), delta(delta(close, 3), 3), 20), 60)
    factor = ts_rank(data_ts_corr, 60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()