import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_entropy, add, abs, ts_corr, ts_mean, adv, divide

def factor_5728(data, **kwargs):
    """
    因子名称: EntropyCorrVolumeRatio_25558
    数学表达式: divide(ts_entropy(vwap, 15), add(abs(ts_corr(close, open, 15)), ts_mean(adv(vol, 25), 15), 0.001))
    中文描述: 该因子旨在捕捉市场的不确定性、价格相关性和交易量之间的复杂关系。它通过计算过去15天vwap的信息熵来衡量市场的不确定性，并将其除以收盘价与开盘价在过去15天相关性的绝对值与过去25天平均成交量在过去15天的均值之和（分母加上一个小的常数防止除零）。高熵值可能表明市场情绪不稳定，而价格相关性和平均成交量则反映了趋势的强度和市场参与度。通过将熵值与价格相关性和交易量结合，该因子试图识别在不确定性较高但有一定趋势和成交量支持的市场环境下的交易机会。相较于参考因子，该因子在结构上进行了创新，通过除法运算将熵值与价格相关性和交易量进行比值计算，并且引入了更长期的平均成交量（25天）来平滑交易量数据，同时在分母中加入了绝对值和常数以增强因子的稳定性和鲁棒性。
    因子应用场景：
    1. 市场不确定性评估：用于评估市场的不确定性水平，高因子值可能表示市场情绪不稳定。
    2. 趋势强度验证：结合价格相关性和交易量，验证市场趋势的强度。
    3. 交易机会识别：识别在不确定性较高但有一定趋势和成交量支持的市场环境下的交易机会。
    """
    # 1. 计算 ts_entropy(vwap, 15)
    data_ts_entropy = ts_entropy(data['vwap'], d = 15)
    # 2. 计算 abs(ts_corr(close, open, 15))
    data_ts_corr = abs(ts_corr(data['close'], data['open'], d = 15))
    # 3. 计算 adv(vol, 25)
    data_adv = adv(data['vol'], d = 25)
    # 4. 计算 ts_mean(adv(vol, 25), 15)
    data_ts_mean = ts_mean(data_adv, d = 15)
    # 5. 计算 add(abs(ts_corr(close, open, 15)), ts_mean(adv(vol, 25), 15), 0.001)
    data_add = add(data_ts_corr, data_ts_mean, 0.001)
    # 6. 计算 divide(ts_entropy(vwap, 15), add(abs(ts_corr(close, open, 15)), ts_mean(adv(vol, 25), 15), 0.001))
    factor = divide(data_ts_entropy, data_add)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()