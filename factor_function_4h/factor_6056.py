import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_entropy, divide, adv, multiply

def factor_6056(data, **kwargs):
    """
    因子名称: Volume_Weighted_Volatility_Entropy_96227
    数学表达式: multiply(ts_std_dev(close, 60), ts_entropy(divide(vol, adv(vol, 60)), 60))
    中文描述: 该因子旨在捕捉成交量加权的价格波动中的信息熵。它通过计算过去60天收盘价的标准差（衡量价格波动），并将其与过去60天内每日成交量相对于60天平均成交量的比值的熵（衡量成交量分布的混乱程度或信息含量）相乘得到。高因子值可能表明在价格波动较大的同时，成交量的分布也呈现出较高的不确定性或信息含量，这可能预示着潜在的市场异动或趋势反转。相较于简单的收益率或成交量变化，该因子结合了价格波动和成交量分布的复杂信息，具有创新性。
    因子应用场景：
    1. 市场异动预警：当因子值异常升高时，可能预示着市场即将发生异动或趋势反转。
    2. 成交量分布分析：该因子可以帮助分析成交量分布的混乱程度或信息含量，从而更好地理解市场参与者的交易行为。
    3. 波动率研究：该因子结合了价格波动和成交量分布的信息，可以用于更深入地研究市场波动率的特征。
    """
    # 1. 计算 adv(vol, 60)
    data_adv_vol = adv(data['vol'], d = 60)
    # 2. 计算 divide(vol, adv(vol, 60))
    data_divide = divide(data['vol'], data_adv_vol)
    # 3. 计算 ts_entropy(divide(vol, adv(vol, 60)), 60)
    data_ts_entropy = ts_entropy(data_divide, d = 60)
    # 4. 计算 ts_std_dev(close, 60)
    data_ts_std_dev = ts_std_dev(data['close'], d = 60)
    # 5. 计算 multiply(ts_std_dev(close, 60), ts_entropy(divide(vol, adv(vol, 60)), 60))
    factor = multiply(data_ts_std_dev, data_ts_entropy)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()