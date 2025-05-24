import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_entropy, scale, divide, multiply

def factor_5827(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Entropy_Ratio_Scaled_24062
    数学表达式: divide(ts_std_dev(vwap, 30), multiply(ts_entropy(vwap, 45), scale(vwap)))
    中文描述: 该因子计算过去30天VWAP的标准差与过去45天VWAP信息熵和当前VWAP缩放值的乘积的比值。标准差衡量VWAP的波动性，信息熵衡量VWAP分布的复杂性或不确定性，而缩放后的VWAP则考虑了当前价格的量纲影响。该因子旨在捕捉VWAP的近期波动性相对于其不确定性和当前价格水平的程度。创新点在于将标准差、信息熵和缩放后的VWAP进行组合，形成一个新的多维度指标，并且调整了时间窗口以更好地捕捉短期市场特征。通过引入缩放后的VWAP，该因子更能反映波动性和不确定性在当前价格水平下的相对意义，可能更好地识别潜在的市场机会或风险。此外，调整了信息熵和标准差的时间窗口，以探索不同的市场周期影响。
    因子应用场景：
    1. 波动性分析：用于衡量VWAP的波动性相对于其不确定性和价格水平的程度。
    2. 市场机会识别：可能用于识别潜在的市场机会或风险。
    3. 多维度指标：将标准差、信息熵和缩放后的VWAP进行组合，形成一个新的多维度指标。
    """
    # 1. 计算 ts_std_dev(vwap, 30)
    data_ts_std_dev = ts_std_dev(data['vwap'], d=30)
    # 2. 计算 ts_entropy(vwap, 45)
    data_ts_entropy = ts_entropy(data['vwap'], d=45)
    # 3. 计算 scale(vwap)
    data_scale = scale(data['vwap'])
    # 4. 计算 multiply(ts_entropy(vwap, 45), scale(vwap))
    data_multiply = multiply(data_ts_entropy, data_scale)
    # 5. 计算 divide(ts_std_dev(vwap, 30), multiply(ts_entropy(vwap, 45), scale(vwap)))
    factor = divide(data_ts_std_dev, data_multiply)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()