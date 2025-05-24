import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_corr, ts_returns

def factor_5624(data, **kwargs):
    """
    因子名称: factor_volume_returns_correlation_zscore_48945
    数学表达式: ts_zscore(ts_corr(vol, ts_returns(close, 5), 15), 45)
    中文描述: 该因子计算过去15天成交量与5日收益率的相关性，并计算该相关性在过去45天的Z-score。成交量与收益率的相关性反映了市场交易活跃程度与价格变化之间的关系，Z-score则衡量了当前相关性相对于过去一段时间的偏离程度。相比于之前的因子，该因子直接使用收益率而非价格，避免了信息熵计算可能带来的信息损失，并可能更直接地捕捉成交量和价格之间的联动关系。此外，通过调整相关性和Z-score的时间窗口，可以捕捉不同时间尺度的市场动态。
    因子应用场景：
    1. 市场情绪：当因子值较高时，可能表明市场情绪高涨，成交量与价格变化呈现正相关。
    2. 风险预警：当因子值异常偏离历史均值时，可能预示着市场风险的积累。
    """
    # 1. 计算 ts_returns(close, 5)
    data_ts_returns = ts_returns(data['close'], 5)
    # 2. 计算 ts_corr(vol, ts_returns(close, 5), 15)
    data_ts_corr = ts_corr(data['vol'], data_ts_returns, 15)
    # 3. 计算 ts_zscore(ts_corr(vol, ts_returns(close, 5), 15), 45)
    factor = ts_zscore(data_ts_corr, 45)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()