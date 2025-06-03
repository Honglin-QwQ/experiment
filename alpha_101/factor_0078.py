import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_delta, multiply, add,indneutralize, ts_rank,adv
import pandas as pd

def factor_0078(data, **kwargs):
    """
    数学表达式: (rank(ts_delta(indneutralize(((close * 0.60733) + (open * (1 - 0.60733))), IndClass.sector), 1.23438)) < rank(ts_corr(ts_rank(vwap, 3.60973), ts_rank(adv150, 9.18637), 14.6644)))
    中文描述: 该因子计算股票排序值的大小关系，左侧是对过去一天多头组合收益进行行业中性化处理后的变化量进行排序，右侧是对成交量加权平均价和150日平均成交额进行排序并计算相关性后的排序，因子值大代表股票短期超额收益变化较小且成交量价关系稳定。
    应用场景：
    1. 选股策略：选择因子值较大的股票，预期这些股票短期表现稳定。
    2. 对冲策略：构建多空组合，做多因子值大的股票，做空因子值小的股票，对冲市场风险。
    3. 风险管理：监控因子值异常变动的股票，可能预示着股票基本面或市场情绪发生变化。
    """
    # 1. 计算 (close * 0.60733)
    data['close_weighted'] = multiply(data['close'], 0.60733)
    # 2. 计算 (open * (1 - 0.60733))
    data['open_weighted'] = multiply(data['open'], (1 - 0.60733))
    # 3. 计算 ((close * 0.60733) + (open * (1 - 0.60733)))
    data['portfolio_returns'] = add(data['close_weighted'], data['open_weighted'])


    data['neutralized_returns'] = indneutralize(data['portfolio_returns'] ,data['industry'])

    # 5. 计算 ts_delta(indneutralize(((close * 0.60733) + (open * (1 - 0.60733))), IndClass.sector), 1.23438)
    data['ts_delta_returns'] = ts_delta(data['neutralized_returns'], d = 1)

    # 6. 计算 rank(ts_delta(indneutralize(((close * 0.60733) + (open * (1 - 0.60733))), IndClass.sector), 1.23438))
    data['rank_left'] = rank(data['ts_delta_returns'])

    # 7. 计算 ts_rank(vwap, 3.60973)
    data['ts_rank_vwap'] = ts_rank(data['vwap'], d = 4)

    # 8. 计算 adv150
    data['adv150'] = adv(data['vol'],150)

    # 9. 计算 ts_rank(adv150, 9.18637)
    data['ts_rank_adv150'] = ts_rank(data['adv150'], d = 9)

    # 10. 计算 ts_corr(ts_rank(vwap, 3.60973), ts_rank(adv150, 9.18637), 14.6644)
    data['ts_corr_vwap_adv150'] = ts_corr(data['ts_rank_vwap'], data['ts_rank_adv150'], d = 15)

    # 11. 计算 rank(ts_corr(ts_rank(vwap, 3.60973), ts_rank(adv150, 9.18637), 14.6644))
    data['rank_right'] = rank(data['ts_corr_vwap_adv150'])

    # 12. 计算 (rank(ts_delta(indneutralize(((close * 0.60733) + (open * (1 - 0.60733))), IndClass.sector), 1.23438)) < rank(ts_corr(ts_rank(vwap, 3.60973), ts_rank(adv150, 9.18637), 14.6644)))
    factor = (data['rank_left'] < data['rank_right']).astype(int)

    # 删除中间变量
    del data['close_weighted']
    del data['open_weighted']
    del data['portfolio_returns']
    del data['neutralized_returns']
    del data['ts_delta_returns']
    del data['rank_left']
    del data['ts_rank_vwap']
    del data['adv150']
    del data['ts_rank_adv150']
    del data['ts_corr_vwap_adv150']
    del data['rank_right']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()