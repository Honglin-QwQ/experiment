import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, rank, ts_corr, ts_std_dev, ts_delta, ts_rank, ts_skewness

def factor_5793(data, **kwargs):
    """
    因子名称: Flow_Volatility_Skew_Decay_39587
    数学表达式: ts_decay_exp_window(rank(ts_corr(tbase, amount, 10)) * ts_std_dev(ts_delta(close, 1), 15), 0.7) - ts_rank(ts_skewness(vol, 10), 5)
    中文描述: 该因子旨在捕捉主动买入流量与交易额相关性、价格波动率和交易量偏度的综合衰减动量。它首先计算主动买入基础币种数量与交易额在过去10天的相关性排名，并乘以收盘价日度变化的15日标准差，反映买卖力量与交易规模相关性对短期价格波动的影响。然后对这个乘积应用指数衰减加权平均，赋予近期数据更高的权重，捕捉动量的衰减特征。最后减去交易量在过去10天的偏度在过去5天内的排名，引入对交易量极端波动的考量。高因子值可能表明近期买入力量与交易额正相关性较强且价格波动适中，同时交易量偏度较低，可能预示着资金流入推动下的温和上涨动能。
    因子应用场景：
    1. 动量分析：识别具有资金流入推动的温和上涨动能的股票。
    2. 风险管理：评估市场中买卖力量与交易规模相关性对短期价格波动的影响。
    3. 交易量分析：结合交易量偏度，识别交易量分布的极端波动情况。
    """
    # 1. 计算 ts_corr(tbase, amount, 10)
    data_ts_corr = ts_corr(data['tbase'], data['amount'], 10)
    # 2. 计算 rank(ts_corr(tbase, amount, 10))
    data_rank = rank(data_ts_corr, 2)
    # 3. 计算 ts_delta(close, 1)
    data_ts_delta = ts_delta(data['close'], 1)
    # 4. 计算 ts_std_dev(ts_delta(close, 1), 15)
    data_ts_std_dev = ts_std_dev(data_ts_delta, 15)
    # 5. 计算 rank(ts_corr(tbase, amount, 10)) * ts_std_dev(ts_delta(close, 1), 15)
    data_multiply = data_rank * data_ts_std_dev
    # 6. 计算 ts_decay_exp_window(rank(ts_corr(tbase, amount, 10)) * ts_std_dev(ts_delta(close, 1), 15), 0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_multiply, d = 6, factor = 0.7)
    # 7. 计算 ts_skewness(vol, 10)
    data_ts_skewness = ts_skewness(data['vol'], 10)
    # 8. 计算 ts_rank(ts_skewness(vol, 10), 5)
    data_ts_rank = ts_rank(data_ts_skewness, 5)
    # 9. 计算 ts_decay_exp_window(rank(ts_corr(tbase, amount, 10)) * ts_std_dev(ts_delta(close, 1), 15), 0.7) - ts_rank(ts_skewness(vol, 10), 5)
    factor = data_ts_decay_exp_window - data_ts_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()