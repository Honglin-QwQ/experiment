import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_decay_linear, ts_delta, ts_scale, ts_corr, adv, sign, multiply, add

def factor_0030(data, **kwargs):
    """
    数学表达式: ((rank(rank(rank(ts_decay_linear((-1 * rank(rank(ts_delta(close, 10)))), 10)))) + rank((-1 * ts_delta(close, 3)))) + sign(ts_scale(ts_corr(adv20, low, 12))))
    中文描述: 该因子综合考虑了价格动量、成交量和时间衰减等因素。首先，计算过去10天收盘价变化率的排名，然后对排名结果再次排名，并进行线性衰减，最后再次排名，目的是捕捉短期价格加速下跌的股票。同时，计算过去3天收盘价变化率的排名，并取负数，反映短期价格下跌的股票。将这两个排名结果相加，增强了对价格下跌股票的识别。此外，计算过去12天平均成交额与最低价的相关性，并进行时间序列标准化，取其符号，用于判断成交量与价格走势的配合情况。最后，将价格动量和成交量的信息结合，构建最终的因子值。该因子可以应用于以下场景：1. 短期反转策略：寻找超跌反弹的股票。2. 动量衰减策略：识别动量开始减弱的股票，避免追高。3. 量价配合策略：验证价格下跌是否伴随成交量放大，提高选股的准确性。
    因子应用场景：
    1. 短期反转策略：寻找超跌反弹的股票。
    2. 动量衰减策略：识别动量开始减弱的股票，避免追高。
    3. 量价配合策略：验证价格下跌是否伴随成交量放大，提高选股的准确性。
    """
    # 1. 计算 ts_delta(close, 10)
    data_ts_delta_close_10 = ts_delta(data['close'], 10)
    # 2. 计算 rank(ts_delta(close, 10))
    data_rank_ts_delta_close_10 = rank(data_ts_delta_close_10, 2)
    # 3. 计算 rank(rank(ts_delta(close, 10)))
    data_rank_rank_ts_delta_close_10 = rank(data_rank_ts_delta_close_10, 2)
    # 4. 计算 -1 * rank(rank(ts_delta(close, 10)))
    data_multiply_minus_1 = multiply(-1, data_rank_rank_ts_delta_close_10, filter=False)
    # 5. 计算 ts_decay_linear((-1 * rank(rank(ts_delta(close, 10)))), 10)
    data_ts_decay_linear = ts_decay_linear(data_multiply_minus_1, 10)
    # 6. 计算 rank(ts_decay_linear((-1 * rank(rank(ts_delta(close, 10)))), 10))
    data_rank_ts_decay_linear = rank(data_ts_decay_linear, 2)
    # 7. 计算 rank(rank(ts_decay_linear((-1 * rank(rank(ts_delta(close, 10)))), 10)))
    data_rank_rank_ts_decay_linear = rank(data_rank_ts_decay_linear, 2)
    # 8. 计算 rank(rank(rank(ts_decay_linear((-1 * rank(rank(ts_delta(close, 10)))), 10))))
    data_rank_rank_rank_ts_decay_linear = rank(data_rank_rank_ts_decay_linear, 2)
    # 9. 计算 ts_delta(close, 3)
    data_ts_delta_close_3 = ts_delta(data['close'], 3)
    # 10. 计算 -1 * ts_delta(close, 3)
    data_multiply_minus_1_2 = multiply(-1, data_ts_delta_close_3, filter=False)
    # 11. 计算 rank((-1 * ts_delta(close, 3)))
    data_rank_multiply_minus_1_2 = rank(data_multiply_minus_1_2, 2)
    # 12. 计算 rank(rank(rank(ts_decay_linear((-1 * rank(rank(ts_delta(close, 10)))), 10)))) + rank((-1 * ts_delta(close, 3)))
    data_add_rank = add(data_rank_rank_rank_ts_decay_linear, data_rank_multiply_minus_1_2, filter=False)
    # 13. 计算 ts_corr(adv20, low, 12)
    data_adv20 = adv(data['vol'],20)
    data_ts_corr = ts_corr(data_adv20, data['low'], 12)
    # 14. 计算 ts_scale(ts_corr(adv20, low, 12))
    data_ts_scale = ts_scale(data_ts_corr)
    # 15. 计算 sign(ts_scale(ts_corr(adv20, low, 12)))
    data_sign_ts_scale = sign(data_ts_scale)
    # 16. 计算 (rank(rank(rank(ts_decay_linear((-1 * rank(rank(ts_delta(close, 10)))), 10)))) + rank((-1 * ts_delta(close, 3)))) + sign(ts_scale(ts_corr(adv20, low, 12))))
    factor = add(data_add_rank, data_sign_ts_scale, filter=False)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()