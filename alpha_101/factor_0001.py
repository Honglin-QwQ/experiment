import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log, ts_delta, rank, subtract, divide, ts_corr, multiply

def factor_0001(data, **kwargs):
    """
    数学表达式: (-1 * ts_corr(rank(ts_delta(log(volume), 2)), rank(((close - open) / open)), 6))
    中文描述: 该因子计算过去6天成交量取对数后差分值排名的变化与当天收益率（收盘价减开盘价除以开盘价）排名变化之间的相关系数的负值。可以理解为成交量变化与当天收益率之间关系的反向指标，负相关性越强，因子值越大，可能预示着反转机会；正相关性越强，因子值越小，可能预示着趋势延续。
    因子应用场景：
    1. 短线反转策略：寻找因子值较大的股票，预期短期内价格下跌；
    2. 趋势跟踪策略：避免选择因子值较低的股票，这些股票可能处于趋势延续状态；
    3. 量价关系分析：辅助判断量价背离或量价齐升等情况，验证市场有效性。
    """
    # 1. 计算 log(volume)
    log_volume = log(data['vol'])
    # 2. 计算 ts_delta(log(volume), 2)
    ts_delta_log_volume = ts_delta(log_volume, 2)
    # 3. 计算 rank(ts_delta(log(volume), 2))
    rank_ts_delta_log_volume = rank(ts_delta_log_volume, rate = 2)
    # 4. 计算 (close - open)
    close_minus_open = subtract(data['close'], data['open'])
    # 5. 计算 (close - open) / open
    return_rate = divide(close_minus_open, data['open'])
    # 6. 计算 rank(((close - open) / open))
    rank_return_rate = rank(return_rate, rate = 2)
    # 7. 计算 ts_corr(rank(ts_delta(log(volume), 2)), rank(((close - open) / open)), 6)
    ts_corr_result = ts_corr(rank_ts_delta_log_volume, rank_return_rate, 6)
    # 8. 计算 -1 * ts_corr(rank(ts_delta(log(volume), 2)), rank(((close - open) / open)), 6)
    factor = multiply(-1, ts_corr_result)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()