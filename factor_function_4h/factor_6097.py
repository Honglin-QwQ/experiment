import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_6097(data, **kwargs):
    """
    因子名称: Scaled_Volume_Price_Correlation_Decay_58595
    数学表达式: ts_decay_exp_window(ts_corr(close, vol, 10), factor = 0.7) * scale(ts_mean(amount, 5))
    中文描述: 该因子计算了过去10天收盘价与交易量的相关性的指数衰减加权平均值，并将其与过去5天平均交易额的标准化值相乘。收盘价与交易量的相关性可以反映价格变动与交易活跃度之间的关系。通过指数衰减加权，近期的数据对相关性的影响更大，更及时地捕捉市场变化。将相关性与标准化后的短期平均交易额相乘，进一步考虑了市场的整体流动性和关注度，并对交易额进行了缩放，使其与其他部分因子值具有可比性。创新点在于结合了指数衰减相关性计算和标准化交易额加权，旨在识别那些近期量价关系显著且交易活跃的股票，可能预示着潜在的价格趋势。相较于历史因子，使用ts_decay_exp_window代替简单的ts_corr，使得因子对近期数据更敏感；使用scale对ts_mean(amount, 5)进行标准化，解决了历史因子中直接乘以amount均值可能导致的量纲问题，使因子值更稳定和可比。此外，ts_decay_exp_window和scale都是改进建议中提到的可以提升因子的操作符。
    因子应用场景：
    1. 量价关系分析：用于识别量价关系近期较为显著的股票。
    2. 趋势判断：可能预示潜在的价格趋势，辅助判断股票的走势。
    3. 市场活跃度考量：结合交易额信息，筛选出交易活跃且量价关系密切的股票。
    """
    # 1. 计算 ts_corr(close, vol, 10)
    data_ts_corr = ts_corr(data['close'], data['vol'], 10)
    # 2. 计算 ts_decay_exp_window(ts_corr(close, vol, 10), factor = 0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_corr, factor = 0.7)
    # 3. 计算 ts_mean(amount, 5)
    data_ts_mean = ts_mean(data['amount'], 5)
    # 4. 计算 scale(ts_mean(amount, 5))
    data_scale = scale(data_ts_mean)
    # 5. 计算 ts_decay_exp_window(ts_corr(close, vol, 10), factor = 0.7) * scale(ts_mean(amount, 5))
    factor = data_ts_decay_exp_window * data_scale

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()