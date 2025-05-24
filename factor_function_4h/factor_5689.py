import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, divide, ts_sum, signed_power, ts_delta, ts_rank, ts_corr

def factor_5689(data, **kwargs):
    """
    数学表达式: ts_zscore(divide(ts_sum(tbase, 5), ts_sum(tquote, 5)), 10) + signed_power(ts_delta(close, 2), 2) + ts_rank(ts_corr(close, vol, 5), 10)
    中文描述: 该因子在factor_0002的基础上进行了改进，增加了成交量与收盘价相关性的考量，以捕捉市场参与度和价格趋势之间的潜在关系。首先，沿用factor_0002的计算方式，即计算过去5天主动买入的基础币种数量之和与过去5天主动买入的计价币种数量之和的比值，并计算这个比值在过去10天内的Z得分，衡量短期内买盘力量的相对强弱。然后，计算收盘价在过去2天的差值的平方，以捕捉价格的动量信息。此外，计算过去5天收盘价与成交量的相关性，并计算这个相关性在过去10天的排名，以评估价格和成交量之间的协同效应。最后，将这三个部分相加。创新点在于结合了主动买入的币种数量信息、价格动量信息和成交量与价格相关性信息，可能更有效地识别潜在的交易机会。
    因子应用场景：
    1. 市场情绪分析：通过主动买入的币种数量比值，衡量市场买盘力量的强弱。
    2. 价格动量捕捉：收盘价差值的平方可以反映价格的动量变化。
    3. 成交量与价格协同效应评估：成交量与价格的相关性排名可以评估价格和成交量之间的协同效应。
    """
    # 1. 计算 ts_sum(tbase, 5)
    data_ts_sum_tbase = ts_sum(data['tbase'], 5)
    # 2. 计算 ts_sum(tquote, 5)
    data_ts_sum_tquote = ts_sum(data['tquote'], 5)
    # 3. 计算 divide(ts_sum(tbase, 5), ts_sum(tquote, 5))
    data_divide = divide(data_ts_sum_tbase, data_ts_sum_tquote)
    # 4. 计算 ts_zscore(divide(ts_sum(tbase, 5), ts_sum(tquote, 5)), 10)
    data_ts_zscore = ts_zscore(data_divide, 10)
    # 5. 计算 ts_delta(close, 2)
    data_ts_delta = ts_delta(data['close'], 2)
    # 6. 计算 signed_power(ts_delta(close, 2), 2)
    data_signed_power = signed_power(data_ts_delta, 2)
    # 7. 计算 ts_corr(close, vol, 5)
    data_ts_corr = ts_corr(data['close'], data['vol'], 5)
    # 8. 计算 ts_rank(ts_corr(close, vol, 5), 10)
    data_ts_rank = ts_rank(data_ts_corr, 10)
    # 9. 计算 ts_zscore(divide(ts_sum(tbase, 5), ts_sum(tquote, 5)), 10) + signed_power(ts_delta(close, 2), 2) + ts_rank(ts_corr(close, vol, 5), 10)
    factor = data_ts_zscore + data_signed_power + data_ts_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()