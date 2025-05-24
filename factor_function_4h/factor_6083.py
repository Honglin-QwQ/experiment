import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_scale, ts_co_skewness, log, add, ts_kurtosis, ts_std_dev

def factor_6083(data, **kwargs):
    """
    因子名称: VolumePriceVolatilitySkewness_97700
    数学表达式: ts_scale(ts_co_skewness(log(add(vol,1)), close, 60)) + ts_scale(ts_kurtosis(amount, 90)) - ts_scale(ts_std_dev(trades, 30))
    中文描述: 该因子旨在捕捉量价关系的非线性特征、交易额的尾部风险以及交易活跃度的短期波动。第一部分计算对数化成交量与收盘价在过去60天内的协偏度（co-skewness），并进行时间序列标准化，捕捉量价分布的非对称性；第二部分计算交易额在过去90天内的峰度（kurtosis），并进行时间序列标准化，衡量交易额分布的尖峭程度和尾部风险；第三部分计算交易笔数在过去30天内的标准差，并进行时间序列标准化后取负，反映交易活跃度的短期波动性。将这三部分结合，旨在从高阶统计量和不同时间窗口捕捉更复杂的市场动态。创新点在于引入了协偏度和峰度这两个高阶统计量来分析量价关系和交易额分布，并结合了不同时间窗口的标准差来衡量交易活跃度的波动性。这相较于参考因子仅使用相关性和Z-score，提供了更丰富的统计信息。
    因子应用场景：
    1. 异常波动识别：高协偏度或高峰度可能预示着交易行为的异常，可用于识别潜在的市场风险或机会。
    2. 交易活跃度变化：交易笔数标准差的变化可以作为交易活跃度短期变化的信号。
    3. 结合其他因子：该因子可以与其他因子结合，构建更全面的量化策略。
    """
    # 1. 计算 add(vol,1)
    data_add = add(data['vol'], 1)
    # 2. 计算 log(add(vol,1))
    data_log = log(data_add)
    # 3. 计算 ts_co_skewness(log(add(vol,1)), close, 60)
    data_ts_co_skewness = ts_co_skewness(data_log, data['close'], 60)
    # 4. 计算 ts_scale(ts_co_skewness(log(add(vol,1)), close, 60))
    factor1 = ts_scale(data_ts_co_skewness)
    # 5. 计算 ts_kurtosis(amount, 90)
    data_ts_kurtosis = ts_kurtosis(data['amount'], 90)
    # 6. 计算 ts_scale(ts_kurtosis(amount, 90))
    factor2 = ts_scale(data_ts_kurtosis)
    # 7. 计算 ts_std_dev(trades, 30)
    data_ts_std_dev = ts_std_dev(data['trades'], 30)
    # 8. 计算 ts_scale(ts_std_dev(trades, 30))
    factor3 = ts_scale(data_ts_std_dev)
    # 9. 计算 ts_scale(ts_co_skewness(log(add(vol,1)), close, 60)) + ts_scale(ts_kurtosis(amount, 90)) - ts_scale(ts_std_dev(trades, 30))
    factor = factor1 + factor2 - factor3

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()