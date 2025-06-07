import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_delta, ts_decay_linear, ts_max, ts_rank, adv,indneutralize
import pandas as pd
import numpy as np

def factor_0075(data, **kwargs):
    """
    数学表达式: (ts_max(rank(ts_decay_linear(ts_delta(vwap, 1.24383), 11.8259)), ts_rank(ts_decay_linear(ts_rank(ts_corr(indneutralize(low, IndClass.sector), adv81, 8.14941), 19.569), 17.1543), 19.383)) * -1) 
    中文描述: 该因子首先计算过去11.8259天成交量加权平均价(vwap)的1.24383期差分的线性衰减值，然后计算该衰减值的过去一段时间内的最大值排名；同时，因子还计算了行业中性化后的最低价与过去8.14941天平均成交额的相关系数，对该相关系数进行排名，再进行线性衰减，然后再次排名，再进行线性衰减，最后再次排名；将这两个排名相乘，并取反。该因子试图捕捉量价变化趋势与行业调整后的价格动量之间的反向关系，可能用于识别超买超卖机会，构建对冲策略，或者作为量化选股模型中的一个负向指标。
    因子应用场景：
    1. 超买超卖识别： 通过量价变化趋势与行业调整后的价格动量之间的反向关系，识别超买超卖的机会。
    2. 对冲策略构建： 用于构建对冲策略，通过捕捉市场中存在的反向关系来降低风险。
    3. 量化选股： 作为量化选股模型中的一个负向指标，过滤掉不符合条件的股票。
    """
    # 1. 计算 ts_delta(vwap, 1.24383)
    data_ts_delta_vwap = ts_delta(data['vwap'], 1.24383)
    # 2. 计算 ts_decay_linear(ts_delta(vwap, 1.24383), 11.8259)
    data_ts_decay_linear_delta = ts_decay_linear(data_ts_delta_vwap, 11.8259)
    # 3. 计算 rank(ts_decay_linear(ts_delta(vwap, 1.24383), 11.8259))
    data_rank_decay = rank(data_ts_decay_linear_delta, 2)
    # 4. 计算 ts_max(rank(ts_decay_linear(ts_delta(vwap, 1.24383), 11.8259)))
    data_ts_max_rank_decay = ts_max(data_rank_decay, 10)



    # 5. 计算 indneutralize(low, IndClass.sector)
    data_indneutralize_low = indneutralize(data['low'], data['industry'])
    # 6. 计算 adv(amount, 8.14941)
    data_adv = adv(data['amount'], 81)
    # 7. 计算 ts_corr(indneutralize(low, IndClass.sector), adv81, 8.14941)
    data_ts_corr = ts_corr(data_indneutralize_low, data_adv, 8.14941)
    # 8. 计算 ts_rank(ts_corr(indneutralize(low, IndClass.sector), adv81, 8.14941), 19.569)
    data_ts_rank_corr = ts_rank(data_ts_corr, 19.569)
    # 9. 计算 ts_decay_linear(ts_rank(ts_corr(indneutralize(low, IndClass.sector), adv81, 8.14941), 19.569), 17.1543)
    data_ts_decay_linear_rank_corr = ts_decay_linear(data_ts_rank_corr, 17.1543)
    # 10. 计算 ts_rank(ts_decay_linear(ts_rank(ts_corr(indneutralize(low, IndClass.sector), adv81, 8.14941), 19.569), 17.1543), 19.383)
    data_ts_rank_decay_rank_corr = ts_rank(data_ts_decay_linear_rank_corr, 19.383)

    # 11. 计算 (ts_max(rank(ts_decay_linear(ts_delta(vwap, 1.24383), 11.8259)), ts_rank(ts_decay_linear(ts_rank(ts_corr(indneutralize(low, IndClass.sector), adv81, 8.14941), 19.569), 17.1543), 19.383)) * -1)
    factor = (data_ts_max_rank_decay + data_ts_rank_decay_rank_corr) * -1

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()