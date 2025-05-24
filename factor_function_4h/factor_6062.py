import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_skewness, ts_delta, ts_std_dev

def factor_6062(data, **kwargs):
    """
    因子名称: Volatility_Skew_Momentum_Correlation_79351
    数学表达式: ts_corr(ts_skewness(low, 15), ts_delta(ts_std_dev(close, 20), 5), 10)
    中文描述: 该因子旨在捕捉最低价偏度与收盘价波动率变化之间的相关性。首先，计算过去15天最低价的偏度，衡量低价分布的不对称性。其次，计算过去20天收盘价的标准差（衡量波动率），并计算其在过去5天内的变化。最后，计算最低价偏度序列与收盘价波动率变化序列在过去10天内的滚动相关性。这个因子结合了价格分布的形态信息（偏度）和价格波动性的变化趋势，通过相关性来识别市场情绪和价格动量的潜在联系。创新点在于结合了偏度和波动率变化这两个不同的维度，并通过相关性来衡量它们之间的动态关系，可能用于识别市场情绪的极端情况或波动率驱动的趋势。
    因子应用场景：
    1. 市场情绪识别： 通过最低价偏度和波动率变化的相关性，识别市场情绪的极端情况。
    2. 波动率驱动的趋势识别： 识别由波动率变化驱动的价格动量。
    3. 风险管理： 评估市场风险，特别是在市场情绪不稳定或波动率异常变化时。
    """
    # 1. 计算 ts_skewness(low, 15)
    data_ts_skewness_low = ts_skewness(data['low'], d=15)
    # 2. 计算 ts_std_dev(close, 20)
    data_ts_std_dev_close = ts_std_dev(data['close'], d=20)
    # 3. 计算 ts_delta(ts_std_dev(close, 20), 5)
    data_ts_delta_ts_std_dev_close = ts_delta(data_ts_std_dev_close, d=5)
    # 4. 计算 ts_corr(ts_skewness(low, 15), ts_delta(ts_std_dev(close, 20), 5), 10)
    factor = ts_corr(data_ts_skewness_low, data_ts_delta_ts_std_dev_close, d=10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()