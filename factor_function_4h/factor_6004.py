import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, divide, ts_std_dev, multiply, adv, abs, ts_delta

def factor_6004(data, **kwargs):
    """
    数学表达式: ts_rank(divide(ts_std_dev(close, 10), multiply(adv(volume, 20), abs(ts_delta(close, 5)))), 15)
    中文描述: 该因子在参考因子的基础上进行了创新，计算了过去10天收盘价的标准差（价格波动性）与过去20天平均成交量和过去5天收盘价变化绝对值乘积的比值。最后，计算这个比值在过去15天内的排名。与参考因子直接相乘不同，这里使用了除法，旨在捕捉在特定成交量和价格变化下的单位价格波动。高排名可能表明在相对较高的成交量和价格变化下，价格波动性仍然显著，这可能预示着市场力量的对比变化或趋势的延续。该因子创新性地将价格波动性与成交量和价格变化结合，通过比值关系和排名来衡量其相对强度，适用于捕捉量价关系异常下的交易机会。改进方向上，考虑到原因子负向预测能力，通过除法可能改变因子与未来收益率的关系。同时，保留了时间序列排名，但调整了内部计算逻辑。
    因子应用场景：
    1. 量价关系异常识别：适用于识别在特定成交量和价格变化下的单位价格波动异常增大的情况。
    2. 市场力量对比变化：高排名可能预示着市场力量的对比变化或趋势的延续。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], 10)
    # 2. 计算 adv(volume, 20)
    data_adv = adv(data['vol'], 20)
    # 3. 计算 ts_delta(close, 5)
    data_ts_delta = ts_delta(data['close'], 5)
    # 4. 计算 abs(ts_delta(close, 5))
    data_abs_ts_delta = abs(data_ts_delta)
    # 5. 计算 multiply(adv(volume, 20), abs(ts_delta(close, 5)))
    data_multiply = multiply(data_adv, data_abs_ts_delta)
    # 6. 计算 divide(ts_std_dev(close, 10), multiply(adv(volume, 20), abs(ts_delta(close, 5))))
    data_divide = divide(data_ts_std_dev, data_multiply)
    # 7. 计算 ts_rank(divide(ts_std_dev(close, 10), multiply(adv(volume, 20), abs(ts_delta(close, 5)))), 15)
    factor = ts_rank(data_divide, 15)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()