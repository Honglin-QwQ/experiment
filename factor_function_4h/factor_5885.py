import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, divide, ts_mean, ts_delta

def factor_5885(data, **kwargs):
    """
    因子名称: VolatilityMomentumRelativeStrength_26818
    数学表达式: ts_rank(divide(ts_mean(ts_delta(vol, 5), 5), ts_mean(vol, 20)), 60)
    中文描述: 该因子计算过去5日成交量变化率的5日均值与过去20日成交量均值的比值，并对该比值在过去60天内进行排名。它旨在捕捉成交量动量的相对强度。高排名可能表明成交量近期加速上升，市场活跃度增强；低排名则可能表示成交量动能减弱。相较于简单的波动率或波动率比率，该因子通过引入成交量变化率和时间序列排名，更精细地衡量了成交量动能的相对强弱，并考虑了历史表现的对比，具有更强的创新性。这可以用于识别潜在的趋势形成或反转信号，并结合历史排名提供更全面的分析视角。
    因子应用场景：
    1. 动量识别：识别成交量加速上升的股票，可能预示着价格上涨的趋势。
    2. 市场活跃度：衡量市场整体的活跃程度，高排名可能表明市场参与者情绪高涨。
    3. 趋势反转信号：低排名可能暗示成交量动能减弱，潜在的价格下跌风险。
    """
    # 1. 计算 ts_delta(vol, 5)
    data_ts_delta_vol = ts_delta(data['vol'], 5)
    # 2. 计算 ts_mean(ts_delta(vol, 5), 5)
    data_ts_mean_delta_vol = ts_mean(data_ts_delta_vol, 5)
    # 3. 计算 ts_mean(vol, 20)
    data_ts_mean_vol = ts_mean(data['vol'], 20)
    # 4. 计算 divide(ts_mean(ts_delta(vol, 5), 5), ts_mean(vol, 20))
    data_divide = divide(data_ts_mean_delta_vol, data_ts_mean_vol)
    # 5. 计算 ts_rank(divide(ts_mean(ts_delta(vol, 5), 5), ts_mean(vol, 20)), 60)
    factor = ts_rank(data_divide, 60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()