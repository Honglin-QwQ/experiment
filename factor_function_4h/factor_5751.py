import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, add, abs, ts_corr, ts_decay_linear, adv, divide
import pandas as pd

def factor_5751(data, **kwargs):
    """
    因子名称: VolatilityTrendVolumeMomentumRatio_21541
    数学表达式: divide(ts_std_dev(vwap, 20), add(abs(ts_corr(close, open, 20)), ts_decay_linear(adv(vol, 30), 20), 0.001))
    中文描述: 该因子旨在捕捉市场波动性、日内价格趋势强度和成交量动量之间的复杂关系。它通过计算过去20天vwap的标准差来衡量价格波动性，并将其除以收盘价与开盘价在过去20天相关性的绝对值与过去30天平均成交量在过去20天线性衰减加权平均值之和（分母加上一个小的常数防止除零）。高标准差可能表明市场波动较大，而价格相关性和线性衰减加权平均成交量则反映了趋势的强度和市场参与度的动态变化。通过将波动性与价格相关性和成交量动量结合，该因子试图识别在波动性较高但有一定动态趋势和成交量支持的市场环境下的交易机会。相较于参考因子，该因子在波动性衡量上从信息熵替换为更稳定的标准差，在成交量衡量上引入了线性衰减加权平均来捕捉成交量的近期动量，并且调整了窗口期参数以寻求更好的预测能力和稳定性。同时在分母中加入了绝对值和常数以增强因子的稳定性和鲁棒性。
    因子应用场景：
    1. 波动性分析：用于识别市场波动较大的股票。
    2. 趋势强度判断：结合价格相关性和成交量动量，判断趋势的强弱。
    3. 市场参与度评估：通过成交量变化，评估市场参与程度。
    """
    # 1. 计算 ts_std_dev(vwap, 20)
    data_ts_std_dev = ts_std_dev(data['vwap'], 20)
    # 2. 计算 abs(ts_corr(close, open, 20))
    data_ts_corr = abs(ts_corr(data['close'], data['open'], 20))
    # 3. 计算 adv(vol, 30)
    data_adv = adv(data['vol'], 30)
    # 4. 计算 ts_decay_linear(adv(vol, 30), 20)
    data_ts_decay_linear = ts_decay_linear(data_adv, 20)
    # 5. 计算 add(abs(ts_corr(close, open, 20)), ts_decay_linear(adv(vol, 30), 20), 0.001)
    data_add = add(data_ts_corr, data_ts_decay_linear, 0.001)
    # 6. 计算 divide(ts_std_dev(vwap, 20), add(abs(ts_corr(close, open, 20)), ts_decay_linear(adv(vol, 30), 20), 0.001))
    factor = divide(data_ts_std_dev, data_add)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()