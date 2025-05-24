import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, divide, ts_std_dev

def factor_5899(data, **kwargs):
    """
    数学表达式: ts_skewness(divide(volume, ts_std_dev(volume, 20)), 60)
    中文描述: 该因子计算标准化成交量（成交量除以其20天标准差）在过去60天内的偏度。标准化成交量可以衡量当前成交量相对于近期平均波动的极端程度。计算其长期偏度旨在捕捉成交量分布的非对称性，例如是否存在频繁的大幅放量或缩量。正偏度可能表明存在突然放量的情况，而负偏度可能表明存在持续缩量的情况。这可以用于识别市场情绪的潜在变化或交易活动的异常模式。相较于参考因子，该因子创新性地结合了成交量的标准化处理和长期偏度计算，以更全面地捕捉成交量特征。
    因子应用场景：
    1. 识别市场情绪变化：通过观察偏度变化，可以识别市场情绪的潜在变化，例如从缩量到放量的转变。
    2. 交易活动异常模式识别：可以用于识别交易活动的异常模式，例如是否存在频繁的大幅放量或缩量。
    3. 量化交易策略：该因子可以作为量化交易策略的输入特征，用于预测股票价格的变动。
    """
    # 1. 计算 ts_std_dev(volume, 20)
    volume_std = ts_std_dev(data['vol'], d=20)
    # 2. 计算 divide(volume, ts_std_dev(volume, 20))
    normalized_volume = divide(data['vol'], volume_std)
    # 3. 计算 ts_skewness(divide(volume, ts_std_dev(volume, 20)), 60)
    factor = ts_skewness(normalized_volume, d=60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()