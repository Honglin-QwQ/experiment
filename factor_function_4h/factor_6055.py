import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_entropy, divide, ts_std_dev, ts_decay_exp_window, adv

def factor_6055(data, **kwargs):
    """
    因子名称: VWAP_Volume_Volatility_Entropy_56768
    数学表达式: ts_entropy(divide(ts_std_dev(vwap, 73), ts_decay_exp_window(adv(vol, 20), 11, 0.5)), 6)
    中文描述: 该因子结合了VWAP的波动性、成交量的指数衰减平均以及信息熵的概念。首先，计算过去73天VWAP的标准差，代表VWAP的波动性。然后，计算过去20天平均成交量在过去11天的指数衰减加权平均值，代表近期成交量的趋势和强度。将VWAP波动性除以指数衰减平均成交量，得到一个波动性与成交量相对强度的度量。最后，计算这个相对强度的度量在过去6天内的信息熵。信息熵衡量了该度量在近期内的不确定性和随机性。高熵可能表示市场情绪不稳定或趋势不明朗，低熵可能表示市场情绪相对稳定或趋势清晰。创新点在于结合了波动性、成交量趋势和信息熵，从多个维度捕捉市场特征，并使用指数衰减平均对成交量进行加权，更关注近期数据的影响。
    因子应用场景：
    1. 市场情绪分析：通过信息熵判断市场情绪的稳定程度。
    2. 趋势识别：结合成交量和波动性，辅助判断趋势的强度和持续性。
    3. 风险管理：识别市场不确定性较高的时期，辅助风险管理决策。
    """
    # 1. 计算 ts_std_dev(vwap, 73)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 73)
    # 2. 计算 adv(vol, 20)
    data_adv_vol = adv(data['vol'], 20)
    # 3. 计算 ts_decay_exp_window(adv(vol, 20), 11, 0.5)
    data_ts_decay_exp_window_adv_vol = ts_decay_exp_window(data_adv_vol, 11, 0.5)
    # 4. 计算 divide(ts_std_dev(vwap, 73), ts_decay_exp_window(adv(vol, 20), 11, 0.5))
    data_divide = divide(data_ts_std_dev_vwap, data_ts_decay_exp_window_adv_vol)
    # 5. 计算 ts_entropy(divide(ts_std_dev(vwap, 73), ts_decay_exp_window(adv(vol, 20), 11, 0.5)), 6)
    factor = ts_entropy(data_divide, 6)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()