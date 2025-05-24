import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_delta, ts_rank

def factor_5901(data, **kwargs):
    """
    因子名称: VolRankChangeSkewness_63686
    数学表达式: ts_skewness(ts_delta(ts_rank(vol, 15), 1), 25)
    中文描述: 该因子旨在捕捉成交量排名的短期变化趋势的偏度。首先，计算过去15天成交量（vol）的排名，相比于参考因子的10天窗口，使用了稍长的窗口以平衡短期敏感性和稳定性。然后计算当前排名与1天前排名的差值，关注成交量排名的日度变化。最后，计算这个日度变化在过去25天内的偏度。偏度衡量了数据分布的不对称性。正偏度表示数据分布右侧尾部较长，可能有较多较大的正向变化；负偏度表示数据分布左侧尾部较长，可能有较多较大的负向变化。这个因子通过分析成交量排名变化的偏度，尝试识别市场情绪的非对称性变化，例如是否存在突然的放量上涨或缩量下跌。创新点在于引入了偏度操作符（ts_skewness）来分析成交量排名变化的分布特征，而非简单地计算均值或标准差，这可能揭示更深层次的市场行为模式。参考了历史评估结果中关于预测能力不稳定和可能存在非线性关系的建议，通过分析偏度，尝试捕捉非线性的市场情绪变化。
    因子应用场景：
    1. 识别市场情绪的非对称性变化，例如是否存在突然的放量上涨或缩量下跌。
    2. 辅助判断市场趋势，正偏度可能预示上涨趋势，负偏度可能预示下跌趋势。
    """
    # 1. 计算 ts_rank(vol, 15)
    data_ts_rank_vol = ts_rank(data['vol'], 15)
    # 2. 计算 ts_delta(ts_rank(vol, 15), 1)
    data_ts_delta = ts_delta(data_ts_rank_vol, 1)
    # 3. 计算 ts_skewness(ts_delta(ts_rank(vol, 15), 1), 25)
    factor = ts_skewness(data_ts_delta, 25)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()