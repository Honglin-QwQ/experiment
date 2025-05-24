import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_rank, ts_sum, sigmoid, ts_delta, multiply, subtract

def factor_5639(data, **kwargs):
    """
    数学表达式: ts_rank(ts_sum(tbase, 5), 5) * sigmoid(ts_delta(close, 5)) - ts_rank(ts_sum(tquote, 5), 5) * sigmoid(-1 * ts_delta(close, 5))
    中文描述: 本因子旨在改进原因子中if_else的硬切换问题，通过sigmoid函数平滑地将主动买入的基础币种和计价币种的交易量排名与价格趋势相结合。具体来说，它计算过去5天主动买入的基础币种数量总和的时间序列排名，并乘以一个sigmoid函数，该函数以过去5天收盘价的变化为输入，从而平滑地反映价格上涨的影响。同时，它计算过去5天主动买入的计价币种数量总和的时间序列排名，并乘以一个sigmoid函数，该函数以过去5天收盘价的负变化为输入，从而平滑地反映价格下跌的影响。该因子试图识别在价格上涨或下跌时，哪种币种的买入更为强势，从而预测价格的后续走势。sigmoid函数的使用使得因子对价格趋势的变化更加敏感，从而提高了因子的预测能力。
    因子应用场景：
    1. 趋势识别：识别在价格上涨或下跌时，哪种币种的买入更为强势，从而预测价格的后续走势。
    2. 市场情绪分析：通过分析基础币种和计价币种的交易量排名与价格趋势的关系，可以了解市场对不同币种的偏好和情绪。
    """
    # 1. 计算 ts_sum(tbase, 5)
    data_ts_sum_tbase = ts_sum(data['tbase'], 5)
    # 2. 计算 ts_rank(ts_sum(tbase, 5), 5)
    data_ts_rank_tbase = ts_rank(data_ts_sum_tbase, 5)
    # 3. 计算 ts_delta(close, 5)
    data_ts_delta_close = ts_delta(data['close'], 5)
    # 4. 计算 sigmoid(ts_delta(close, 5))
    data_sigmoid_delta_close = sigmoid(data_ts_delta_close)
    # 5. 计算 ts_rank(ts_sum(tbase, 5), 5) * sigmoid(ts_delta(close, 5))
    term1 = multiply(data_ts_rank_tbase, data_sigmoid_delta_close)
    # 6. 计算 ts_sum(tquote, 5)
    data_ts_sum_tquote = ts_sum(data['tquote'], 5)
    # 7. 计算 ts_rank(ts_sum(tquote, 5), 5)
    data_ts_rank_tquote = ts_rank(data_ts_sum_tquote, 5)
    # 8. 计算 -1 * ts_delta(close, 5)
    data_neg_delta_close = multiply(-1, data_ts_delta_close)
    # 9. 计算 sigmoid(-1 * ts_delta(close, 5))
    data_sigmoid_neg_delta_close = sigmoid(data_neg_delta_close)
    # 10. 计算 ts_rank(ts_sum(tquote, 5), 5) * sigmoid(-1 * ts_delta(close, 5))
    term2 = multiply(data_ts_rank_tquote, data_sigmoid_neg_delta_close)
    # 11. 计算 ts_rank(ts_sum(tbase, 5), 5) * sigmoid(ts_delta(close, 5)) - ts_rank(ts_sum(tquote, 5), 5) * sigmoid(-1 * ts_delta(close, 5))
    factor = subtract(term1, term2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()