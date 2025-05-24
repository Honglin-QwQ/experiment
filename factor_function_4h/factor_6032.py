import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_skewness, ts_std_dev

def factor_6032(data, **kwargs):
    """
    数学表达式: divide(ts_skewness(vwap, 30), ts_std_dev(vwap, 20))
    中文描述: 该因子衡量成交量加权平均价（VWAP）的偏度与标准差之比。首先计算过去30天VWAP的偏度，捕捉价格分布的极端情况。然后计算过去20天VWAP的标准差，衡量价格波动性。最后，将偏度除以标准差。该因子创新性地将偏度与波动性结合，并使用不同时间窗口进行计算。较高的因子值可能表明在相对较低的波动性下存在显著的偏度，这可能预示着潜在的市场机会或风险。该因子相较于参考因子，通过引入标准差作为分母，对偏度进行了波动性调整，提供了更具风险调整意义的市场情绪指标。同时，使用了不同的时间窗口，增加了因子的创新性。
    因子应用场景：
    1. 市场情绪分析：用于识别市场的乐观或悲观情绪。
    2. 风险评估：用于评估市场潜在的风险水平。
    3. 交易信号生成：结合其他技术指标，生成交易信号。
    """
    # 1. 计算 ts_skewness(vwap, 30)
    data_ts_skewness = ts_skewness(data['vwap'], 30)
    # 2. 计算 ts_std_dev(vwap, 20)
    data_ts_std_dev = ts_std_dev(data['vwap'], 20)
    # 3. 计算 divide(ts_skewness(vwap, 30), ts_std_dev(vwap, 20))
    factor = divide(data_ts_skewness, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()