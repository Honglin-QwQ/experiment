import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_min, ts_product, ts_scale, log, ts_sum, ts_delta, ts_rank, ts_delay, multiply, add

def factor_0028(data, **kwargs):
    """
    数学表达式: (ts_min(ts_product(rank(rank(ts_scale(log(ts_sum(ts_min(rank(rank((-1 * rank(ts_delta((close - 1), 5))))), 2), 1))))), 1), 5) + ts_rank(ts_delay((-1 * returns), 6), 5))
    中文描述: 该因子计算了两个部分的加和：第一部分是过去5天内，对一个复杂时间序列进行最小值计算的结果；这个复杂时间序列是先计算过去一段时间内收盘价差值的负排名的排名，再取过去2天最小值，再求和，取对数，标准化，再进行两次排名，最后计算过去1天的最小值；第二部分是过去5天内，负收益率滞后6期的排名。整体而言，该因子试图捕捉短期价格动量和中期反转效应的结合。
    因子应用场景：
    1. 短线择时：结合动量和反转信号，识别短期超买超卖机会。
    2. 趋势跟踪：作为趋势跟踪策略的辅助因子，验证趋势的可靠性。
    3. 风险管理：用于识别高风险股票，避免参与过度拥挤的交易。
    """
    # 第一部分：
    # 1. 计算 (close - 1)
    close_minus_1 = data['close'] - 1
    # 2. 计算 ts_delta((close - 1), 5)
    ts_delta_close_minus_1 = ts_delta(close_minus_1, 5)
    # 3. 计算 (-1 * rank(ts_delta((close - 1), 5)))
    neg_rank_ts_delta = multiply(-1, rank(ts_delta_close_minus_1, 2))
    # 4. 计算 rank((-1 * rank(ts_delta((close - 1), 5))))
    rank_neg_rank_ts_delta = rank(neg_rank_ts_delta, 2)
    # 5. 计算 rank(rank((-1 * rank(ts_delta((close - 1), 5)))))
    rank_rank_neg_rank_ts_delta = rank(rank_neg_rank_ts_delta, 2)
    # 6. 计算 ts_min(rank(rank((-1 * rank(ts_delta((close - 1), 5))))), 2)
    ts_min_rank_rank = ts_min(rank_rank_neg_rank_ts_delta, 2)
    # 7. 计算 ts_sum(ts_min(rank(rank((-1 * rank(ts_delta((close - 1), 5))))), 2), 1)
    ts_sum_ts_min_rank_rank = ts_sum(ts_min_rank_rank, 1)
    # 8. 计算 log(ts_sum(ts_min(rank(rank((-1 * rank(ts_delta((close - 1), 5))))), 2), 1))
    log_ts_sum = log(ts_sum_ts_min_rank_rank)
    # 9. 计算 ts_scale(log(ts_sum(ts_min(rank(rank((-1 * rank(ts_delta((close - 1), 5))))), 2), 1)))
    ts_scale_log_ts_sum = ts_scale(log_ts_sum, 6)
    # 10. 计算 rank(ts_scale(log(ts_sum(ts_min(rank(rank((-1 * rank(ts_delta((close - 1), 5))))), 2), 1))))
    rank_ts_scale = rank(ts_scale_log_ts_sum, 2)
    # 11. 计算 rank(rank(ts_scale(log(ts_sum(ts_min(rank(rank((-1 * rank(ts_delta((close - 1), 5))))), 2), 1)))))
    rank_rank_ts_scale = rank(rank_ts_scale, 2)
    # 12. 计算 ts_product(rank(rank(ts_scale(log(ts_sum(ts_min(rank(rank((-1 * rank(ts_delta((close - 1), 5))))), 2), 1))))), 1), 5)
    ts_product_rank_rank = ts_product(rank_rank_ts_scale, 5)
    # 13. 计算 ts_min(ts_product(rank(rank(ts_scale(log(ts_sum(ts_min(rank(rank((-1 * rank(ts_delta((close - 1), 5))))), 2), 1))))), 1), 5), 5)
    ts_min_ts_product = ts_min(ts_product_rank_rank, 5)

    # 第二部分：
    # 1. 计算 (-1 * returns)
    neg_returns = multiply(-1, data['returns'])
    # 2. 计算 ts_delay((-1 * returns), 6)
    ts_delay_neg_returns = ts_delay(neg_returns, 6)
    # 3. 计算 ts_rank(ts_delay((-1 * returns), 6), 5)
    ts_rank_ts_delay = ts_rank(ts_delay_neg_returns, 5)

    # 两部分加和
    factor = add(ts_min_ts_product, ts_rank_ts_delay)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()