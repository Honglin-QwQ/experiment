import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_max, rank, ts_decay_linear, ts_delta, ts_rank, multiply

def factor_0072(data, **kwargs):
    """
    数学表达式: (ts_max(rank(ts_decay_linear(ts_delta(vwap, 4.72775), 2.91864)), ts_rank(ts_decay_linear(((ts_delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608) / ((open * 0.147155) + (low * (1 - 0.147155)))) * -1), 3.33829), 16.7411)) * -1)
    中文描述: 该因子首先计算过去4.72775期成交量加权平均价(vwap)的变化，然后计算该变化值的过去2.91864期线性衰减值，并对衰减值进行排序，取过去一段时间内排序的最大值；同时，计算开盘价乘以0.147155加上最低价乘以(1-0.147155)的加权平均价，计算该加权平均价过去2.03608期的变化，再除以该加权平均价本身，乘以-1，计算结果的过去3.33829期线性衰减值，然后计算衰减值的过去16.7411期排名；最后，将两个排名相乘，取负值。该因子可能捕捉了价格和成交量的短期变化趋势，以及开盘价和最低价之间关系的变动，并通过衰减和排序来突出近期变化的重要性。
    因子应用场景：
    1. 短线择时策略，捕捉价格快速上涨或下跌的机会。
    2. 量价关系分析，用于识别成交量和价格变化的不同步情况，辅助判断趋势反转的可能性。
    3. 构建多因子模型，与其他基本面或技术指标结合使用，提高选股或择时的准确性。
    """
    # 1. 计算 ts_delta(vwap, 4.72775)
    data_ts_delta_vwap = ts_delta(data['vwap'], 4.72775)
    # 2. 计算 ts_decay_linear(ts_delta(vwap, 4.72775), 2.91864)
    data_ts_decay_linear_1 = ts_decay_linear(data_ts_delta_vwap, 2.91864)
    # 3. 计算 rank(ts_decay_linear(ts_delta(vwap, 4.72775), 2.91864))
    data_rank_1 = rank(data_ts_decay_linear_1)
    # 4. 计算 ts_max(rank(ts_decay_linear(ts_delta(vwap, 4.72775), 2.91864)))
    data_ts_max_1 = ts_max(data_rank_1)
    # 5. 计算 (open * 0.147155) + (low * (1 - 0.147155))
    data_weighted_avg = (data['open'] * 0.147155) + (data['low'] * (1 - 0.147155))
    # 6. 计算 ts_delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608)
    data_ts_delta_weighted_avg = ts_delta(data_weighted_avg, 2.03608)
    # 7. 计算 ts_delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608) / ((open * 0.147155) + (low * (1 - 0.147155)))
    data_divide_1 = data_ts_delta_weighted_avg / data_weighted_avg
    # 8. 计算 ((ts_delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608) / ((open * 0.147155) + (low * (1 - 0.147155)))) * -1)
    data_multiply_1 = data_divide_1 * -1
    # 9. 计算 ts_decay_linear((((ts_delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608) / ((open * 0.147155) + (low * (1 - 0.147155)))) * -1), 3.33829)
    data_ts_decay_linear_2 = ts_decay_linear(data_multiply_1, 3.33829)
    # 10. 计算 ts_rank(ts_decay_linear((((ts_delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608) / ((open * 0.147155) + (low * (1 - 0.147155)))) * -1), 3.33829), 16.7411)
    data_ts_rank_1 = ts_rank(data_ts_decay_linear_2, 16.7411)
    # 11. 计算 ts_max(rank(ts_decay_linear(ts_delta(vwap, 4.72775), 2.91864)), ts_rank(ts_decay_linear((((ts_delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608) / ((open * 0.147155) + (low * (1 - 0.147155)))) * -1), 3.33829), 16.7411))
    data_multiply_2 = multiply(data_ts_max_1, data_ts_rank_1)
    # 12. 计算 (ts_max(rank(ts_decay_linear(ts_delta(vwap, 4.72775), 2.91864)), ts_rank(ts_decay_linear((((ts_delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608) / ((open * 0.147155) + (low * (1 - 0.147155)))) * -1), 3.33829), 16.7411)) * -1)
    factor = data_multiply_2 * -1

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()