import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_mean, divide

def factor_6041(data, **kwargs):
    """
    因子名称: LowPriceVolatilityRatio_58090
    数学表达式: divide(ts_std_dev(low, 60), ts_mean(low, 60))
    中文描述: 该因子计算过去60天最低价的标准差与过去60天最低价均值的比值。它衡量了最低价格在近期内的相对波动性。高值可能表示最低价格波动剧烈，低值表示最低价格相对稳定。该因子结合了参考因子中对最低价的关注和对时间序列标准差的应用，创新点在于通过比值来衡量相对波动性，而非绝对波动性或Z得分。这可以用于识别在特定时期内最低价表现出异常波动或异常稳定的股票。
    因子应用场景：
    1. 波动性分析：用于识别最低价波动较大的股票，可能存在较高的投资风险。
    2. 稳定性分析：用于识别最低价波动较小的股票，可能适合稳健型投资者。
    """
    # 1. 计算 ts_std_dev(low, 60)
    data_ts_std_dev = ts_std_dev(data['low'], 60)
    # 2. 计算 ts_mean(low, 60)
    data_ts_mean = ts_mean(data['low'], 60)
    # 3. 计算 divide(ts_std_dev(low, 60), ts_mean(low, 60))
    factor = divide(data_ts_std_dev, data_ts_mean)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()