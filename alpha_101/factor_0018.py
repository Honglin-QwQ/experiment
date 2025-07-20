import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import sign, ts_delay, ts_delta, add, rank, ts_sum, multiply,subtract

def factor_0018(data, **kwargs):
    """
    数学表达式: ((-1 * sign(((close - ts_delay(close, 7)) + ts_delta(close, 7)))) * (1 + rank((1 + ts_sum(returns, 250))))) 
    中文描述: 该因子首先计算过去7天收盘价的变化，包括收盘价与7天前收盘价的差值以及7天内收盘价的变化量，并取其和的符号，若为正表示上涨，为负表示下跌，然后乘以-1，反转了这个方向。接着，计算过去250天收益率之和，加上1后进行排序，得到一个排序值，再加1，反映了长期收益累积的相对排名。最后，将反转后的涨跌方向信号乘以这个长期收益排名，形成最终的因子值。
    应用场景：
    1. 趋势反转策略：识别短期下跌但长期收益排名靠前的股票，可能存在反弹机会。
    2. 动量反转策略：捕捉短期价格动量与长期价值之间的背离。
    3. 风险调整收益策略：结合长期收益排名，过滤掉长期表现不佳的短期反弹股票。
    """
    # 1. 计算 ts_delay(close, 7)
    delay_close = ts_delay(data['close'], 7)
    # 2. 计算 (close - ts_delay(close, 7))
    sub_close = subtract(data['close'], delay_close)
    # 3. 计算 ts_delta(close, 7)
    delta_close = ts_delta(data['close'], 7)
    # 4. 计算 ((close - ts_delay(close, 7)) + ts_delta(close, 7))
    add_close = add(sub_close, delta_close)
    # 5. 计算 sign(((close - ts_delay(close, 7)) + ts_delta(close, 7)))
    sign_close = sign(add_close)
    # 6. 计算 -1 * sign(((close - ts_delay(close, 7)) + ts_delta(close, 7)))
    neg_sign_close = multiply(-1, sign_close)
    # 7. 计算 ts_sum(returns, 250)
    sum_returns = ts_sum(data['returns'], 250)
    # 8. 计算 (1 + ts_sum(returns, 250))
    add_sum_returns = add(1, sum_returns)
    # 9. 计算 rank((1 + ts_sum(returns, 250)))
    rank_sum_returns = rank(add_sum_returns)
    # 10. 计算 (1 + rank((1 + ts_sum(returns, 250))))
    add_rank_sum_returns = add(1, rank_sum_returns)
    # 11. 计算 ((-1 * sign(((close - ts_delay(close, 7)) + ts_delta(close, 7)))) * (1 + rank((1 + ts_sum(returns, 250)))))
    factor = multiply(neg_sign_close, add_rank_sum_returns)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()