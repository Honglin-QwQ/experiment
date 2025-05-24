import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_arg_max, rank, adv

def factor_5891(data, **kwargs):
    """
    因子名称: TS_ArgMax_Returns_Weighted_AvgVol_Rank_38025
    数学表达式: ts_arg_max(returns, 16) * rank(adv(vol, 20))
    中文描述: 该因子综合考虑了短期收益率的极值位置和长期平均交易量的排名。首先，ts_arg_max(returns, 16)计算过去16天内日收益率最高值出现的时间索引，反映了短期动量或反转的强度和时机。接着，rank(adv(vol, 20))计算过去20天平均交易量在所有股票中的排名，反映了该股票在市场中的活跃度和关注度。将这两个值相乘，旨在捕捉那些在短期内有过显著收益率波动（无论近期还是稍早）且长期交易活跃度较高的股票。创新点在于将时间序列极值位置信息与截面交易活跃度排名相结合，试图发现那些在市场关注度较高背景下，短期收益率出现过极端表现的股票，可能预示着潜在的投资机会或风险。相较于参考因子，该因子引入了交易量信息和截面排名，丰富了因子的维度和信息含量。
    因子应用场景：
    1. 动量捕捉：用于识别短期内收益率达到峰值，且交易活跃的股票，这些股票可能具有持续上涨的动能。
    2. 反转交易：在收益率达到峰值后，因子可能预示着超买状态，从而进行反转交易。
    3. 活跃度筛选：通过交易量排名，筛选出市场关注度高的股票，避免流动性差的股票。
    """
    # 1. 计算 ts_arg_max(returns, 16)
    data_ts_arg_max = ts_arg_max(data['returns'], d=16)
    # 2. 计算 adv(vol, 20)
    data_adv = adv(data['vol'], d=20)
    # 3. 计算 rank(adv(vol, 20))
    data_rank = rank(data_adv)
    # 4. 计算 ts_arg_max(returns, 16) * rank(adv(vol, 20))
    factor = data_ts_arg_max * data_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()