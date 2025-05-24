import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, log, add

def factor_5597(data, **kwargs):
    """
    因子名称: volume_weighted_amplitude_ratio_20880
    数学表达式: divide(amplitude, ts_std_dev(amplitude, 20)) * log(add(1, vol))
    中文描述: 该因子是在历史因子amplitude_volatility_ratio的基础上，引入成交量信息，对振幅波动率比率进行加权调整。首先计算振幅因子与振幅因子过去20天标准差的比率，得到一个衡量相对波动性的指标。然后，将该比率与成交量的自然对数（加1是为了避免对0取对数）相乘，使得成交量越大，因子值越大，反之亦然。创新点在于结合了量价关系，认为成交量可以验证振幅的有效性，成交量放大时，振幅的波动性可能更具有趋势指示意义。适用于识别短期内价格波动异常且成交量放大的股票，辅助判断市场风险和趋势强度。
    因子应用场景：
    1. 识别短期内价格波动异常且成交量放大的股票。
    2. 辅助判断市场风险和趋势强度。
    """
    # 计算振幅因子
    data['amplitude'] = data['high'] - data['low']
    # 1. 计算 ts_std_dev(amplitude, 20)
    data_ts_std_dev = ts_std_dev(data['amplitude'], 20)
    # 2. 计算 divide(amplitude, ts_std_dev(amplitude, 20))
    data_divide = divide(data['amplitude'], data_ts_std_dev)
    # 3. 计算 add(1, vol)
    data_add = add(1, data['vol'])
    # 4. 计算 log(add(1, vol))
    data_log = log(data_add)
    # 5. 计算 divide(amplitude, ts_std_dev(amplitude, 20)) * log(add(1, vol))
    factor = data_divide * data_log

    # 删除中间变量
    del data['amplitude']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()