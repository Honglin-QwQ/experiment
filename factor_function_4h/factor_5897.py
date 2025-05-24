import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delta, ts_entropy

def factor_5897(data, **kwargs):
    """
    数学表达式: ts_std_dev(ts_delta(close, 5), 30) - ts_entropy(ts_delta(close, 5), 30)
    中文描述: 该因子计算了收盘价5日变化的30日标准差与收盘价5日变化的30日信息熵之差。标准差衡量了价格波动的绝对幅度，而信息熵衡量了价格波动的复杂性和不可预测性。当标准差较高而信息熵较低时，可能表明存在强烈的单边趋势；反之，当标准差较低而信息熵较高时，可能表明市场处于震荡且难以预测的状态。该因子旨在捕捉价格波动幅度和波动模式之间的差异，以识别潜在的趋势或震荡行情。创新点在于结合了标准差和信息熵这两种不同的波动性度量方法，通过计算它们的差值来揭示市场状态的细微变化。
    因子应用场景：
    1. 趋势识别：用于识别市场趋势，当标准差远大于信息熵时，可能预示着趋势的开始或延续。
    2. 震荡行情判断：当信息熵接近或大于标准差时，可能表明市场处于震荡状态，交易难度增加。
    3. 波动性风险评估：通过观察因子值的变化，评估市场波动性风险，辅助仓位管理。
    """
    # 1. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], 5)
    # 2. 计算 ts_std_dev(ts_delta(close, 5), 30)
    data_ts_std_dev = ts_std_dev(data_ts_delta, 30)
    # 3. 计算 ts_entropy(ts_delta(close, 5), 30)
    data_ts_entropy = ts_entropy(data_ts_delta, 30)
    # 4. 计算 ts_std_dev(ts_delta(close, 5), 30) - ts_entropy(ts_delta(close, 5), 30)
    factor = data_ts_std_dev - data_ts_entropy

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()