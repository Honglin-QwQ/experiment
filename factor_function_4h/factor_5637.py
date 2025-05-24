import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, ts_skewness

def factor_5637(data, **kwargs):
    """
    因子名称: factor_volatility_adjusted_low_skew_47934
    数学表达式: divide(low, ts_std_dev(low, 20)) * ts_skewness(low, 20)
    中文描述: 该因子是对历史因子factor_volatility_adjusted_low的改进，通过将经波动率调整后的最低价与过去20天最低价的偏度相乘，进一步衡量价格分布的非对称性。正偏度表明价格下跌的概率较小，而负偏度表明价格下跌的概率较大。该因子旨在识别在不同波动率和偏度环境下的真实价格支撑水平，从而提高因子在不同市场条件下的鲁棒性。
    因子应用场景：
    1. 价格支撑识别：用于识别在不同波动率和偏度环境下的价格支撑水平。
    2. 风险评估：结合偏度信息，评估价格下跌的潜在风险。
    3. 市场条件适应性：提高因子在不同市场条件下的鲁棒性。
    """
    # 1. 计算 ts_std_dev(low, 20)
    data_ts_std_dev = ts_std_dev(data['low'], d=20)
    # 2. 计算 divide(low, ts_std_dev(low, 20))
    data_divide = divide(data['low'], data_ts_std_dev)
    # 3. 计算 ts_skewness(low, 20)
    data_ts_skewness = ts_skewness(data['low'], d=20)
    # 4. 计算 divide(low, ts_std_dev(low, 20)) * ts_skewness(low, 20)
    factor = data_divide * data_ts_skewness

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()