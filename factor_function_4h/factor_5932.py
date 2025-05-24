import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import scale, rank, divide, ts_delta

def factor_5932(data, **kwargs):
    """
    因子名称: vwap_delta_relative_strength_rank_scaled_27803
    数学表达式: scale(rank(divide(ts_delta(vwap, 7), ts_delta(vwap, 20))), 1)
    中文描述: 该因子首先计算VWAP在短期（7天）和中期（20天）内的变化。然后，计算短期变化与中期变化的比例，衡量短期动量相对于长期动量强弱。接着，计算该比例在截面上的排名。最后，对排名结果进行标准化。这个因子旨在捕捉短期VWAP变化率相对于中期变化率的相对强度，并识别那些短期动量显著强于中期动量的股票。通过结合不同时间周期的VWAP变化和截面排名，可以识别具有潜在持续动量的股票。标准化处理有助于因子在不同股票和时间点上的可比性。这可能用于识别处于加速趋势中的股票。
    因子应用场景：
    1. 动量分析：识别短期动量相对于长期动量较强的股票。
    2. 趋势识别：用于识别处于加速趋势中的股票。
    3. 相对强度：衡量股票短期表现相对于长期表现的强度。
    """
    # 1. 计算 ts_delta(vwap, 7)
    data_ts_delta_vwap_7 = ts_delta(data['vwap'], 7)
    # 2. 计算 ts_delta(vwap, 20)
    data_ts_delta_vwap_20 = ts_delta(data['vwap'], 20)
    # 3. 计算 divide(ts_delta(vwap, 7), ts_delta(vwap, 20))
    data_divide = divide(data_ts_delta_vwap_7, data_ts_delta_vwap_20)
    # 4. 计算 rank(divide(ts_delta(vwap, 7), ts_delta(vwap, 20)))
    data_rank = rank(data_divide, 2)
    # 5. 计算 scale(rank(divide(ts_delta(vwap, 7), ts_delta(vwap, 20))), 1)
    factor = scale(data_rank, 1)

    # 删除中间变量
    del data_ts_delta_vwap_7
    del data_ts_delta_vwap_20
    del data_divide
    del data_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()