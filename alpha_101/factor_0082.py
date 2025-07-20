import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_delay, ts_sum, divide, subtract, multiply

def factor_0082(data, **kwargs):
    """
    数学表达式: ((rank(ts_delay(((high - low) / (ts_sum(close, 5) / 5)), 2)) * rank(rank(volume))) / (((high - low) / (ts_sum(close, 5) / 5)) / (vwap - close)))
    中文描述: 该因子首先计算每日最高价和最低价之差与过去5日收盘价平均值的比率，衡量价格波动幅度；然后计算这个比率在过去2日的滞后值，并进行排序；同时计算成交量的排序值，并再次进行排序；将上述两个排序值相乘，再除以价格波动幅度与(成交额均价-收盘价)的比率。该因子试图结合价格波动和成交量信息，寻找价格波动相对较小但成交量相对活跃的股票，可能用于识别短期内具有上涨潜力的股票，或者用于构建量价组合策略，例如，可以选取因子值较高的股票构建多头组合，或者用于高频交易中捕捉价格异动。
    因子应用场景：
    1. 短期上涨潜力：因子值较高可能表示股票价格波动相对较小，但成交量相对活跃，可能预示着短期内具有上涨潜力。
    2. 量价组合策略：可以选取因子值较高的股票构建多头组合，以期获得超额收益。
    3. 高频交易：用于捕捉价格异动，辅助高频交易决策。
    """
    # 1. 计算 (high - low)
    high_minus_low = subtract(data['high'], data['low'])
    # 2. 计算 ts_sum(close, 5)
    ts_sum_close_5 = ts_sum(data['close'], 5)
    # 3. 计算 ts_sum(close, 5) / 5
    ts_sum_close_5_divided_5 = divide(ts_sum_close_5, 5)
    # 4. 计算 (high - low) / (ts_sum(close, 5) / 5)
    price_volatility = divide(high_minus_low, ts_sum_close_5_divided_5)
    # 5. 计算 ts_delay(((high - low) / (ts_sum(close, 5) / 5)), 2)
    price_volatility_delayed = ts_delay(price_volatility, 2)
    # 6. 计算 rank(ts_delay(((high - low) / (ts_sum(close, 5) / 5)), 2))
    rank_price_volatility_delayed = rank(price_volatility_delayed)
    # 7. 计算 rank(volume)
    rank_volume = rank(data['vol'])
    # 8. 计算 rank(rank(volume))
    rank_rank_volume = rank(rank_volume)
    # 9. 计算 rank(ts_delay(((high - low) / (ts_sum(close, 5) / 5)), 2)) * rank(rank(volume))
    numerator = multiply(rank_price_volatility_delayed, rank_rank_volume)
    # 10. 计算 vwap - close
    vwap_minus_close = subtract(data['vwap'], data['close'])
    # 11. 计算 ((high - low) / (ts_sum(close, 5) / 5)) / (vwap - close)
    denominator = divide(price_volatility, vwap_minus_close)
    # 12. 计算 ((rank(ts_delay(((high - low) / (ts_sum(close, 5) / 5)), 2)) * rank(rank(volume))) / (((high - low) / (ts_sum(close, 5) / 5)) / (vwap - close)))
    factor = divide(numerator, denominator)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()