import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_delta, adv, ts_median, ts_returns, inverse

def factor_5587(data, **kwargs):
    """
    数学表达式: ts_rank(ts_delta(adv(10), 1), 120) + inverse(ts_median(ts_returns(close, d = 1), 5))
    中文描述: 该因子结合了交易量变化的时间序列排名和基于倒数与中位数收益率的因子。前半部分ts_rank(ts_delta(adv(10), 1), 120)衡量过去1天平均交易量变化在过去120天的排名，反映市场情绪和参与度。后半部分inverse(ts_median(ts_returns(close, d = 1), 5))计算过去5天日收益率中位数的倒数，评估股票的短期风险, 相比于历史因子，本因子使用中位数替代了kth_element，避免了极端值的影响，同时缩短了adv的窗口期，提升了因子的灵敏度。
    因子应用场景：
    1. 市场情绪分析：通过交易量变化排名，捕捉市场参与者的情绪波动。
    2. 短期风险评估：利用收益率中位数的倒数，评估股票的短期风险水平。
    3. 趋势跟踪：结合市场情绪和风险指标，辅助判断股票价格的潜在趋势。
    """
    # 1. 计算 adv(10)
    data_adv = adv(data['vol'], d = 10)
    # 2. 计算 ts_delta(adv(10), 1)
    data_ts_delta = ts_delta(data_adv, d = 1)
    # 3. 计算 ts_rank(ts_delta(adv(10), 1), 120)
    data_ts_rank = ts_rank(data_ts_delta, d = 120)
    # 4. 计算 ts_returns(close, d = 1)
    data_ts_returns = ts_returns(data['close'], d = 1)
    # 5. 计算 ts_median(ts_returns(close, d = 1), 5)
    data_ts_median = ts_median(data_ts_returns, d = 5)
    # 6. 计算 inverse(ts_median(ts_returns(close, d = 1), 5))
    data_inverse = inverse(data_ts_median)
    # 7. 计算 ts_rank(ts_delta(adv(10), 1), 120) + inverse(ts_median(ts_returns(close, d = 1), 5))
    factor = data_ts_rank + data_inverse

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()