import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_entropy, divide, ts_std_dev, adv

def factor_5617(data, **kwargs):
    """
    因子名称: factor_price_volatility_entropy_73376
    数学表达式: ts_entropy(divide(ts_std_dev(close, 10), adv(vol, 10)), 20)
    中文描述: 该因子计算过去20天内，收盘价的10日标准差与10日平均成交量的比率的信息熵。这个比率可以理解为价格波动相对于成交量的波动程度，即单位成交量所对应的价格波动大小。信息熵则用于衡量这个比率在一段时间内的不确定性和复杂性。当市场在较低交易量下出现剧烈价格波动时，该因子值可能较高，表明市场情绪不稳定；反之，当市场交易活跃且价格波动平稳时，该因子值可能较低，表明市场情绪相对稳定。该因子结合了价格波动、成交量和信息熵，从量价关系的角度分析市场情绪和潜在风险。创新点在于将波动率和成交量的比率作为信息熵的输入，从而捕捉市场微观结构的变化。
    因子应用场景：
    1. 市场情绪分析： 通过观察因子值的变化，可以评估市场情绪的稳定程度，辅助判断市场风险。
    2. 量价关系研究： 用于研究价格波动与成交量之间的关系，揭示市场微观结构的变化。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev_close = ts_std_dev(data['close'], 10)
    # 2. 计算 adv(vol, 10)
    data_adv_vol = adv(data['vol'], 10)
    # 3. 计算 divide(ts_std_dev(close, 10), adv(vol, 10))
    data_divide = divide(data_ts_std_dev_close, data_adv_vol)
    # 4. 计算 ts_entropy(divide(ts_std_dev(close, 10), adv(vol, 10)), 20)
    factor = ts_entropy(data_divide, 20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()