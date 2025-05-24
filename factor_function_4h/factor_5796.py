import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, subtract, ts_min, adv

def factor_5796(data, **kwargs):
    """
    数学表达式: divide(subtract(open, ts_min(low, 20)), adv(vol, 20))
    中文描述: 该因子计算开盘价与过去20天最低价的差值，并用过去20天平均成交量进行标准化。它试图捕捉开盘价相对于近期低点的强势程度，并考虑成交量的放大效应。当开盘价远高于近期低点且成交量较大时，因子值较高，可能预示着上涨趋势。这结合了对近期价格趋势的关注和成交量验证。创新点在于将开盘价与近期最低价的相对位置与成交量动态结合，构建一个反映短期市场情绪和动能的指标。
    因子应用场景：
    1. 短期趋势判断：因子值较高可能预示着短期上涨趋势，可以用于识别潜在的买入机会。
    2. 成交量验证：结合成交量信息，验证价格上涨的可靠性。
    3. 市场情绪分析：反映市场对股票的乐观程度，因子值越高表示市场情绪越积极。
    """
    # 1. 计算 ts_min(low, 20)
    data_ts_min = ts_min(data['low'], 20)
    # 2. 计算 subtract(open, ts_min(low, 20))
    data_subtract = subtract(data['open'], data_ts_min)
    # 3. 计算 adv(vol, 20)
    data_adv = adv(data['vol'], 20)
    # 4. 计算 divide(subtract(open, ts_min(low, 20)), adv(vol, 20))
    factor = divide(data_subtract, data_adv)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()