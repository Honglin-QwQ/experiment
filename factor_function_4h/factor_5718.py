import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_delta, log_diff, divide

def factor_5718(data, **kwargs):
    """
    因子名称: TsDeltaLowZscoreInverseLogDiffVWAP_59063
    数学表达式: divide(ts_zscore(ts_delta(low, 3), 22), log_diff(vwap))
    中文描述: 该因子结合了最低价的短期波动标准化和VWAP的对数差分。首先计算过去3天最低价的变化，并在过去22天内进行Z分数标准化，以衡量最低价波动的相对强度。然后计算VWAP的对数差分，反映VWAP的相对变化率。最后，将标准化后的最低价波动除以VWAP的对数差分。这个因子试图捕捉短期价格波动与成交量加权平均价格变化之间的关系，可能用于识别在不同市场条件下表现出特定波动模式的股票。创新点在于结合了两种不同类型的价格动量指标，并通过除法构建了新的关系，同时参考了用户提供的两个因子中的核心计算逻辑。
    因子应用场景：
    1. 波动性分析：用于识别价格波动与成交量变化之间存在特定关系的股票。
    2. 市场情绪判断：结合价格波动和成交量变化，辅助判断市场情绪。
    """
    # 1. 计算 ts_delta(low, 3)
    data_ts_delta_low = ts_delta(data['low'], d=3)
    # 2. 计算 ts_zscore(ts_delta(low, 3), 22)
    data_ts_zscore = ts_zscore(data_ts_delta_low, d=22)
    # 3. 计算 log_diff(vwap)
    data_log_diff_vwap = log_diff(data['vwap'])
    # 4. 计算 divide(ts_zscore(ts_delta(low, 3), 22), log_diff(vwap))
    factor = divide(data_ts_zscore, data_log_diff_vwap)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()