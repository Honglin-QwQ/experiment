import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_delta, ts_rank, ts_decay_linear, adv, log, ts_corr, min

def factor_5582(data, **kwargs):
    """
    因子名称: factor_volume_price_momentum_58821
    数学表达式: rank(ts_delta(close, 5)) * ts_rank(ts_decay_linear(adv(vol, 10), 5), 3) - min(log(adv(amount, 20)), 8) + ts_corr(ts_delta(high, 2), vol, 5)
    中文描述: 该因子结合了价格动量、成交量衰减和量价相关性，旨在识别具有持续上涨潜力的股票。它在历史因子基础上进行了改进，主要体现在以下几个方面：

    1.  **价格动量增强：** 使用`rank(ts_delta(close, 5))`来衡量过去5天收盘价的变化幅度，捕捉短期价格动量。
    2.  **成交量衰减加速：** 使用`ts_decay_linear(adv(vol, 10), 5)`计算过去5天平均成交量的线性衰减值，并使用`ts_rank`对衰减值进行排序，强化了对近期成交量变化的敏感性。
    3.  **量价相关性：** 使用`ts_corr(ts_delta(high, 2), vol, 5)`计算过去5天最高价变化与成交量的相关性，捕捉量价关系的短期变化。
    4.  **异常值控制：** 使用`min(log(adv(amount, 20)), 8)`对成交额的对数进行截断，限制异常值的影响。

    该因子通过结合价格动量、成交量变化和量价关系，能够更全面地评估股票的交易活跃度和潜在的投资价值。适用于寻找短期量价关系突变且具有上涨趋势的股票。
    因子应用场景：
    1. 识别具有持续上涨潜力的股票。
    2. 寻找短期量价关系突变且具有上涨趋势的股票。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], d = 5)
    # 2. 计算 rank(ts_delta(close, 5))
    factor1 = rank(data_ts_delta_close)
    # 3. 计算 adv(vol, 10)
    data_adv_vol = adv(data['vol'], d = 10)
    # 4. 计算 ts_decay_linear(adv(vol, 10), 5)
    data_ts_decay_linear = ts_decay_linear(data_adv_vol, d = 5)
    # 5. 计算 ts_rank(ts_decay_linear(adv(vol, 10), 5), 3)
    factor2 = ts_rank(data_ts_decay_linear, d = 5, constant = 3)
    # 6. 计算 adv(amount, 20)
    data_adv_amount = adv(data['amount'], d = 20)
    # 7. 计算 log(adv(amount, 20))
    data_log_adv_amount = log(data_adv_amount)
    # 8. 计算 min(log(adv(amount, 20)), 8)
    factor3 = min(data_log_adv_amount, 8)
    # 9. 计算 ts_delta(high, 2)
    data_ts_delta_high = ts_delta(data['high'], d = 2)
    # 10. 计算 ts_corr(ts_delta(high, 2), vol, 5)
    factor4 = ts_corr(data_ts_delta_high, data['vol'], d = 5)
    # 11. 计算 rank(ts_delta(close, 5)) * ts_rank(ts_decay_linear(adv(vol, 10), 5), 3) - min(log(adv(amount, 20)), 8) + ts_corr(ts_delta(high, 2), vol, 5)
    factor = factor1 * factor2 - factor3 + factor4

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()