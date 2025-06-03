import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_scale, ts_arg_max, subtract, divide, multiply

def factor_0059(data, **kwargs):
    """
    数学表达式: (0 - (1 * ((2 * ts_scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) - ts_scale(rank(ts_arg_max(close, 10))))))
    中文描述: 该因子首先计算每日的（收盘价-最低价）与（最高价-收盘价）之差，再除以（最高价-最低价），乘以成交量，然后对结果进行排序并进行时间序列上的标准化。接着计算过去10天收盘价最大值出现的位置索引，也进行排序和时间序列标准化。最后用0减去前一部分乘以1的结果，再减去后一部分的结果。这个因子试图捕捉量价关系和价格动量，标准化排序是为了消除量纲影响，求最大值位置是为了寻找短期价格反转信号。
    因子应用场景：
    1. 短期反转策略：当因子值较低时，可能预示着超卖，可以考虑买入；当因子值较高时，可能预示着超买，可以考虑卖出。
    2. 量价共振分析：结合成交量和价格波动，筛选出量价关系异常的股票。
    3. 趋势跟踪策略的辅助指标：与其他趋势指标结合使用，提高趋势判断的准确性。
    """

    # 1. 计算 (close - low)
    close_minus_low = subtract(data['close'], data['low'])

    # 2. 计算 (high - close)
    high_minus_close = subtract(data['high'], data['close'])

    # 3. 计算 ((close - low) - (high - close))
    numerator = subtract(close_minus_low, high_minus_close)

    # 4. 计算 (high - low)
    denominator = subtract(data['high'], data['low'])

    # 5. 计算 (((close - low) - (high - close)) / (high - low))
    temp1 = divide(numerator, denominator)

    # 6. 计算 ((((close - low) - (high - close)) / (high - low)) * volume)
    temp2 = multiply(temp1, data['vol'])

    # 7. 计算 rank(((((close - low) - (high - close)) / (high - low)) * volume))
    ranked = rank(temp2)

    # 8. 计算 ts_scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))
    ts_scaled_rank = ts_scale(ranked)

    # 9. 计算 ts_arg_max(close, 10)
    ts_arg_max_close = ts_arg_max(data['close'], d=10)

    # 10. 计算 rank(ts_arg_max(close, 10))
    ranked_ts_arg_max = rank(ts_arg_max_close)

    # 11. 计算 ts_scale(rank(ts_arg_max(close, 10)))
    ts_scaled_rank_ts_arg_max = ts_scale(ranked_ts_arg_max)

    # 12. 计算 (2 * ts_scale(rank(((((close - low) - (high - close)) / (high - low)) * volume))))
    temp3 = multiply(2, ts_scaled_rank)

    # 13. 计算 (2 * ts_scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) - ts_scale(rank(ts_arg_max(close, 10)))
    temp4 = subtract(temp3, ts_scaled_rank_ts_arg_max)

    # 14. 计算 (1 * ((2 * ts_scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) - ts_scale(rank(ts_arg_max(close, 10)))))
    temp5 = multiply(1, temp4)

    # 15. 计算 (0 - (1 * ((2 * ts_scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) - ts_scale(rank(ts_arg_max(close, 10))))))
    factor = subtract(0, temp5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()