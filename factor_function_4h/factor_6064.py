import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_rank, adv, divide

def factor_6064(data, **kwargs):
    """
    因子名称: VWAP_Volume_Correlation_Rank_Ratio_84006
    数学表达式: divide(ts_rank(ts_corr(vwap, vol, 10), 5), ts_rank(adv(vol, 20), 15))
    中文描述: 该因子旨在衡量短期VWAP与成交量相关性的排名相对于长期平均成交量排名的比率。首先，计算过去10天VWAP与成交量的滚动相关性。然后，计算这个滚动相关性在过去5天内的排名。同时，计算过去20天平均成交量在过去15天内的排名。最后，将短期相关性排名除以长期平均成交量排名。这个比率可以反映短期价量关系的重要性相对于长期成交量趋势的重要性。高比率可能表明短期市场情绪和交易行为对价格影响较大，而低比率可能表明长期成交量趋势更具主导性。创新点在于结合了短期价量相关性和长期平均成交量，并通过排名和比率的形式来捕捉它们之间的相对强度，同时根据评估报告的建议，调整了时间窗口参数，并简化了因子结构，移除了复杂的熵计算，以期提高因子的有效性和可解释性。
    因子应用场景：
    1. 短期市场情绪分析：用于识别短期市场情绪对价格的影响程度。
    2. 长期成交量趋势分析：用于评估长期成交量趋势在价格形成中的主导性。
    3. 价量关系分析：结合短期价量相关性和长期平均成交量，捕捉它们之间的相对强度。
    """
    # 1. 计算ts_corr(vwap, vol, 10)
    data_ts_corr = ts_corr(data['vwap'], data['vol'], 10)
    # 2. 计算ts_rank(ts_corr(vwap, vol, 10), 5)
    data_ts_rank_corr = ts_rank(data_ts_corr, 5)
    # 3. 计算adv(vol, 20)
    data_adv_vol = adv(data['vol'], 20)
    # 4. 计算ts_rank(adv(vol, 20), 15)
    data_ts_rank_adv = ts_rank(data_adv_vol, 15)
    # 5. 计算divide(ts_rank(ts_corr(vwap, vol, 10), 5), ts_rank(adv(vol, 20), 15))
    factor = divide(data_ts_rank_corr, data_ts_rank_adv)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()