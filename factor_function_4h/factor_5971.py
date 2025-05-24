import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_returns, ts_entropy

def factor_5971(data, **kwargs):
    """
    因子名称: VWAP_Return_Entropy_Correlation_31977
    数学表达式: ts_corr(ts_returns(vwap, 10), ts_entropy(vwap, 60), 20)
    中文描述: 该因子旨在捕捉成交量加权平均价格（VWAP）短期收益率与VWAP长期信息熵之间的滚动相关性。首先，计算过去10天VWAP的收益率，衡量短期价格变化。
            接着，计算过去60天VWAP的信息熵，衡量长期价格分布的复杂性和不确定性。最后，在过去20天的时间窗口内计算这两者之间的相关性。
            较高的正相关可能表明短期价格上涨伴随着长期市场不确定性的增加，而较高的负相关可能表明短期价格下跌伴随着长期市场不确定性的降低。
            这个因子结合了价格变化和市场不确定性两个维度，可以用于识别市场情绪的变化和潜在的趋势反转。
            相较于参考因子，本因子引入了收益率和信息熵的概念，并通过计算它们之间的相关性来捕捉更复杂的市场动态，提供了对市场状态更全面的视角。
            改进方向上，我们采纳了结合其他因子的建议，将短期收益率与长期信息熵进行关联，并使用了ts_corr操作符来衡量这种关联性。
    因子应用场景：
    1. 市场情绪分析：通过观察短期收益率与长期信息熵之间的相关性，可以判断市场情绪是趋于稳定还是动荡。
    2. 趋势反转识别：当相关性出现显著变化时，可能预示着市场趋势即将发生反转。
    3. 风险管理：该因子可以帮助识别市场不确定性增加的时期，从而进行风险管理。
    """
    # 1. 计算 ts_returns(vwap, 10)
    data_ts_returns_vwap = ts_returns(data['vwap'], 10)
    # 2. 计算 ts_entropy(vwap, 60)
    data_ts_entropy_vwap = ts_entropy(data['vwap'], 60)
    # 3. 计算 ts_corr(ts_returns(vwap, 10), ts_entropy(vwap, 60), 20)
    factor = ts_corr(data_ts_returns_vwap, data_ts_entropy_vwap, 20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()