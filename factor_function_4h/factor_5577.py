import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_scale, ts_covariance, ts_rank, ts_delta, signed_power, log

def factor_5577(data, **kwargs):
    """
    因子名称: factor_0008_14511
    数学表达式: ts_scale(ts_covariance(ts_rank(close, d=5), ts_delta(signed_power(high,2), d=2), d=10), d=20, constant=1)*log(volume)
    中文描述: 该因子在factor_0007的基础上，对最高价(high)进行了平方处理(signed_power(high,2))，并对成交量(volume)取对数(log(volume))。平方处理增强了最高价的影响，使得因子对价格的敏感度更高。对成交量取对数，降低了成交量极端值的影响，使因子更加稳健。整体而言，该因子旨在捕捉价格高点变化与收盘价排名的协方差关系，并结合成交量的影响，从而识别潜在的市场动量变化。创新点在于对价格和成交量分别进行非线性变换，增强了因子的非线性表达能力。
    因子应用场景：
    1. 动量捕捉：捕捉价格高点变化与收盘价排名的协方差关系，识别潜在的市场动量变化。
    2. 稳健性增强：对成交量取对数，降低了成交量极端值的影响，使因子更加稳健。
    """
    # 1. 计算 ts_rank(close, d=5)
    data_ts_rank_close = ts_rank(data['close'], d=5)
    # 2. 计算 signed_power(high,2)
    data_signed_power_high = signed_power(data['high'], 2)
    # 3. 计算 ts_delta(signed_power(high,2), d=2)
    data_ts_delta_signed_power_high = ts_delta(data_signed_power_high, d=2)
    # 4. 计算 ts_covariance(ts_rank(close, d=5), ts_delta(signed_power(high,2), d=2), d=10)
    data_ts_covariance = ts_covariance(data_ts_rank_close, data_ts_delta_signed_power_high, d=10)
    # 5. 计算 ts_scale(ts_covariance(ts_rank(close, d=5), ts_delta(signed_power(high,2), d=2), d=10), d=20, constant=1)
    data_ts_scale = ts_scale(data_ts_covariance, d=20, constant=1)
    # 6. 计算 log(volume)
    data_log_volume = log(data['vol'])
    # 7. 计算 ts_scale(ts_covariance(ts_rank(close, d=5), ts_delta(signed_power(high,2), d=2), d=10), d=20, constant=1)*log(volume)
    factor = data_ts_scale * data_log_volume

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()