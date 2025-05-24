import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import abs, ts_skewness, ts_delta, ts_std_dev, ts_rank, multiply

def factor_5980(data, **kwargs):
    """
    因子名称: Volatility_Skew_Momentum_Enhanced_21161
    数学表达式: multiply(abs(ts_skewness(ts_delta(low, 3), 66)), ts_std_dev(ts_delta(open, 3), 66), ts_rank(ts_delta(close, 1), 20))
    中文描述: 该因子是对原有Volatility_Skew_Momentum因子的增强版本，旨在提升其预测能力和稳定性。它计算了过去66天内最低价3日变化量的绝对偏度，与过去66天开盘价3日变化量的标准差的乘积，再乘以过去20天收盘价1日变化量的排名。通过使用绝对偏度，避免了正负偏度相互抵消的影响；引入短期收盘价变化量的排名，进一步捕捉了价格的相对动量。该因子期望在波动性较高且存在明显偏度的市场环境下，同时表现出相对较强的短期上涨动量的股票具有更好的表现。
    因子应用场景：
    1. 波动性与偏度分析：适用于识别市场波动性较高且存在明显偏度的股票。
    2. 短期动量捕捉：能够捕捉短期价格上涨动量较强的股票。
    3. 增强因子稳定性：通过绝对偏度和排名，增强了因子的预测能力和稳定性。
    """
    # 1. 计算 ts_delta(low, 3)
    data_ts_delta_low = ts_delta(data['low'], 3)
    # 2. 计算 ts_skewness(ts_delta(low, 3), 66)
    data_ts_skewness = ts_skewness(data_ts_delta_low, 66)
    # 3. 计算 abs(ts_skewness(ts_delta(low, 3), 66))
    data_abs_ts_skewness = abs(data_ts_skewness)
    # 4. 计算 ts_delta(open, 3)
    data_ts_delta_open = ts_delta(data['open'], 3)
    # 5. 计算 ts_std_dev(ts_delta(open, 3), 66)
    data_ts_std_dev = ts_std_dev(data_ts_delta_open, 66)
    # 6. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 7. 计算 ts_rank(ts_delta(close, 1), 20)
    data_ts_rank = ts_rank(data_ts_delta_close, 20)
    # 8. 计算 multiply(abs(ts_skewness(ts_delta(low, 3), 66)), ts_std_dev(ts_delta(open, 3), 66), ts_rank(ts_delta(close, 1), 20))
    factor = multiply(data_abs_ts_skewness, data_ts_std_dev, data_ts_rank, filter=False)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()