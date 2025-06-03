import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_delay, multiply

def factor_0019(data, **kwargs):
    """
    数学表达式: (((-1 * rank((open - ts_delay(high, 1)))) * rank((open - ts_delay(close, 1)))) * rank((open - ts_delay(low, 1))))
    中文描述: 该因子计算的是当日开盘价与前一天最高价、收盘价、最低价之差的排序值的乘积的负数。因子值越大，说明开盘价相对于前一日的高、收、低价都较低，反之则表明开盘价相对较高。这个因子可能反映了市场情绪的转变，或者隔夜消息对开盘的影响。
    因子应用场景包括：
    1. 短线反转策略：因子值较高时，可能预示着超卖，可以尝试买入；因子值较低时，可能预示着超买，可以尝试卖出。
    2. 趋势跟踪策略：结合其他趋势指标，如果因子值持续走高，可能意味着下跌趋势的开始，可以考虑做空。
    3. 波动率交易：该因子可以作为衡量市场波动的指标之一，结合波动率模型，预测市场波动。
    """
    # 1. 计算 (open - ts_delay(high, 1))
    data_open_high = data['open'] - ts_delay(data['high'], 1)
    # 2. 计算 rank((open - ts_delay(high, 1)))
    rank_open_high = rank(data_open_high)
    # 3. 计算 (open - ts_delay(close, 1))
    data_open_close = data['open'] - ts_delay(data['close'], 1)
    # 4. 计算 rank((open - ts_delay(close, 1)))
    rank_open_close = rank(data_open_close)
    # 5. 计算 (open - ts_delay(low, 1))
    data_open_low = data['open'] - ts_delay(data['low'], 1)
    # 6. 计算 rank((open - ts_delay(low, 1)))
    rank_open_low = rank(data_open_low)
    # 7. 计算 (rank((open - ts_delay(high, 1)))) * rank((open - ts_delay(close, 1))))
    temp_product = multiply(rank_open_high, rank_open_close)
    # 8. 计算 ((rank((open - ts_delay(high, 1)))) * rank((open - ts_delay(close, 1)))) * rank((open - ts_delay(low, 1))))
    product = multiply(temp_product, rank_open_low)
    # 9. 计算 -1 * (((rank((open - ts_delay(high, 1)))) * rank((open - ts_delay(close, 1)))) * rank((open - ts_delay(low, 1)))))
    factor = -1 * product

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()