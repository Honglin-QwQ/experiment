import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_delta, divide, adv, ts_rank

def factor_6101(data, **kwargs):
    """
    数学表达式: ts_skewness(ts_delta(divide(close, vwap), 5), 20) * ts_rank(divide(adv(vol, 10), adv(vol, 50)), 30)
    中文描述: 该因子结合了收盘价与VWAP比值的短期变化偏度以及短期相对长期成交量的排名。首先，计算收盘价与VWAP比值在过去5天内的变化（ts_delta），然后计算这些变化在过去20天内的偏度（ts_skewness），捕捉价格相对于VWAP偏离变化分布的不对称性。接着，计算过去10天平均成交量与过去50天平均成交量的比值，衡量短期成交量相对于长期成交量的强度。最后，计算这个成交量比值在过去30天内的排名（ts_rank）。整个因子是偏度与成交量相对强度排名的乘积。相较于参考因子，该因子创新性地关注了收盘价与VWAP比值的'变化'的偏度，而不是直接的偏度，这可能更能捕捉动量信息。同时，使用了短期相对长期成交量的比值排名，引入了成交量结构的变化信息。根据历史评估结果，该因子尝试通过结合价格偏离变化的分布特征和成交量结构的相对强度来提高预测能力和稳定性，并调整了时间窗口参数，以期捕捉更有效的市场信号。使用了ts_skewness, ts_delta, divide, adv, ts_rank等运算符，增加了因子的复杂度和信息含量。
    因子应用场景：
    1. 动量捕捉：捕捉价格相对于VWAP偏离变化分布的不对称性，可能更能捕捉动量信息。
    2. 成交量结构变化：引入短期相对长期成交量的比值排名，反映成交量结构的变化信息。
    3. 预测能力和稳定性：结合价格偏离变化的分布特征和成交量结构的相对强度来提高预测能力和稳定性。
    """
    # 1. 计算 divide(close, vwap)
    data_divide_close_vwap = divide(data['close'], data['vwap'])
    # 2. 计算 ts_delta(divide(close, vwap), 5)
    data_ts_delta = ts_delta(data_divide_close_vwap, 5)
    # 3. 计算 ts_skewness(ts_delta(divide(close, vwap), 5), 20)
    data_ts_skewness = ts_skewness(data_ts_delta, 20)
    # 4. 计算 adv(vol, 10)
    data_adv_10 = adv(data['vol'], 10)
    # 5. 计算 adv(vol, 50)
    data_adv_50 = adv(data['vol'], 50)
    # 6. 计算 divide(adv(vol, 10), adv(vol, 50))
    data_divide_adv = divide(data_adv_10, data_adv_50)
    # 7. 计算 ts_rank(divide(adv(vol, 10), adv(vol, 50)), 30)
    data_ts_rank = ts_rank(data_divide_adv, 30)
    # 8. 计算 ts_skewness(ts_delta(divide(close, vwap), 5), 20) * ts_rank(divide(adv(vol, 10), adv(vol, 50)), 30)
    factor = data_ts_skewness * data_ts_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()