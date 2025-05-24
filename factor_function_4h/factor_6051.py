import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, rank

def factor_6051(data, **kwargs):
    """
    因子名称: Price_Volume_Volatility_Divergence_Rank_61637
    数学表达式: rank(ts_std_dev(close, 20)) - rank(ts_std_dev(vol, 20))
    中文描述: 该因子计算了过去20天收盘价标准差的排名与过去20天成交量标准差的排名之差。标准差衡量了价格或成交量的波动性。通过计算两者波动性排名的差值，该因子旨在捕捉价格波动与成交量波动之间的相对强弱关系。如果价格波动排名远高于成交量波动排名，可能表明价格变动在缺乏成交量支撑的情况下发生，反之亦然。这可以用于识别价格趋势的健康程度或潜在的背离信号。相较于参考因子，创新点在于使用了波动率（标准差）作为核心度量，并直接比较其排名差异，结构更简洁，逻辑更直观。同时，结合了历史输出的评估结果，该因子避免了过于复杂的计算，专注于捕捉价格和成交量波动性的相对关系，希望通过简化和聚焦来提升预测能力和稳定性。
    因子应用场景：
    1. 背离信号识别：用于识别价格和成交量波动之间的背离，辅助判断趋势的可靠性。
    2. 趋势强度评估：评估价格趋势的健康程度，成交量波动是否支持价格波动。
    """
    # 1. 计算 ts_std_dev(close, 20)
    data_ts_std_dev_close = ts_std_dev(data['close'], 20)
    # 2. 计算 rank(ts_std_dev(close, 20))
    data_rank_close = rank(data_ts_std_dev_close, 2)
    # 3. 计算 ts_std_dev(vol, 20)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], 20)
    # 4. 计算 rank(ts_std_dev(vol, 20))
    data_rank_vol = rank(data_ts_std_dev_vol, 2)
    # 5. 计算 rank(ts_std_dev(close, 20)) - rank(ts_std_dev(vol, 20))
    factor = data_rank_close - data_rank_vol

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()