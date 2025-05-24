import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_rank, ts_std_dev, ts_delta

def factor_5921(data, **kwargs):
    """
    因子名称: Vol_Vol_Corr_Rank_Delta_36455
    数学表达式: ts_corr(ts_rank(ts_std_dev(vol, 10), 15), ts_delta(vol, 5), 10)
    中文描述: 该因子旨在捕捉成交量波动率的相对排名与中期成交量变化之间的相关性。首先，计算过去10天成交量的标准差，衡量短期成交量波动性，并对其进行15日时间序列排名，得到成交量波动性的相对强度。然后，计算过去5天成交量的差值，衡量中期成交量变化。最后，计算这两个序列在过去10天内的相关性。创新点在于：1. 将成交量波动率和中期成交量变化结合，而非仅关注价格。2. 对成交量波动率进行了时间序列排名，使其更具可比性。3. 使用了ts_corr来衡量这两个指标之间的动态关系。高相关性可能表明成交量波动性上升的相对强度与中期成交量上涨同步，而低相关性或负相关性可能预示着成交量波动性上升与成交量下跌或盘整同时发生，这可能用于识别市场参与者情绪的转变或成交量趋势的潜在反转。
    应用场景：
    1. 趋势跟踪：当相关性较高且为正时，可能加强成交量趋势信号；当相关性较低或为负时，可能预示成交量趋势减弱或反转。
    2. 动量策略辅助：结合成交量动量指标，判断动量是否可持续或面临阻力。
    3. 风险管理：高成交量波动性与成交量下跌的正相关性可能指示市场风险增加。
    """
    # 1. 计算 ts_std_dev(vol, 10)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], 10)
    # 2. 计算 ts_rank(ts_std_dev(vol, 10), 15)
    data_ts_rank_ts_std_dev_vol = ts_rank(data_ts_std_dev_vol, 15)
    # 3. 计算 ts_delta(vol, 5)
    data_ts_delta_vol = ts_delta(data['vol'], 5)
    # 4. 计算 ts_corr(ts_rank(ts_std_dev(vol, 10), 15), ts_delta(vol, 5), 10)
    factor = ts_corr(data_ts_rank_ts_std_dev_vol, data_ts_delta_vol, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()