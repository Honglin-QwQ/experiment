import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, multiply, ts_std_dev, ts_delta, divide

def factor_5955(data, **kwargs):
    """
    因子名称: VolumeWeightedPriceDeltaSkew_94626
    数学表达式: divide(ts_skewness(multiply(close, vol), 15), ts_std_dev(ts_delta(close, 5), 25))
    中文描述: 该因子计算过去15天收盘价与成交量乘积（成交额代理）的偏度与过去25天收盘价5日差值的标准差之比。在参考因子基础上，该因子调整了时间窗口参数，将偏度计算窗口从20天调整为15天，将标准差计算窗口从30天调整为25天，并将价格差值的滞后天数从10天调整为5天。这些调整旨在捕捉更近期的市场动态和价格变化速率的波动性。通过调整参数，该因子试图在保留原因子核心逻辑的同时，提高对短期市场情绪和资金流动的敏感度，以期在不同市场环境下表现更优。相较于参考因子，创新点在于参数的优化调整，以适应更短期的市场特征。
    因子应用场景：
    1. 短期市场情绪捕捉： 适用于需要快速反应市场情绪变化的策略，例如日内交易或短线波段交易。
    2. 资金流动敏感度： 适用于追踪资金流动对股价影响的策略，例如量化选股或事件驱动型交易。
    """
    # 1. 计算 multiply(close, vol)
    data_multiply = multiply(data['close'], data['vol'])
    # 2. 计算 ts_skewness(multiply(close, vol), 15)
    data_ts_skewness = ts_skewness(data_multiply, d=15)
    # 3. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], d=5)
    # 4. 计算 ts_std_dev(ts_delta(close, 5), 25)
    data_ts_std_dev = ts_std_dev(data_ts_delta, d=25)
    # 5. 计算 divide(ts_skewness(multiply(close, vol), 15), ts_std_dev(ts_delta(close, 5), 25))
    factor = divide(data_ts_skewness, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()