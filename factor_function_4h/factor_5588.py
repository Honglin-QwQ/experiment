import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_delta, log, divide, ts_arg_max

def factor_5588(data, **kwargs):
    """
    因子名称: factor_price_volume_interaction_82455
    数学表达式: ts_rank(ts_delta(log(divide(amount,vol)),3), 240) * ts_arg_max(high,41)
    中文描述: 该因子结合了成交额与成交量的比率变化以及最高价出现的时间位置。ts_rank(ts_delta(log(divide(amount,vol)),3), 240)衡量了过去3天成交额与成交量比率的对数变化在过去240天内的排名，反映了市场对价量关系的敏感度。ts_arg_max(high,41)则捕捉了过去41天内最高价出现的时间点，可能预示着市场突破或趋势反转。通过将这两个因子相乘，该因子旨在识别既有价量关系变化，又伴随价格高点出现的股票，从而提高捕捉交易机会的准确性。该因子在历史因子ts_rank(ts_delta(log(divide(amount,vol)),3), 240)的基础上，融入了ts_arg_max(high,41)因子，从时间维度上增强了对价格高点的关注，提升了因子对市场关键时刻的捕捉能力。
    因子应用场景：
    1. 识别价量关系变化：捕捉成交额与成交量比率变化的市场敏感度。
    2. 捕捉市场突破或趋势反转：通过最高价出现的时间点，预示市场变化。
    3. 提高交易机会的准确性：识别既有价量关系变化，又伴随价格高点出现的股票。
    """
    # 1. 计算 divide(amount,vol)
    data_divide = divide(data['amount'], data['vol'])
    # 2. 计算 log(divide(amount,vol))
    data_log = log(data_divide)
    # 3. 计算 ts_delta(log(divide(amount,vol)),3)
    data_ts_delta = ts_delta(data_log, 3)
    # 4. 计算 ts_rank(ts_delta(log(divide(amount,vol)),3), 240)
    data_ts_rank = ts_rank(data_ts_delta, 240)
    # 5. 计算 ts_arg_max(high,41)
    data_ts_arg_max = ts_arg_max(data['high'], 41)
    # 6. 计算 ts_rank(ts_delta(log(divide(amount,vol)),3), 240) * ts_arg_max(high,41)
    factor = data_ts_rank * data_ts_arg_max

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()