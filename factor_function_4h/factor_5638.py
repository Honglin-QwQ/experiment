import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delta, log, divide, ts_delay, ts_min

def factor_5638(data, **kwargs):
    """
    数学表达式: ts_std_dev(ts_delta(close,3), 20) * log(divide(high, ts_delay(ts_min(low,5),5)))
    中文描述: 该因子结合了短期收盘价波动率和日内价格波动幅度，并引入了滞后最低价的概念。首先计算过去3天收盘价的变化，然后计算这些变化的20天标准差，以此衡量短期价格波动率。同时，计算每日最高价和5天前5日最低价的比率的自然对数，以此衡量日内价格波动幅度与过去一段时间最低价格之间的关系。相较于历史版本，该因子使用ts_delay(ts_min(low,5),5)替代了ts_delay(low,5)，即使用过去5日的最低价的5日滞后替代了5日滞后最低价，从而避免了因子与已生成因子相关性过高的问题，并且考虑了更长周期的最低价的影响。
    因子应用场景：
    1. 波动率分析：该因子可用于衡量股票的短期价格波动率，并结合日内价格波动幅度来识别潜在的交易机会。
    2. 风险管理：通过结合短期波动率和滞后最低价，该因子有助于评估股票的风险水平。
    """
    # 1. 计算 ts_delta(close,3)
    data_ts_delta = ts_delta(data['close'], 3)
    # 2. 计算 ts_std_dev(ts_delta(close,3), 20)
    data_ts_std_dev = ts_std_dev(data_ts_delta, 20)
    # 3. 计算 ts_min(low,5)
    data_ts_min = ts_min(data['low'], 5)
    # 4. 计算 ts_delay(ts_min(low,5),5)
    data_ts_delay = ts_delay(data_ts_min, 5)
    # 5. 计算 divide(high, ts_delay(ts_min(low,5),5))
    data_divide = divide(data['high'], data_ts_delay)
    # 6. 计算 log(divide(high, ts_delay(ts_min(low,5),5)))
    data_log = log(data_divide)
    # 7. 计算 ts_std_dev(ts_delta(close,3), 20) * log(divide(high, ts_delay(ts_min(low,5),5)))
    factor = data_ts_std_dev * data_log

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()