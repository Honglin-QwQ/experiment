import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, rank, adv, multiply

def factor_5910(data, **kwargs):
    """
    因子名称: TS_DecayExpWindow_Returns_Rank_AdvVol_96269
    数学表达式: ts_decay_exp_window(returns, 16, 0.7) * rank(adv(vol, 20))
    中文描述: 该因子旨在捕捉短期收益率的指数衰减趋势与长期平均交易量排名的结合效应。ts_decay_exp_window(returns, 16, 0.7)计算过去16天收益率的指数衰减加权平均值，赋予近期收益率更高的权重（衰减因子0.7），反映了近期收益率的持续性或反转迹象。rank(adv(vol, 20))计算过去20天平均交易量在所有股票中的排名，衡量股票的市场活跃度和关注度。将这两个值相乘，旨在识别那些近期收益率呈现一定趋势（无论是持续还是反转）且长期交易活跃度较高的股票。相较于参考因子和历史输出，该因子创新性地使用了指数衰减加权平均来捕捉收益率的时间序列特征，而非简单的时间索引或平均值，并且保留了交易量排名信息。通过赋予近期收益率更高的权重，该因子可能更能反映当前的市场情绪和动量，结合交易量排名，有望筛选出在市场关注度较高背景下，具有更明确短期收益趋势的股票。
    因子应用场景：
    1. 趋势识别：识别近期收益率呈现指数衰减趋势的股票。
    2. 活跃度筛选：结合交易量排名，筛选出市场关注度较高的股票。
    3. 动量策略：捕捉市场情绪和动量，辅助动量策略的构建。
    """
    # 1. 计算 ts_decay_exp_window(returns, 16, 0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data['returns'], d=16, factor=0.7)
    # 2. 计算 adv(vol, 20)
    data_adv = adv(data['vol'], d=20)
    # 3. 计算 rank(adv(vol, 20))
    data_rank = rank(data_adv)
    # 4. 计算 ts_decay_exp_window(returns, 16, 0.7) * rank(adv(vol, 20))
    factor = multiply(data_ts_decay_exp_window, data_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()