import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_arg_max, ts_std_dev, divide, add

def factor_5727(data, **kwargs):
    """
    因子名称: VWAP_Volatility_ArgMax_Ratio_40977
    数学表达式: divide(ts_arg_max(vwap, 22), add(ts_std_dev(vwap, 5), 1e-6))
    中文描述: 该因子结合了VWAP的长期最大值位置和短期波动性。它计算过去22天VWAP最大值出现的相对天数，并将其除以过去5天VWAP的标准差。
    通过将长期价格趋势的峰值位置与短期价格波动性相结合，该因子试图捕捉在价格达到近期高点后，其波动性对未来趋势的影响。
    分母中加入一个小的常数1e-6是为了避免除以零。因子的创新点在于结合了时间序列位置信息（ts_arg_max）和时间序列统计信息（ts_std_dev），
    并以比率形式呈现，可能用于识别价格动能衰减或反转的信号。

    因子应用场景：
    1. 动能衰减识别：当因子值较高时，可能表明价格在达到近期高点后，波动性相对较低，预示着动能可能衰减。
    2. 反转信号：因子值突然降低可能表明价格波动性增加，潜在的反转风险增加。
    """
    # 1. 计算 ts_arg_max(vwap, 22)
    data_ts_arg_max_vwap = ts_arg_max(data['vwap'], d=22)
    # 2. 计算 ts_std_dev(vwap, 5)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], d=5)
    # 3. 计算 add(ts_std_dev(vwap, 5), 1e-6)
    data_add = add(data_ts_std_dev_vwap, 1e-6)
    # 4. 计算 divide(ts_arg_max(vwap, 22), add(ts_std_dev(vwap, 5), 1e-6))
    factor = divide(data_ts_arg_max_vwap, data_add)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()