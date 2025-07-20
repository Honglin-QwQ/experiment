import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_min, ts_delay, rank, ts_sum, ts_rank, multiply, subtract,add

def factor_0051(data, **kwargs):
    """
    数学表达式: ((((-1 * ts_min(low, 5)) + ts_delay(ts_min(low, 5), 5)) * rank(((ts_sum(returns, 240) - ts_sum(returns, 20)) / 220))) * ts_rank(volume, 5))
    中文描述: 这个因子衡量了近期最低价变化趋势与成交量的协同效应，并通过与中期收益率对比来捕捉潜在的交易机会，具体来说，首先计算过去5天最低价的最小值，然后计算当前最小值与5天前最小值的差值，这个差值反映了近期价格下跌动能的变化，如果差值为负，说明近期下跌动能减弱，反之则增强，接着，计算过去240天收益率总和与过去20天收益率总和的差值，再除以220，得到一个中期收益率指标，并对其进行排序，这个排序反映了股票在中期内的相对收益表现，然后，计算过去5天成交量的排名，反映了近期成交量的活跃程度，最后，将价格下跌动能变化、中期收益率排名和成交量排名三个因素相乘，得到最终的因子值，这个因子试图找到那些近期价格下跌动能减弱，中期收益率表现较好，且成交量活跃的股票，这个因子可以应用于以下场景：1. 短期反转策略：寻找因子值较高的股票，预期这些股票可能出现短期反弹，2. 量价突破策略：结合成交量和价格变化，筛选出价格下跌动能减弱且成交量放大的股票，预期这些股票可能突破阻力位，3. 趋势跟踪策略：结合中期收益率，选择因子值较高且中期收益率表现良好的股票，预期这些股票可能延续上涨趋势。
    因子应用场景：
    1. 短期反转策略：寻找因子值较高的股票，预期这些股票可能出现短期反弹。
    2. 量价突破策略：结合成交量和价格变化，筛选出价格下跌动能减弱且成交量放大的股票，预期这些股票可能突破阻力位。
    3. 趋势跟踪策略：结合中期收益率，选择因子值较高且中期收益率表现良好的股票，预期这些股票可能延续上涨趋势。
    """

    # 1. 计算 ts_min(low, 5)
    ts_min_low_5 = ts_min(data['low'], d=5)

    # 2. 计算 -1 * ts_min(low, 5)
    neg_ts_min_low_5 = multiply(-1, ts_min_low_5)

    # 3. 计算 ts_delay(ts_min(low, 5), 5)
    ts_delay_ts_min_low_5 = ts_delay(ts_min_low_5, d=5)

    # 4. 计算 (-1 * ts_min(low, 5)) + ts_delay(ts_min(low, 5), 5)
    add_result = add(neg_ts_min_low_5, ts_delay_ts_min_low_5)

    # 5. 计算 ts_sum(returns, 240)
    ts_sum_returns_240 = ts_sum(data['returns'], d=240)

    # 6. 计算 ts_sum(returns, 20)
    ts_sum_returns_20 = ts_sum(data['returns'], d=20)

    # 7. 计算 (ts_sum(returns, 240) - ts_sum(returns, 20))
    subtract_result = subtract(ts_sum_returns_240, ts_sum_returns_20)

    # 8. 计算 (ts_sum(returns, 240) - ts_sum(returns, 20)) / 220
    divide_result = subtract_result / 220

    # 9. 计算 rank(((ts_sum(returns, 240) - ts_sum(returns, 20)) / 220))
    rank_result = rank(divide_result)

    # 10. 计算 ts_rank(volume, 5)
    ts_rank_volume_5 = ts_rank(data['vol'], d=5)

    # 11. 计算 (((-1 * ts_min(low, 5)) + ts_delay(ts_min(low, 5), 5)) * rank(((ts_sum(returns, 240) - ts_sum(returns, 20)) / 220)))
    multiply_result1 = multiply(add_result, rank_result)

    # 12. 计算 ((((-1 * ts_min(low, 5)) + ts_delay(ts_min(low, 5), 5)) * rank(((ts_sum(returns, 240) - ts_sum(returns, 20)) / 220))) * ts_rank(volume, 5))
    factor = multiply(multiply_result1, ts_rank_volume_5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()