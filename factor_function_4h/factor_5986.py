import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_delay, rank, subtract

def factor_5986(data, **kwargs):
    """
    因子名称: VWAP_Skew_Volume_Lag_Rank_Diff_72460
    数学表达式: subtract(rank(ts_skewness(vwap, 22)), rank(ts_delay(vol, 40)))
    中文描述: 该因子结合了参考因子中的VWAP偏斜度、成交量滞后和排名操作符。它首先计算过去22天VWAP的偏斜度，然后对这个偏斜度进行排名。同时，计算40天前成交量的排名。最后，因子值为VWAP偏斜度排名与40天前成交量排名的差值。这个因子试图捕捉近期价格分布的偏斜程度与历史成交量活跃度之间的关系。当近期VWAP偏斜度排名高于历史成交量排名时，可能表明市场在近期价格波动方面表现出更强的非对称性，而历史成交量较低，这种差异可能预示着潜在的市场情绪变化或资金流动的异常。创新点在于结合了不同时间窗口下的价格偏斜度和历史成交量信息，并通过排名操作符进行比较，突出两者相对强弱的差异，而非简单的叠加或乘积关系。
    因子应用场景：
    1. 识别市场情绪变化：通过比较价格偏斜度和成交量排名，辅助判断市场情绪的转变。
    2. 发现潜在的交易机会：在价格偏斜度排名显著高于成交量排名时，可能预示着潜在的买入或卖出机会。
    """
    # 1. 计算 ts_skewness(vwap, 22)
    data_ts_skewness_vwap = ts_skewness(data['vwap'], 22)
    # 2. 计算 rank(ts_skewness(vwap, 22))
    data_rank_ts_skewness_vwap = rank(data_ts_skewness_vwap, 2)
    # 3. 计算 ts_delay(vol, 40)
    data_ts_delay_vol = ts_delay(data['vol'], 40)
    # 4. 计算 rank(ts_delay(vol, 40))
    data_rank_ts_delay_vol = rank(data_ts_delay_vol, 2)
    # 5. 计算 subtract(rank(ts_skewness(vwap, 22)), rank(ts_delay(vol, 40)))
    factor = subtract(data_rank_ts_skewness_vwap, data_rank_ts_delay_vol, filter = False)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()