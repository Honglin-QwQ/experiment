import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_delta, log, divide

def factor_5644(data, **kwargs):
    """
    因子名称: factor_0001_99530
    数学表达式: ts_rank(ts_delta(vwap, 1), 10) * log(divide(amount, vol))
    中文描述: 该因子结合了VWAP变化率的排名和交易额与交易量的比率的对数。首先，计算VWAP的日变化率，然后计算该变化率在过去10天内的排名。同时，计算交易额与交易量的比率，并取其自然对数。最后，将这两个结果相乘。该因子旨在捕捉价格动量变化和交易活跃度的关系，当价格动量变化迅速且交易额相对于交易量较高时，因子值较高，可能预示着潜在的交易机会。
    因子应用场景：
    1. 动量捕捉：捕捉价格动量变化。
    2. 交易活跃度分析：分析交易额与交易量的比率。
    3. 潜在交易机会识别：识别价格动量变化迅速且交易额相对于交易量较高时的交易机会。
    """
    # 1. 计算 ts_delta(vwap, 1)
    data_ts_delta_vwap = ts_delta(data['vwap'], 1)
    # 2. 计算 ts_rank(ts_delta(vwap, 1), 10)
    data_ts_rank = ts_rank(data_ts_delta_vwap, 10)
    # 3. 计算 divide(amount, vol)
    data_divide = divide(data['amount'], data['vol'])
    # 4. 计算 log(divide(amount, vol))
    data_log = log(data_divide)
    # 5. 计算 ts_rank(ts_delta(vwap, 1), 10) * log(divide(amount, vol))
    factor = data_ts_rank * data_log

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()