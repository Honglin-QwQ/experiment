import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, ts_std_dev, abs, ts_skewness, divide

def factor_5831(data, **kwargs):
    """
    因子名称: VolatilitySkewDecayRatio_47868
    数学表达式: divide(ts_decay_linear(ts_std_dev(vol, 15), 8), abs(ts_skewness(vol, 8)))
    中文描述: 该因子旨在捕捉成交量波动性的线性衰减趋势与成交量偏度的比率。它计算了过去15天成交量标准差的8天线性衰减值，并除以过去8天成交量偏度的绝对值。高因子值可能表明股票近期成交量波动性呈现较强的线性衰减趋势，同时成交量分布的偏度绝对值较小（即分布更对称）。这可能预示着市场情绪趋于稳定或潜在的趋势反转。相较于参考因子，本因子将波动性排名与偏度排名相乘的结构替换为波动性衰减与偏度绝对值的比率，并调整了时间窗口，同时使用了建议中提到的divide和abs操作符，旨在捕捉成交量波动性和分布特征的相对关系，并增强因子的鲁棒性。
    因子应用场景：
    1. 趋势识别：当因子值较高时，表明成交量波动性呈现较强的线性衰减趋势，可能意味着市场情绪趋于稳定。
    2. 反转信号：因子值较高可能预示着潜在的趋势反转。
    3. 稳定性分析：因子值较高可能表明市场趋于稳定。
    """
    # 1. 计算 ts_std_dev(vol, 15)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], 15)
    # 2. 计算 ts_decay_linear(ts_std_dev(vol, 15), 8)
    data_ts_decay_linear = ts_decay_linear(data_ts_std_dev_vol, 8)
    # 3. 计算 ts_skewness(vol, 8)
    data_ts_skewness_vol = ts_skewness(data['vol'], 8)
    # 4. 计算 abs(ts_skewness(vol, 8))
    data_abs_ts_skewness_vol = abs(data_ts_skewness_vol)
    # 5. 计算 divide(ts_decay_linear(ts_std_dev(vol, 15), 8), abs(ts_skewness(vol, 8)))
    factor = divide(data_ts_decay_linear, data_abs_ts_skewness_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()