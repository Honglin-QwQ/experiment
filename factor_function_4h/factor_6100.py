import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_rank, ts_mean, adv, divide

def factor_6100(data, **kwargs):
    """
    因子名称: Vol_Rank_Momentum_Ratio_87805
    数学表达式: divide(ts_rank(vol, 87), ts_mean(adv(vol, 20), 51))
    中文描述: 该因子结合了交易量的短期时间序列排名和长期平均交易量均值，旨在捕捉市场流动性的相对变化。因子表达式为ts_rank(vol, 87)除以ts_mean(adv(vol, 20), 51)。分子计算过去87天内当前交易量的排名，反映短期交易量的相对强度。分母计算过去51天内20日平均交易量的均值，反映长期交易活跃度的平滑趋势。该因子通过计算短期交易量排名与长期平均交易量均值的比值，量化了当前交易量相对于长期平均交易量的相对活跃程度。较高的因子值可能表明当前交易量异常活跃，远超长期平均水平，可能预示着市场情绪的显著变化或资金的快速流入。较低的因子值则可能表明当前交易量相对低迷。该因子可以用于识别交易量异常活跃或低迷的股票，作为市场情绪、资金流向和潜在价格波动的参考指标。相较于简单的交易量排名或平均交易量，该因子通过结合短期排名和长期均值，提供了更全面的交易量分析视角，具有一定的创新性。
    因子应用场景：
    1. 识别交易量异常活跃或低迷的股票。
    2. 作为市场情绪、资金流向和潜在价格波动的参考指标。
    """
    # 1. 计算 ts_rank(vol, 87)
    data_ts_rank_vol = ts_rank(data['vol'], 87)
    # 2. 计算 adv(vol, 20)
    data_adv_vol = adv(data['vol'], 20)
    # 3. 计算 ts_mean(adv(vol, 20), 51)
    data_ts_mean_adv_vol = ts_mean(data_adv_vol, 51)
    # 4. 计算 divide(ts_rank(vol, 87), ts_mean(adv(vol, 20), 51))
    factor = divide(data_ts_rank_vol, data_ts_mean_adv_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()