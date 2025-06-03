import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_delta, ts_decay_linear, divide, adv, ts_sum, multiply, subtract,add

def factor_0038(data, **kwargs):
    """
    数学表达式: ((-1 * rank((ts_delta(close, 7) * (1 - rank(ts_decay_linear((volume / adv20), 9)))))) * (1 + rank(ts_sum(returns, 250)))) 
    中文描述: 该因子首先计算过去7天收盘价的变化，然后乘以一个调整项，该调整项由成交量除以过去20天平均成交量的比率进行线性衰减后的排名决定，最后将上述结果的排名取负。这个负排名结果再乘以一个由过去250天收益率之和的排名加1得到的数值。该因子试图捕捉短期价格动量与成交量变化的关系，并结合长期收益表现进行调整。
    因子应用场景包括：
    1. 短期反转策略：寻找价格短期下跌但成交量相对较高的股票，预期价格可能反弹。
    2. 趋势跟踪策略：结合长期收益率，筛选出既有长期上涨趋势，近期又出现调整的股票。
    3. 量价共振策略：利用成交量变化验证价格变动的有效性，例如，价格下跌但成交量放大可能预示着更强的下跌趋势。
    """
    # 1. 计算 ts_delta(close, 7)
    data_ts_delta_close = ts_delta(data['close'], 7)
    # 2. 计算 adv20
    data_adv20 = adv(data['vol'], d = 20)
    # 3. 计算 volume / adv20
    data_volume_over_adv20 = divide(data['vol'], data_adv20)
    # 4. 计算 ts_decay_linear((volume / adv20), 9)
    data_ts_decay_linear = ts_decay_linear(data_volume_over_adv20, 9)
    # 5. 计算 rank(ts_decay_linear((volume / adv20), 9))
    data_rank_ts_decay_linear = rank(data_ts_decay_linear)
    # 6. 计算 1 - rank(ts_decay_linear((volume / adv20), 9))
    data_subtract = subtract(1, data_rank_ts_decay_linear)
    # 7. 计算 ts_delta(close, 7) * (1 - rank(ts_decay_linear((volume / adv20), 9)))
    data_multiply = multiply(data_ts_delta_close, data_subtract)
    # 8. 计算 rank(ts_delta(close, 7) * (1 - rank(ts_decay_linear((volume / adv20), 9))))
    data_rank = rank(data_multiply)
    # 9. 计算 -1 * rank(ts_delta(close, 7) * (1 - rank(ts_decay_linear((volume / adv20), 9))))
    data_multiply_negative_one = multiply(-1, data_rank)
    # 10. 计算 ts_sum(returns, 250)
    data_ts_sum_returns = ts_sum(data['returns'], 250)
    # 11. 计算 rank(ts_sum(returns, 250))
    data_rank_ts_sum_returns = rank(data_ts_sum_returns)
    # 12. 计算 1 + rank(ts_sum(returns, 250))
    data_add_one = add(1, data_rank_ts_sum_returns)
    # 13. 计算 (-1 * rank((ts_delta(close, 7) * (1 - rank(ts_decay_linear((volume / adv20), 9)))))) * (1 + rank(ts_sum(returns, 250)))
    factor = multiply(data_multiply_negative_one, data_add_one)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()