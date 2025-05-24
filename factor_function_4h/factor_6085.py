import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_scale, divide, ts_std_dev, ts_mean

def factor_6085(data, **kwargs):
    """
    数学表达式: ts_scale(divide(ts_std_dev(high, 10), ts_mean(high, 10)), 60, constant = 1)
    中文描述: 该因子计算短期（10天）最高价标准差与平均最高价的比值，并在长期（60天）窗口内进行缩放和常数偏移。这旨在捕捉短期价格波动相对于其平均水平的强度，并将其在更长的历史背景下进行标准化。高值可能表示短期内价格波动剧烈，相对于长期历史波动水平较高，可能预示着潜在的市场机会或风险。
    因子应用场景：
    1. 波动率分析：用于识别短期价格波动相对于其平均水平较高的股票。
    2. 风险管理：高波动率可能预示着更高的投资风险。
    3. 趋势识别：短期波动率的增加可能预示着趋势的开始或结束。
    """
    # 1. 计算 ts_std_dev(high, 10)
    data_ts_std_dev = ts_std_dev(data['high'], 10)
    # 2. 计算 ts_mean(high, 10)
    data_ts_mean = ts_mean(data['high'], 10)
    # 3. 计算 divide(ts_std_dev(high, 10), ts_mean(high, 10))
    data_divide = divide(data_ts_std_dev, data_ts_mean)
    # 4. 计算 ts_scale(divide(ts_std_dev(high, 10), ts_mean(high, 10)), 60, constant = 1)
    factor = ts_scale(data_divide, 60, constant = 1)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()