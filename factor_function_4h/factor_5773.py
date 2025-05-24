import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_std_dev

def factor_5773(data, **kwargs):
    """
    因子名称: Volatility_Skew_Divergence_15134
    数学表达式: ts_skewness(ts_std_dev(close, 10), 20) - ts_skewness(ts_std_dev(volume, 10), 20)
    中文描述: 该因子计算过去20天内，收盘价在过去10天的标准差的偏度与成交量在过去10天的标准差的偏度之间的差值。它旨在捕捉价格波动和成交量波动分布形态的差异。正值可能表明价格波动分布更偏向正向极端值，而成交量波动分布更偏向负向极端值，反之亦然。这种波动分布的背离可能预示着市场情绪或结构的变化。相较于简单的相关性，该因子引入了偏度来分析波动的分布特征，提供更精细的市场动态洞察，并参考了历史评估中对波动率和成交量的关注以及对更复杂统计指标的建议。
    因子应用场景：
    1. 市场情绪分析： 通过观察价格波动和成交量波动偏度的差异，可以辅助判断市场是处于乐观还是恐慌状态。
    2. 趋势反转预测： 当价格波动偏度与成交量波动偏度出现显著背离时，可能预示着当前趋势即将发生反转。
    3. 量价关系研究： 因子可以用于量化分析量价关系，例如，当价格波动偏度较高但成交量波动偏度较低时，可能意味着市场存在潜在的上涨动力。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev_close = ts_std_dev(data['close'], 10)
    # 2. 计算 ts_skewness(ts_std_dev(close, 10), 20)
    data_ts_skewness_close = ts_skewness(data_ts_std_dev_close, 20)
    # 3. 计算 ts_std_dev(volume, 10)
    data_ts_std_dev_volume = ts_std_dev(data['vol'], 10)
    # 4. 计算 ts_skewness(ts_std_dev(volume, 10), 20)
    data_ts_skewness_volume = ts_skewness(data_ts_std_dev_volume, 20)
    # 5. 计算 ts_skewness(ts_std_dev(close, 10), 20) - ts_skewness(ts_std_dev(volume, 10), 20)
    factor = data_ts_skewness_close - data_ts_skewness_volume

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()