import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_sum, signed_power, ts_std_dev, log, divide, ts_max, ts_min

def factor_5625(data, **kwargs):
    """
    因子名称: factor_0002_96665
    数学表达式: ts_sum(signed_power(close / ts_std_dev(close, 10), 2), 10) * log(divide(ts_max(high, 5), ts_min(low, 5)))
    中文描述: 该因子是对历史因子factor_0001的改进，旨在提升其预测能力和稳定性。核心改进在于将收盘价除以其过去10天的标准差，从而对收盘价进行波动率标准化。这样的处理可以降低高波动率时期价格的影响，同时放大低波动率时期价格的影响，从而使因子对市场变化的敏感度更高。该因子结合了波动率调整后的收盘价的平方和与最高价和最低价的比率的对数，旨在捕捉价格波动幅度和范围之间的关系，可能用于识别市场趋势的强度和潜在的反转点。此外，通过除以波动率，该因子在不同市场条件下的适应性更强。
    因子应用场景：
    1. 波动率标准化：通过将收盘价除以其过去10天的标准差，该因子可以降低高波动率时期价格的影响，同时放大低波动率时期价格的影响，从而使因子对市场变化的敏感度更高。
    2. 趋势强度识别：该因子结合了波动率调整后的收盘价的平方和与最高价和最低价的比率的对数，旨在捕捉价格波动幅度和范围之间的关系，可能用于识别市场趋势的强度和潜在的反转点。
    3. 市场适应性：通过除以波动率，该因子在不同市场条件下的适应性更强。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], 10)
    # 2. 计算 close / ts_std_dev(close, 10)
    data_divide = divide(data['close'], data_ts_std_dev)
    # 3. 计算 signed_power(close / ts_std_dev(close, 10), 2)
    data_signed_power = signed_power(data_divide, 2)
    # 4. 计算 ts_sum(signed_power(close / ts_std_dev(close, 10), 2), 10)
    data_ts_sum = ts_sum(data_signed_power, 10)
    # 5. 计算 ts_max(high, 5)
    data_ts_max = ts_max(data['high'], 5)
    # 6. 计算 ts_min(low, 5)
    data_ts_min = ts_min(data['low'], 5)
    # 7. 计算 divide(ts_max(high, 5), ts_min(low, 5))
    data_divide_max_min = divide(data_ts_max, data_ts_min)
    # 8. 计算 log(divide(ts_max(high, 5), ts_min(low, 5)))
    data_log = log(data_divide_max_min)
    # 9. 计算 ts_sum(signed_power(close / ts_std_dev(close, 10), 2), 10) * log(divide(ts_max(high, 5), ts_min(low, 5)))
    factor = data_ts_sum * data_log

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()