import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, abs, ts_max_diff, divide

def factor_5948(data, **kwargs):
    """
    因子名称: Volatility_MaxDiff_Ratio_95225
    数学表达式: divide(ts_std_dev(close, 60), abs(ts_max_diff(open, 120)))
    中文描述: 该因子计算了过去60天收盘价标准差与过去120天开盘价最大差值绝对值的比率。标准差衡量了短期价格波动性，而最大差值反映了长期价格偏离历史高点的程度。通过这个比率，我们可以评估短期波动相对于长期价格回撤的强度。较高的比率可能表明在经历了一段时间的下跌后，短期波动正在加剧，可能预示着潜在的反转机会；较低的比率则可能意味着价格波动相对稳定，长期趋势可能持续。这是一种结合短期波动和长期价格偏离的创新性因子，用于识别潜在的趋势变化和风险水平。
    因子应用场景：
    1. 反转机会识别：较高的比率可能表明在经历了一段时间的下跌后，短期波动正在加剧，可能预示着潜在的反转机会。
    2. 趋势稳定性评估：较低的比率则可能意味着价格波动相对稳定，长期趋势可能持续。
    3. 风险水平评估：通过结合短期波动和长期价格偏离，评估潜在的趋势变化和风险水平。
    """
    # 1. 计算 ts_std_dev(close, 60)
    data_ts_std_dev_close = ts_std_dev(data['close'], 60)
    # 2. 计算 ts_max_diff(open, 120)
    data_ts_max_diff_open = ts_max_diff(data['open'], 120)
    # 3. 计算 abs(ts_max_diff(open, 120))
    data_abs_ts_max_diff_open = abs(data_ts_max_diff_open)
    # 4. 计算 divide(ts_std_dev(close, 60), abs(ts_max_diff(open, 120)))
    factor = divide(data_ts_std_dev_close, data_abs_ts_max_diff_open)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()