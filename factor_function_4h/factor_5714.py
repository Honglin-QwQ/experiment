import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_delta, ts_std_dev

def factor_5714(data, **kwargs):
    """
    数学表达式: ts_corr(volume, ts_delta(volume, 3), 5) * ts_std_dev(volume, 10)
    中文描述: 该因子结合了短期成交量的动量和波动性。它首先计算当前成交量与3天前成交量变化的相关性，捕捉成交量的短期趋势。然后，将这个相关性与过去10天的成交量标准差相乘，引入了成交量的波动性信息。高因子值可能表明成交量在短期内呈现出较强的趋势性变化，并且伴随着较高的波动性，这可能预示着价格的快速变动。相对于参考因子，该因子通过引入相关性和标准差的组合，更全面地刻画了成交量的动态特征，而非仅仅依赖于均值或极值。
    因子应用场景：
    1. 成交量趋势判断：用于判断成交量在短期内是否存在明显的趋势。
    2. 波动性分析：结合成交量的波动性，判断市场活跃程度。
    3. 预判价格变动：高因子值可能预示着价格的快速变动。
    """
    # 1. 计算 ts_delta(volume, 3)
    data_ts_delta = ts_delta(data['vol'], 3)
    # 2. 计算 ts_corr(volume, ts_delta(volume, 3), 5)
    data_ts_corr = ts_corr(data['vol'], data_ts_delta, 5)
    # 3. 计算 ts_std_dev(volume, 10)
    data_ts_std_dev = ts_std_dev(data['vol'], 10)
    # 4. 计算 ts_corr(volume, ts_delta(volume, 3), 5) * ts_std_dev(volume, 10)
    factor = data_ts_corr * data_ts_std_dev

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()