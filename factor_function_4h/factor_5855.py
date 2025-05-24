import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_entropy, divide, subtract, add, rank

def factor_5855(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Entropy_Ratio_Ranked_45178
    数学表达式: divide(rank(ts_std_dev(vwap, 60)), rank(ts_entropy(divide(subtract(close, open), add(subtract(high, low), 0.001)), 60)))
    中文描述: 该因子计算了VWAP在过去60天的标准差的排名与当日价格波动强度（收盘价减开盘价除以日内振幅）在过去60天的信息熵的排名的比值。VWAP标准差衡量了VWAP的波动性，而价格波动强度的信息熵衡量了日内价格波动模式的混乱度。该因子在参考因子基础上，进行了结构和逻辑的创新，将原始因子中的分子和分母进行了互换，并对两者都进行了排名处理，以降低异常值的影响并突出相对强弱。此外，将时间窗口调整为60天，以捕捉中期趋势。较高的因子值可能表明VWAP波动性相对较高，而日内波动模式相对稳定且有序，这可能预示着价格趋势的形成；较低的因子值则可能表明VWAP相对稳定，而日内波动模式混乱且不确定，市场缺乏明确方向。该因子可用于识别市场波动模式的变化和潜在的趋势形成机会。
    因子应用场景：
    1. 波动性分析：用于识别VWAP波动性相对较高，而日内波动模式相对稳定且有序的股票。
    2. 趋势预测：较高的因子值可能预示着价格趋势的形成。
    3. 市场情绪分析：较低的因子值可能表明市场缺乏明确方向。
    """
    # 1. 计算 ts_std_dev(vwap, 60)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 60)
    # 2. 计算 rank(ts_std_dev(vwap, 60))
    data_rank_ts_std_dev_vwap = rank(data_ts_std_dev_vwap)
    # 3. 计算 subtract(close, open)
    data_subtract_close_open = subtract(data['close'], data['open'])
    # 4. 计算 subtract(high, low)
    data_subtract_high_low = subtract(data['high'], data['low'])
    # 5. 计算 add(subtract(high, low), 0.001)
    data_add_subtract_high_low = add(data_subtract_high_low, 0.001)
    # 6. 计算 divide(subtract(close, open), add(subtract(high, low), 0.001))
    data_divide_subtract_close_open = divide(data_subtract_close_open, data_add_subtract_high_low)
    # 7. 计算 ts_entropy(divide(subtract(close, open), add(subtract(high, low), 0.001)), 60)
    data_ts_entropy_divide_subtract_close_open = ts_entropy(data_divide_subtract_close_open, 60)
    # 8. 计算 rank(ts_entropy(divide(subtract(close, open), add(subtract(high, low), 0.001)), 60))
    data_rank_ts_entropy_divide_subtract_close_open = rank(data_ts_entropy_divide_subtract_close_open)
    # 9. 计算 divide(rank(ts_std_dev(vwap, 60)), rank(ts_entropy(divide(subtract(close, open), add(subtract(high, low), 0.001)), 60)))
    factor = divide(data_rank_ts_std_dev_vwap, data_rank_ts_entropy_divide_subtract_close_open)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()