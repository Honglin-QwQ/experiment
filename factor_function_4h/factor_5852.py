import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_mean, divide
import pandas as pd

def factor_5852(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Ratio_97365
    数学表达式: divide(ts_std_dev(vwap, 117), ts_mean(vwap, 117))
    中文描述: 该因子计算过去117天VWAP（成交量加权平均价格）的标准差与均值的比值。标准差衡量VWAP在时间序列上的波动性，而均值代表了平均交易成本。通过计算这个比率，因子量化了VWAP相对于其平均水平的波动程度。高比值可能表明该股票在过去一段时间内VWAP波动剧烈，市场交易成本差异较大，可能预示着不确定性或趋势的形成。低比值则表示VWAP相对稳定，市场交易成本差异较小。这个因子可以用于捕捉股票价格波动的相对强度，作为衡量风险或趋势稳定性的指标。相较于简单的VWAP中位数或均值，该因子更关注价格的波动特性，提供了更深层次的市场洞察。
    因子应用场景：
    1. 波动性评估：用于评估股票价格的波动程度，高比率可能意味着高波动性。
    2. 风险管理：作为风险指标，帮助识别潜在的高风险股票。
    3. 趋势识别：辅助识别市场趋势，高波动性可能预示着趋势的形成或转变。
    """
    # 1. 计算 ts_std_dev(vwap, 117)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], d = 117)
    # 2. 计算 ts_mean(vwap, 117)
    data_ts_mean_vwap = ts_mean(data['vwap'], d = 117)
    # 3. 计算 divide(ts_std_dev(vwap, 117), ts_mean(vwap, 117))
    factor = divide(data_ts_std_dev_vwap, data_ts_mean_vwap)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()