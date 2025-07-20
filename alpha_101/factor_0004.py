import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_sum, divide, subtract, abs, multiply

def factor_0004(data, **kwargs):
    """
    数学表达式: (rank((open - (ts_sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap))))) 
    中文描述: 该因子首先计算每日开盘价与过去10日成交量加权平均价均值的差值，然后对该差值进行排序，得到一个排序值。接着，计算每日收盘价与成交量加权平均价的差值，取绝对值后再进行排序，并乘以-1。最后，将这两个排序值相乘。这个因子的含义是，如果开盘价低于过去一段时间的平均价格，且收盘价接近成交量加权平均价，则因子值较高，反之则较低。该因子可能捕捉了开盘价的异动和收盘价回归平均价格的趋势。
    因子应用场景：
    1. 可以用于短线择时，当因子值较高时，可能预示着股价将上涨；当因子值较低时，可能预示着股价将下跌。
    2. 可以用于构建量化交易策略，结合其他因子进行多因子选股，筛选出具有上涨潜力的股票。
    3. 可以用于风险管理，通过监控因子值的变化，及时调整仓位，降低投资风险。
    """
    # 1. 计算 ts_sum(vwap, 10)
    data_ts_sum_vwap = ts_sum(data['vwap'], 10)
    # 2. 计算 (ts_sum(vwap, 10) / 10)
    data_divide = divide(data_ts_sum_vwap, 10)
    # 3. 计算 (open - (ts_sum(vwap, 10) / 10))
    data_subtract = subtract(data['open'], data_divide)
    # 4. 计算 rank((open - (ts_sum(vwap, 10) / 10)))
    data_rank1 = rank(data_subtract, 2)
    # 5. 计算 (close - vwap)
    data_subtract2 = subtract(data['close'], data['vwap'])
    # 6. 计算 abs(rank((close - vwap)))
    data_abs_rank = abs(rank(data_subtract2, 2))
    # 7. 计算 (-1 * abs(rank((close - vwap)))))
    data_multiply = multiply(-1, data_abs_rank)
    # 8. 计算 (rank((open - (ts_sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))
    factor = multiply(data_rank1, data_multiply)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()