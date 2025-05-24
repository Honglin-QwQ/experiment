import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import abs, ts_returns, ts_std_dev, divide

def factor_5819(data, **kwargs):
    """
    因子名称: Vol_StdDev_Returns_Ratio_Adjusted_97722
    数学表达式: divide(abs(ts_returns(vol, 10)), ts_std_dev(vol, 60))
    中文描述: 该因子计算了交易量的短期变化率（过去10天的收益率）的绝对值与中期交易量波动性（过去60天的标准差）之比。相较于原因子，我们将收益率窗口缩短至10天以捕捉更近期的动量，并将波动率窗口缩短至60天以反映中期波动特征。同时，我们将短期变化率放在分子，长期波动性放在分母，并对短期变化率取绝对值，以应对原因子IC为负的问题，并突出短期交易量变化的强度相对于中期波动的程度。高值可能表明近期交易量变化剧烈，而中期波动相对平缓，预示着潜在的市场情绪变化或交易机会。
    因子应用场景：
    1. 交易量变化分析：用于衡量交易量近期变化的剧烈程度相对于中期波动水平。
    2. 市场情绪捕捉：高值可能预示着市场情绪的变化或潜在的交易机会。
    """
    # 1. 计算 ts_returns(vol, 10)
    data_ts_returns = ts_returns(data['vol'], 10)
    # 2. 计算 abs(ts_returns(vol, 10))
    data_abs_ts_returns = abs(data_ts_returns)
    # 3. 计算 ts_std_dev(vol, 60)
    data_ts_std_dev = ts_std_dev(data['vol'], 60)
    # 4. 计算 divide(abs(ts_returns(vol, 10)), ts_std_dev(vol, 60))
    factor = divide(data_abs_ts_returns, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()