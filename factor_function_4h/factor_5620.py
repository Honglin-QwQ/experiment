import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_delta, ts_std_dev, rank, reverse, ts_returns, ts_rank, ts_corr

def factor_5620(data, **kwargs):
    """
    因子名称: factor_0007_71024
    数学表达式: ts_zscore(ts_delta(close, 5) / ts_std_dev(close, 20), 120) + rank(ts_delta(high, 2)) + ts_rank(reverse(ts_returns(close, 5)), 20) + ts_rank(ts_corr(low, ts_returns(close, 1), 30), 10)
    中文描述: 该因子是对历史因子factor_0006的改进，旨在提升预测能力和稳定性。它融合了波动率调整的动量因子、高价变化排名、反转因子以及价格与收益率相关性的时间序列排名。具体来说，ts_zscore(ts_delta(close, 5) / ts_std_dev(close, 20), 120)通过将收盘价的5日变化除以过去20日的标准差，实现了波动率调整，并计算其120日Z-score，从而更准确地衡量价格变动的异常程度。rank(ts_delta(high, 2))捕捉了每日最高价变动的相对位置。ts_rank(reverse(ts_returns(close, 5)), 20)引入了反转因子，通过对过去5日收益率取反并进行时间序列排名，捕捉短期超买超卖带来的反转机会。ts_rank(ts_corr(low, ts_returns(close, 1), 30), 10)捕捉了每日最低价和日收益率之间历史相关性的相对位置。通过这些改进，该因子旨在更全面地评估股票的潜在投资价值，并提高在不同市场条件下的适应性。
    因子应用场景：
    1. 波动率调整的动量分析：ts_zscore部分衡量了价格变动的异常程度，可用于识别具有显著动量且波动率调整后的股票。
    2. 短期反转机会捕捉：ts_rank(reverse(ts_returns(close, 5)), 20)部分可用于识别短期超买超卖带来的反转机会。
    3. 价格与收益率相关性分析：ts_rank(ts_corr(low, ts_returns(close, 1), 30), 10)部分可用于评估价格和收益率之间的关系，可能用于风险评估。
    """

    # 1. 计算 ts_delta(close, 5)
    ts_delta_close_5 = ts_delta(data['close'], 5)

    # 2. 计算 ts_std_dev(close, 20)
    ts_std_dev_close_20 = ts_std_dev(data['close'], 20)

    # 3. 计算 ts_delta(close, 5) / ts_std_dev(close, 20)
    temp = ts_delta_close_5 / ts_std_dev_close_20

    # 4. 计算 ts_zscore(ts_delta(close, 5) / ts_std_dev(close, 20), 120)
    ts_zscore_result = ts_zscore(temp, 120)

    # 5. 计算 ts_delta(high, 2)
    ts_delta_high_2 = ts_delta(data['high'], 2)

    # 6. 计算 rank(ts_delta(high, 2))
    rank_result = rank(ts_delta_high_2)

    # 7. 计算 ts_returns(close, 5)
    ts_returns_close_5 = ts_returns(data['close'], 5)

    # 8. 计算 reverse(ts_returns(close, 5))
    reverse_result = reverse(ts_returns_close_5)

    # 9. 计算 ts_rank(reverse(ts_returns(close, 5)), 20)
    ts_rank_result1 = ts_rank(reverse_result, 20)

    # 10. 计算 ts_returns(close, 1)
    ts_returns_close_1 = ts_returns(data['close'], 1)

    # 11. 计算 ts_corr(low, ts_returns(close, 1), 30)
    ts_corr_result = ts_corr(data['low'], ts_returns_close_1, 30)

    # 12. 计算 ts_rank(ts_corr(low, ts_returns(close, 1), 30), 10)
    ts_rank_result2 = ts_rank(ts_corr_result, 10)

    # 13. 计算 ts_zscore(ts_delta(close, 5) / ts_std_dev(close, 20), 120) + rank(ts_delta(high, 2)) + ts_rank(reverse(ts_returns(close, 5)), 20) + ts_rank(ts_corr(low, ts_returns(close, 1), 30), 10)
    factor = ts_zscore_result + rank_result + ts_rank_result1 + ts_rank_result2

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()