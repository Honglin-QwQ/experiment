import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_delta, ts_rank, ts_corr, ts_sum

def factor_5627(data, **kwargs):
    """
    因子名称: factor_0001_24121
    数学表达式: rank(ts_delta(amount, 1)) * ts_rank(returns, 20) - ts_corr(ts_sum(vol, 5), close, 10)
    中文描述: 本因子结合了交易额变化、收益率排名和量价相关性。首先，计算交易额的日变化并进行排名，反映资金流动的活跃程度。其次，计算收益率在过去20天的排名，衡量收益率的相对表现。然后，计算过去5天成交量总和与收盘价的10天相关性，反映量价关系。最后，用交易额变化排名乘以收益率排名，再减去量价相关性，综合评估市场情绪和趋势。
    因子应用场景：
    1. 市场情绪分析：因子值较高可能表示市场情绪乐观，资金活跃，收益率表现较好。
    2. 趋势跟踪：因子可以帮助识别市场趋势，尤其是在交易额变化和收益率排名都较高的情况下。
    3. 量价关系验证：通过量价相关性的扣除，可以更准确地评估市场情绪，避免虚假信号。
    """
    # 1. 计算 ts_delta(amount, 1)
    data_ts_delta_amount = ts_delta(data['amount'], 1)
    # 2. 计算 rank(ts_delta(amount, 1))
    data_rank_ts_delta_amount = rank(data_ts_delta_amount)
    # 3. 计算 ts_rank(returns, 20)
    data_ts_rank_returns = ts_rank(data['returns'], 20)
    # 4. 计算 ts_sum(vol, 5)
    data_ts_sum_vol = ts_sum(data['vol'], 5)
    # 5. 计算 ts_corr(ts_sum(vol, 5), close, 10)
    data_ts_corr_ts_sum_vol_close = ts_corr(data_ts_sum_vol, data['close'], 10)
    # 6. 计算 rank(ts_delta(amount, 1)) * ts_rank(returns, 20)
    factor_part1 = data_rank_ts_delta_amount * data_ts_rank_returns
    # 7. 计算 rank(ts_delta(amount, 1)) * ts_rank(returns, 20) - ts_corr(ts_sum(vol, 5), close, 10)
    factor = factor_part1 - data_ts_corr_ts_sum_vol_close

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()