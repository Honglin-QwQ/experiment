import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_delay, ts_sum, multiply

def factor_0044(data, **kwargs):
    """
    数学表达式: (-1 * ((rank((ts_sum(ts_delay(close, 5), 20) / 20)) * ts_corr(close, volume, 2)) * rank(ts_corr(ts_sum(close, 5), ts_sum(close, 20), 2))))
    中文描述: 该因子首先计算过去20天，每天收盘价前5天收盘价之和的均值，然后计算该均值的排序；接着计算收盘价和成交量的2日相关性；再计算过去5日收盘价之和与过去20日收盘价之和的2日相关性，并计算该相关性的排序；最后将第一个排序、收盘价和成交量的相关性、以及第二个排序三者相乘，并取反。该因子试图捕捉量价关系和短期、长期价格趋势相关性的综合影响，取反可能是为了反向操作。
    应用场景包括：
    1. 趋势反转策略：当因子值较高时，可能预示着超买，可以做空；当因子值较低时，可能预示着超卖，可以做多。
    2. 量价共振策略：结合成交量和价格变化，寻找量价关系异常的股票。
    3. 多因子模型：将该因子与其他基本面、技术面因子结合，构建更稳健的选股模型。
    """
    # 1. 计算 ts_delay(close, 5)
    data_ts_delay = ts_delay(data['close'], 5)
    # 2. 计算 ts_sum(ts_delay(close, 5), 20)
    data_ts_sum1 = ts_sum(data_ts_delay, 20)
    # 3. 计算 (ts_sum(ts_delay(close, 5), 20) / 20)
    data_divide = data_ts_sum1 / 20
    # 4. 计算 rank((ts_sum(ts_delay(close, 5), 20) / 20))
    data_rank1 = rank(data_divide, 2)
    # 5. 计算 ts_corr(close, volume, 2)
    data_ts_corr1 = ts_corr(data['close'], data['vol'], 2)
    # 6. 计算 ts_sum(close, 5)
    data_ts_sum2 = ts_sum(data['close'], 5)
    # 7. 计算 ts_sum(close, 20)
    data_ts_sum3 = ts_sum(data['close'], 20)
    # 8. 计算 ts_corr(ts_sum(close, 5), ts_sum(close, 20), 2)
    data_ts_corr2 = ts_corr(data_ts_sum2, data_ts_sum3, 2)
    # 9. 计算 rank(ts_corr(ts_sum(close, 5), ts_sum(close, 20), 2))
    data_rank2 = rank(data_ts_corr2, 2)
    # 10. 计算 (rank((ts_sum(ts_delay(close, 5), 20) / 20)) * ts_corr(close, volume, 2))
    data_multiply1 = multiply(data_rank1, data_ts_corr1)
    # 11. 计算 ((rank((ts_sum(ts_delay(close, 5), 20) / 20)) * ts_corr(close, volume, 2)) * rank(ts_corr(ts_sum(close, 5), ts_sum(close, 20), 2)))
    data_multiply2 = multiply(data_multiply1, data_rank2)
    # 12. 计算 -1 * ((rank((ts_sum(ts_delay(close, 5), 20) / 20)) * ts_corr(close, volume, 2)) * rank(ts_corr(ts_sum(close, 5), ts_sum(close, 20), 2)))
    factor = -1 * data_multiply2

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()