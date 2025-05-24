import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_entropy, abs, multiply

def factor_5618(data, **kwargs):
    """
    因子名称: factor_0001_50038
    数学表达式: ts_delta(returns,67) * ts_entropy(abs(ts_delta(returns,67)), 20)
    中文描述: 该因子结合了收益率变化和收益率变化信息熵的概念。首先计算过去67天收益率的变化，然后计算该变化绝对值在过去20天内的信息熵。该因子旨在捕捉收益率变化的不确定性和趋势持续性。创新点在于将收益率变化幅度与信息熵结合，以此来识别趋势的稳定性和潜在风险。
    因子应用场景：
    1. 趋势识别：该因子可能用于识别收益率变化趋势，结合信息熵来判断趋势的稳定性和风险。
    2. 风险评估：通过信息熵评估收益率变化的不确定性，可能用于风险评估。
    """
    # 1. 计算 ts_delta(returns, 67)
    data_ts_delta = ts_delta(data['returns'], d=67)

    # 2. 计算 abs(ts_delta(returns, 67))
    data_abs_ts_delta = abs(data_ts_delta)

    # 3. 计算 ts_entropy(abs(ts_delta(returns, 67)), 20)
    data_ts_entropy = ts_entropy(data_abs_ts_delta, d=20)

    # 4. 计算 ts_delta(returns,67) * ts_entropy(abs(ts_delta(returns,67)), 20)
    factor = multiply(data_ts_delta, data_ts_entropy)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()