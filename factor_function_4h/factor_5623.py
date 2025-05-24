import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import if_else, ts_rank, ts_delta, ts_sum, ts_std_dev

def factor_5623(data, **kwargs):
    """
    数学表达式: if_else(ts_rank(ts_delta(close,1), 5) > 3, ts_sum(ts_delta(close, 1), 5) / ts_std_dev(close, 5), ts_sum(ts_delta(close, 1), 5) * ts_std_dev(close, 5))
    中文描述: 该因子旨在捕捉价格趋势和波动率之间的关系。首先，使用ts_rank计算过去5天收盘价每日变化的排名。如果排名高于3，则计算过去5天收盘价每日变化的加总，并除以收盘价的标准差；否则，计算过去5天收盘价每日变化的加总，并乘以收盘价的标准差。该因子的创新之处在于将排名信息作为条件，动态地调整价格变化和波动率之间的关系，从而更灵活地捕捉市场动态。
    因子应用场景：
    1. 趋势识别：当因子值较高时，可能意味着当前趋势较强且稳定。
    2. 波动率关系：因子有助于识别价格变化与波动率之间的关系，可能对市场整体趋势更为敏感。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta = ts_delta(data['close'], 1)
    # 2. 计算 ts_rank(ts_delta(close,1), 5)
    data_ts_rank = ts_rank(data_ts_delta, 5)
    # 3. 计算 ts_sum(ts_delta(close, 1), 5)
    data_ts_sum = ts_sum(data_ts_delta, 5)
    # 4. 计算 ts_std_dev(close, 5)
    data_ts_std_dev = ts_std_dev(data['close'], 5)
    # 5. 计算 if_else(ts_rank(ts_delta(close,1), 5) > 3, ts_sum(ts_delta(close, 1), 5) / ts_std_dev(close, 5), ts_sum(ts_delta(close, 1), 5) * ts_std_dev(close, 5))
    factor = if_else(data_ts_rank > 3, data_ts_sum / data_ts_std_dev, data_ts_sum * data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()