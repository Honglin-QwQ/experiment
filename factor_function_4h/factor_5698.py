import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_skewness, divide

def factor_5698(data, **kwargs):
    """
    数学表达式: divide(ts_std_dev(vwap, 10), ts_skewness(vwap, 10))
    中文描述: 该因子旨在捕捉VWAP在过去一段时间内的波动性和偏度之间的关系。首先计算过去10天VWAP的标准差 (ts_std_dev(vwap, 10))，衡量VWAP的波动程度。然后计算过去10天VWAP的偏度 (ts_skewness(vwap, 10))，衡量VWAP分布的对称性。最后将标准差除以偏度。较高的因子值可能表明在VWAP波动较大的同时，其分布向负方向倾斜（偏度为负），这可能预示着潜在的下行风险。相较于参考因子，创新点在于结合了VWAP的波动性和偏度这两个统计特征，通过它们的比例来衡量市场情绪和潜在风险。同时参考了历史输出的改进建议，使用了更具统计意义的指标并调整了时间窗口。
    因子应用场景：
    1. 风险预警：当因子值异常高时，可能预示着市场潜在的下行风险，提醒投资者注意风险控制。
    2. 趋势判断：结合其他技术指标，辅助判断市场趋势，例如，因子值持续升高可能预示着下跌趋势。
    3. 策略优化：在量化交易策略中，可以作为筛选股票的条件之一，例如，选择因子值较低的股票进行投资。
    """
    # 1. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 10)
    # 2. 计算 ts_skewness(vwap, 10)
    data_ts_skewness_vwap = ts_skewness(data['vwap'], 10)
    # 3. 计算 divide(ts_std_dev(vwap, 10), ts_skewness(vwap, 10))
    factor = divide(data_ts_std_dev_vwap, data_ts_skewness_vwap)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()