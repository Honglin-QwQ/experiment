import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_zscore, ts_std_dev
import pandas as pd

def factor_5842(data, **kwargs):
    """
    因子名称: VolatilityAdjustedVolumeFlow_72562
    数学表达式: divide(ts_zscore(tbase, 20), ts_std_dev(amount, 60))
    中文描述: 该因子旨在衡量主动买入量相对于交易额波动性的标准化强度。它首先计算过去20天主动买入基础币种数量（tbase）的Z分数，以衡量主动买入的相对强弱和异常程度。
            然后，将这个Z分数除以过去60天交易额（amount）的标准差，对主动买入的强度进行波动率调整。高因子值可能表明在相对稳定的交易额波动下出现了异常强劲的主动买入，可能预示着价格上涨动能。
            这结合了参考因子ts_zscore(high,19)对异常波动的捕捉和ts_std_dev(returns, 66)对波动性的衡量，并引入了新的数据元素tbase和amount以及divide操作符，具有创新性。
            适用于捕捉在低波动环境下由主动买入驱动的价格上涨机会。
    因子应用场景：
    1. 识别主动买入驱动的价格上涨机会：当因子值较高时，可能表明在相对稳定的交易额波动下出现了异常强劲的主动买入，可能预示着价格上涨动能。
    2. 波动率调整：通过将主动买入的Z分数除以交易额的标准差，可以对主动买入的强度进行波动率调整，从而更好地衡量主动买入的相对强度。
    """
    # 1. 计算 ts_zscore(tbase, 20)
    tbase_zscore = ts_zscore(data['tbase'], d = 20)
    # 2. 计算 ts_std_dev(amount, 60)
    amount_std = ts_std_dev(data['amount'], d = 60)
    # 3. 计算 divide(ts_zscore(tbase, 20), ts_std_dev(amount, 60))
    factor = divide(tbase_zscore, amount_std)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()