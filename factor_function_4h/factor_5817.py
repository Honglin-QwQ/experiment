import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_kurtosis, ts_rank, ts_decay_linear, adv, log, min, multiply, rank, subtract

def factor_5817(data, **kwargs):
    """
    数学表达式: subtract(multiply(rank(ts_kurtosis(vol, 15)), ts_rank(ts_decay_linear(adv(vol, 25), 15), 7)), min(log(adv(vol, 25)), 12))
    中文描述: 该因子结合了成交量的峰度、线性衰减的排名以及平均成交量的对数，旨在捕捉市场中成交量的异常波动和趋势性变化。具体而言，它计算了过去15天成交量峰度的全市场排名，并乘以过去15天25日平均成交量线性衰减值的7日时间序列排名。最后，减去25日平均成交量对数的最小值（限制在12以内）。高因子值可能表明股票近期成交量呈现尖峰状分布，且近期平均成交量有明显的线性衰减趋势，同时平均成交量水平适中。这可能预示着市场对该股票的关注度正在发生变化，或存在潜在的交易机会。相较于参考因子，本因子调整了时间窗口和常数，并使用了更长的平均成交量周期，旨在捕捉更长期和更稳定的成交量特征。
    因子应用场景：
    1. 异常波动检测：用于识别成交量出现异常尖峰的股票。
    2. 趋势变化识别：辅助判断成交量衰减趋势明显的股票。
    3. 潜在机会发现：结合成交量特征，寻找市场关注度变化的股票，挖掘潜在交易机会。
    """
    # 1. 计算 ts_kurtosis(vol, 15)
    data_ts_kurtosis = ts_kurtosis(data['vol'], 15)
    # 2. 计算 rank(ts_kurtosis(vol, 15))
    data_rank_ts_kurtosis = rank(data_ts_kurtosis, 2)
    # 3. 计算 adv(vol, 25)
    data_adv = adv(data['vol'], 25)
    # 4. 计算 ts_decay_linear(adv(vol, 25), 15)
    data_ts_decay_linear = ts_decay_linear(data_adv, 15)
    # 5. 计算 ts_rank(ts_decay_linear(adv(vol, 25), 15), 7)
    data_ts_rank = ts_rank(data_ts_decay_linear, 7)
    # 6. 计算 multiply(rank(ts_kurtosis(vol, 15)), ts_rank(ts_decay_linear(adv(vol, 25), 15), 7))
    data_multiply = multiply(data_rank_ts_kurtosis, data_ts_rank)
    # 7. 计算 log(adv(vol, 25))
    data_log_adv = log(data_adv)
    # 8. 计算 min(log(adv(vol, 25)), 12)
    data_min = min(data_log_adv, 12)
    # 9. 计算 subtract(multiply(rank(ts_kurtosis(vol, 15)), ts_rank(ts_decay_linear(adv(vol, 25), 15), 7)), min(log(adv(vol, 25)), 12))
    factor = subtract(data_multiply, data_min)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()