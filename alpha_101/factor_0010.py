import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_max, ts_min, ts_delta, multiply, add, subtract

def factor_0010(data, **kwargs):
    """
    数学表达式: ((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(ts_delta(volume, 3))) 
    中文描述: 该因子首先计算过去3天内每天的(成交量加权平均价 - 收盘价)的最大值和最小值，然后分别对这两个时间序列进行排序，并求和，接着计算过去3天成交量的变化量，并对其进行排序，最后将前两部分的结果相乘。该因子试图捕捉量价关系在短期内的变化趋势，结合成交量的变化，可能反映了市场对价格短期偏离程度的反应。
    应用场景：
    1. 短线择时：当因子值较高时，可能预示着短期内价格将向成交量加权平均价回归，可考虑反向操作。
    2. 异动捕捉：该因子可以用来识别量价关系出现异常波动的股票，进一步分析其基本面或消息面。
    3. 构建组合：将该因子与其他量价因子结合，构建多因子选股模型。
    """
    # 1. 计算 (vwap - close)
    vwap_minus_close = subtract(data['vwap'], data['close'])
    
    # 2. 计算 ts_max((vwap - close), 3)
    ts_max_vwap_close = ts_max(vwap_minus_close, d=3)
    
    # 3. 计算 rank(ts_max((vwap - close), 3))
    rank_ts_max_vwap_close = rank(ts_max_vwap_close)
    
    # 4. 计算 ts_min((vwap - close), 3)
    ts_min_vwap_close = ts_min(vwap_minus_close, d=3)
    
    # 5. 计算 rank(ts_min((vwap - close), 3))
    rank_ts_min_vwap_close = rank(ts_min_vwap_close)
    
    # 6. 计算 rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))
    sum_rank_ts_max_min = add(rank_ts_max_vwap_close, rank_ts_min_vwap_close)
    
    # 7. 计算 ts_delta(volume, 3)
    ts_delta_volume = ts_delta(data['vol'], d=3)
    
    # 8. 计算 rank(ts_delta(volume, 3))
    rank_ts_delta_volume = rank(ts_delta_volume)
    
    # 9. 计算 (rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(ts_delta(volume, 3))
    factor = multiply(sum_rank_ts_max_min, rank_ts_delta_volume)
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()