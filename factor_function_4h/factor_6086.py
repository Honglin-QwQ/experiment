import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_6086(data, **kwargs):
    """
    因子名称: VolumePriceMomentumSkew_85223
    数学表达式: ts_scale(ts_co_skewness(vol, ts_delta(close, 5), 60)) - ts_scale(ts_skewness(amount, 90)) + ts_scale(ts_rank(trades, 30))
    中文描述: 该因子旨在捕捉成交量与价格动量之间的非对称关系、交易额的偏度以及交易活跃度的相对排名。第一部分计算成交量与5天价格变化率在过去60天内的协偏度，并进行时间序列标准化，捕捉量价关系中的非线性特征和方向性；第二部分计算交易额在过去90天内的偏度，并进行时间序列标准化后取负，衡量交易额分布的非对称性；第三部分计算交易笔数在过去30天内的排名，并进行时间序列标准化，反映交易活跃度的相对强弱。将这三部分结合，旨在从不同维度捕捉市场动态。创新点在于：1. 引入成交量与价格动量（ts_delta(close, 5)）的协偏度，而非简单的价格或成交量协偏度，更能体现量价配合对价格变化的非线性影响。2. 使用交易额的偏度而非峰度，关注交易额分布的非对称性，而非仅仅尾部风险。3. 结合了交易笔数的排名，引入了相对强弱的概念。这些创新点相较于参考因子在量价关系、交易额分析和活跃度衡量上提供了更丰富的视角。改进建议的采纳体现在：1. 改进了协偏度的计算逻辑，直接使用vol和ts_delta(close, 5)，避免了对数转换。2. 尝试了不同的高阶统计量（偏度代替峰度）。3. 引入了新的操作符 ts_delta 和 ts_rank。应用场景：1. 识别潜在的价格反转或趋势延续信号，高协偏度可能预示着量价配合下的价格动量变化。2. 分析交易额分布的异常，高偏度可能与异常交易行为相关。3. 结合交易笔数排名，判断市场活跃度是否支持当前的价格走势。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close_5 = ts_delta(data['close'], 5)
    # 2. 计算 ts_co_skewness(vol, ts_delta(close, 5), 60)
    data_ts_co_skewness = ts_co_skewness(data['vol'], data_ts_delta_close_5, 60)
    # 3. 计算 ts_scale(ts_co_skewness(vol, ts_delta(close, 5), 60))
    factor1 = ts_scale(data_ts_co_skewness)
    # 4. 计算 ts_skewness(amount, 90)
    data_ts_skewness = ts_skewness(data['amount'], 90)
    # 5. 计算 ts_scale(ts_skewness(amount, 90))
    factor2 = ts_scale(data_ts_skewness)
    # 6. 计算 ts_rank(trades, 30)
    data_ts_rank = ts_rank(data['trades'], 30)
    # 7. 计算 ts_scale(ts_rank(trades, 30))
    factor3 = ts_scale(data_ts_rank)
    # 8. 计算 ts_scale(ts_co_skewness(vol, ts_delta(close, 5), 60)) - ts_scale(ts_skewness(amount, 90)) + ts_scale(ts_rank(trades, 30))
    factor = factor1 - factor2 + factor3

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()