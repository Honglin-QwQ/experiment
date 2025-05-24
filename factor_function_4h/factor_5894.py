import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_skewness, ts_std_dev

def factor_5894(data, **kwargs):
    """
    数学表达式: divide(ts_skewness(vol, 10), ts_std_dev(vol, 20))
    中文描述: 该因子旨在捕捉成交量分布的偏度和波动性之间的关系。分子部分计算了过去10天成交量的偏度（Skewness），反映了成交量分布的非对称性。正偏度表示成交量分布有长尾在右侧（即存在少量极端高成交量），负偏度表示有长尾在左侧（存在少量极端低成交量）。分母部分计算了过去20天成交量的标准差，反映了成交量的波动性。最后，用成交量的偏度除以成交量的波动性。该因子认为，成交量分布的偏度相对于其波动性，可能提供了关于市场情绪和资金流动的额外信息。例如，在波动性较低的情况下出现显著的正偏度，可能预示着有大资金在特定方向上交易。相较于参考因子，该因子引入了成交量分布的偏度，提供了对成交量更深层次的分析，并简化了结构，专注于成交量本身的统计特征。可以应用于识别异常成交量模式、判断市场情绪或作为其他因子的补充。
    因子应用场景：
    1. 识别异常成交量模式
    2. 判断市场情绪
    3. 作为其他因子的补充
    """
    # 1. 计算 ts_skewness(vol, 10)
    data_ts_skewness_vol = ts_skewness(data['vol'], d = 10)
    # 2. 计算 ts_std_dev(vol, 20)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], d = 20)
    # 3. 计算 divide(ts_skewness(vol, 10), ts_std_dev(vol, 20))
    factor = divide(data_ts_skewness_vol, data_ts_std_dev_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()