import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, divide, subtract, add

def factor_0041(data, **kwargs):
    """
    数学表达式: (rank((vwap - close)) / rank((vwap + close))) 
    中文描述: 因子计算了（成交量加权平均价 - 收盘价）的排序百分比，除以（成交量加权平均价 + 收盘价）的排序百分比，反映了成交量加权平均价和收盘价相对强弱关系。
    因子应用场景：
    1. 短线择时，该因子可以捕捉日内价格波动的异常情况，用于判断超买超卖现象。
    2. 趋势跟踪，结合其他趋势指标，辅助判断价格趋势的强度和持续性。
    3. 风险管理，可以作为衡量市场情绪和价格偏离程度的指标，用于调整仓位或设置止损。
    """
    # 1. 计算 (vwap - close)
    data_vwap_minus_close = subtract(data['vwap'], data['close'])
    # 2. 计算 rank((vwap - close))
    rank_vwap_minus_close = rank(data_vwap_minus_close, rate = 2)
    # 3. 计算 (vwap + close)
    data_vwap_plus_close = add(data['vwap'], data['close'])
    # 4. 计算 rank((vwap + close))
    rank_vwap_plus_close = rank(data_vwap_plus_close, rate = 2)
    # 5. 计算 (rank((vwap - close)) / rank((vwap + close)))
    factor = divide(rank_vwap_minus_close, rank_vwap_plus_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()