import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_delay, ts_rank, abs, ts_sum, subtract, multiply, divide,add,adv

def factor_0035(data, **kwargs):
    """
    数学表达式: (((((2.21 * rank(ts_corr((close - open), ts_delay(volume, 1), 15))) + (0.7 * rank((open - close)))) + (0.73 * rank(ts_rank(ts_delay((-1 * returns), 6), 5)))) + rank(abs(ts_corr(vwap, adv20, 6)))) + (0.6 * rank((((ts_sum(close, 200) / 200) - open) * (close - open)))))
    中文描述: 该因子综合考虑了价格动量、成交量和波动率等因素。首先计算收盘价与开盘价差值与滞后一天成交量的相关性，并进行排序；然后计算开盘价与收盘价差值的排序；以及过去6天收益率延迟6期的排名再进行排名；接着计算成交额加权平均价与过去20日平均成交额的相关性的绝对值并排序；最后计算过去200天收盘价均值与开盘价的差乘以收盘价与开盘价的差，再进行排序。将上述各项加权求和后进行排序，得到最终因子值。该因子可能捕捉了量价关系、趋势反转和波动率变化等信息。
    因子应用场景包括：
    1. 趋势跟踪策略：因子值较高可能表示股票处于上升趋势，可用于筛选潜在的上涨股票。
    2. 反转策略：因子值较低可能暗示股票价格超跌，可用于寻找潜在的反弹机会。
    3. 量化选股：将该因子与其他基本面或技术面因子结合，构建多因子选股模型，提高选股效果。
    """
    # 1. 计算 (close - open)
    close_minus_open = subtract(data['close'], data['open'])
    # 2. 计算 ts_delay(volume, 1)
    ts_delay_volume = ts_delay(data['vol'], 1)
    # 3. 计算 ts_corr((close - open), ts_delay(volume, 1), 15)
    ts_corr_1 = ts_corr(close_minus_open, ts_delay_volume, 15)
    # 4. 计算 rank(ts_corr((close - open), ts_delay(volume, 1), 15))
    rank_1 = rank(ts_corr_1, 2)
    # 5. 计算 2.21 * rank(ts_corr((close - open), ts_delay(volume, 1), 15))
    multiply_1 = multiply(2.21, rank_1)
    # 6. 计算 (open - close)
    open_minus_close = subtract(data['open'], data['close'])
    # 7. 计算 rank((open - close))
    rank_2 = rank(open_minus_close, 2)
    # 8. 计算 0.7 * rank((open - close))
    multiply_2 = multiply(0.7, rank_2)
    # 9. 计算 add((2.21 * rank(ts_corr((close - open), ts_delay(volume, 1), 15))), (0.7 * rank((open - close))))
    add_1 = add(multiply_1, multiply_2)
    # 10. 计算 (-1 * returns)
    multiply_3 = multiply(-1, data['returns'])
    # 11. 计算 ts_delay((-1 * returns), 6)
    ts_delay_returns = ts_delay(multiply_3, 6)
    # 12. 计算 ts_rank(ts_delay((-1 * returns), 6), 5)
    ts_rank_1 = ts_rank(ts_delay_returns, 5)
    # 13. 计算 rank(ts_rank(ts_delay((-1 * returns), 6), 5))
    rank_3 = rank(ts_rank_1, 2)
    # 14. 计算 0.73 * rank(ts_rank(ts_delay((-1 * returns), 6), 5))
    multiply_4 = multiply(0.73, rank_3)
    # 15. 计算 add(add((2.21 * rank(ts_corr((close - open), ts_delay(volume, 1), 15))), (0.7 * rank((open - close)))), (0.73 * rank(ts_rank(ts_delay((-1 * returns), 6), 5))))
    add_2 = add(add_1, multiply_4)
    # 16. 计算 adv20
    adv20 = adv(data['amount'], d = 20)
    # 17. 计算 ts_corr(vwap, adv20, 6)
    ts_corr_2 = ts_corr(data['vwap'], adv20, 6)
    # 18. 计算 abs(ts_corr(vwap, adv20, 6))
    abs_corr = abs(ts_corr_2)
    # 19. 计算 rank(abs(ts_corr(vwap, adv20, 6)))
    rank_4 = rank(abs_corr, 2)
    # 20. 计算 add(add(add((2.21 * rank(ts_corr((close - open), ts_delay(volume, 1), 15))), (0.7 * rank((open - close)))), (0.73 * rank(ts_rank(ts_delay((-1 * returns), 6), 5)))), rank(abs(ts_corr(vwap, adv20, 6))))
    add_3 = add(add_2, rank_4)
    # 21. 计算 ts_sum(close, 200)
    ts_sum_close = ts_sum(data['close'], 200)
    # 22. 计算 (ts_sum(close, 200) / 200)
    divide_1 = divide(ts_sum_close, 200)
    # 23. 计算 ((ts_sum(close, 200) / 200) - open)
    subtract_1 = subtract(divide_1, data['open'])
    # 24. 计算 (close - open)
    close_minus_open_2 = subtract(data['close'], data['open'])
    # 25. 计算 (((ts_sum(close, 200) / 200) - open) * (close - open))
    multiply_5 = multiply(subtract_1, close_minus_open_2)
    # 26. 计算 rank((((ts_sum(close, 200) / 200) - open) * (close - open)))
    rank_5 = rank(multiply_5, 2)
    # 27. 计算 0.6 * rank((((ts_sum(close, 200) / 200) - open) * (close - open)))
    multiply_6 = multiply(0.6, rank_5)
    # 28. 计算 add(add(add(add((2.21 * rank(ts_corr((close - open), ts_delay(volume, 1), 15))), (0.7 * rank((open - close)))), (0.73 * rank(ts_rank(ts_delay((-1 * returns), 6), 5)))), rank(abs(ts_corr(vwap, adv20, 6)))), (0.6 * rank((((ts_sum(close, 200) / 200) - open) * (close - open)))))
    factor = add(add_3, multiply_6)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()