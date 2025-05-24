import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_std_dev, ts_max, ts_min, quantile

def factor_5659(data, **kwargs):
    """
    因子名称: factor_volume_price_momentum_quantile_27878
    数学表达式: quantile(ts_corr(close, vol, 3) * ts_std_dev(amount, 5) / (ts_max(high, 3) - ts_min(low, 3)))
    中文描述: 该因子旨在捕捉价格与成交量相关性的动量，并结合成交额的波动性进行分析。首先计算收盘价与成交量在过去3天的相关性，然后将这个相关性与过去5天成交额的标准差相乘，以衡量市场活跃程度对价量关系的影响。最后，将结果除以过去3天的价格范围，以对结果进行标准化，消除价格范围的影响。与之前的因子相比，移除了ts_delta操作，简化了因子结构，减少了噪音。最重要的是，使用quantile函数对因子进行非线性转换，将因子值转换为分位数，增强了因子的区分度，提升了因子在不同股票之间的区分能力。
    因子应用场景：
    1. 市场活跃度分析：通过成交量与价格的相关性及成交额的标准差，评估市场活跃度对价格的影响。
    2. 价格范围标准化：通过价格范围进行标准化，消除价格绝对值的影响，关注相对价格波动。
    3. 量价关系识别：识别量价关系异常的股票，辅助判断趋势反转或持续的可能性。
    """
    # 1. 计算 ts_corr(close, vol, 3)
    data_ts_corr = ts_corr(data['close'], data['vol'], 3)
    # 2. 计算 ts_std_dev(amount, 5)
    data_ts_std_dev = ts_std_dev(data['amount'], 5)
    # 3. 计算 ts_max(high, 3)
    data_ts_max = ts_max(data['high'], 3)
    # 4. 计算 ts_min(low, 3)
    data_ts_min = ts_min(data['low'], 3)
    # 5. 计算 (ts_max(high, 3) - ts_min(low, 3))
    data_diff = data_ts_max - data_ts_min
    # 6. 计算 ts_corr(close, vol, 3) * ts_std_dev(amount, 5)
    data_multiply = data_ts_corr * data_ts_std_dev
    # 7. 计算 ts_corr(close, vol, 3) * ts_std_dev(amount, 5) / (ts_max(high, 3) - ts_min(low, 3))
    factor = data_multiply / data_diff

    # 8. 计算 quantile(ts_corr(close, vol, 3) * ts_std_dev(amount, 5) / (ts_max(high, 3) - ts_min(low, 3)))
    factor = quantile(factor)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()