import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_sum, ts_delta, divide, ts_std_dev, log, ts_max, ts_min

def factor_5629(data, **kwargs):
    """
    因子名称: factor_0003_77103
    数学表达式: ts_sum(ts_delta(close / ts_std_dev(close, 5), 1), 5) * log(divide(ts_max(high, 3), ts_min(low, 3)))
    中文描述: 该因子是对历史因子factor_0002的改进，旨在提升其预测能力和稳定性。核心改进在于缩短了标准差的计算窗口，从而对收盘价进行波动率标准化。这样的处理可以降低高波动率时期价格的影响，同时放大低波动率时期价格的影响，从而使因子对市场变化的敏感度更高。该因子结合了波动率调整后的收盘价的平方和与最高价和最低价的比率的对数，旨在捕捉价格波动幅度和范围之间的关系，可能用于识别市场趋势的强度和潜在的反转点。此外，通过除以波动率，该因子在不同市场条件下的适应性更强。
    因子应用场景：
    1. 趋势识别：用于识别市场趋势的强度。
    2. 反转点识别：可能用于识别潜在的反转点。
    3. 波动率调整：在不同市场条件下的适应性更强。
    """
    # 1. 计算 ts_std_dev(close, 5)
    data_ts_std_dev = ts_std_dev(data['close'], 5)
    # 2. 计算 close / ts_std_dev(close, 5)
    data_divide = divide(data['close'], data_ts_std_dev)
    # 3. 计算 ts_delta(close / ts_std_dev(close, 5), 1)
    data_ts_delta = ts_delta(data_divide, 1)
    # 4. 计算 ts_sum(ts_delta(close / ts_std_dev(close, 5), 1), 5)
    data_ts_sum = ts_sum(data_ts_delta, 5)
    # 5. 计算 ts_max(high, 3)
    data_ts_max = ts_max(data['high'], 3)
    # 6. 计算 ts_min(low, 3)
    data_ts_min = ts_min(data['low'], 3)
    # 7. 计算 divide(ts_max(high, 3), ts_min(low, 3))
    data_divide_max_min = divide(data_ts_max, data_ts_min)
    # 8. 计算 log(divide(ts_max(high, 3), ts_min(low, 3)))
    data_log = log(data_divide_max_min)
    # 9. 计算 ts_sum(ts_delta(close / ts_std_dev(close, 5), 1), 5) * log(divide(ts_max(high, 3), ts_min(low, 3)))
    factor = data_ts_sum * data_log

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()