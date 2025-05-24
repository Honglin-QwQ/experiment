import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_delta, ts_mean, multiply

def factor_5757(data, **kwargs):
    """
    因子名称: VolumeWeightedLowPriceMomentumRatio_50361
    数学表达式: divide(ts_delta(low, 20), ts_mean(multiply(low, vol), 41))
    中文描述: 该因子计算过去20天最低价格的变化量与过去41天成交量加权最低价格的平均值之比。它旨在捕捉短期价格动量与长期成交量加权价格水平之间的关系。相较于参考因子，该因子在分子中使用了最低价格的短期变化量来衡量动量，并在分母中引入了成交量加权最低价格的平均值，以更全面地反映市场对价格的认可程度。较高的因子值可能表明短期内最低价格出现显著上涨，且这种上涨发生在长期成交量加权价格水平相对较低的情况下，可能预示着潜在的买入机会。改进之处在于结合了价格动量和成交量加权价格信息，提供了更丰富的市场信号，并使用了divide和multiply操作符来计算比率和加权平均。
    因子应用场景：
    1. 短期价格动量：用于识别短期内最低价格快速上涨的股票。
    2. 市场认可度评估：结合成交量加权价格，评估市场对当前价格水平的认可程度。
    3. 买入机会识别：较高的因子值可能预示着潜在的买入机会。
    """
    # 1. 计算 ts_delta(low, 20)
    data_ts_delta_low = ts_delta(data['low'], d=20)
    # 2. 计算 multiply(low, vol)
    data_multiply_low_vol = multiply(data['low'], data['vol'])
    # 3. 计算 ts_mean(multiply(low, vol), 41)
    data_ts_mean_multiply_low_vol = ts_mean(data_multiply_low_vol, d=41)
    # 4. 计算 divide(ts_delta(low, 20), ts_mean(multiply(low, vol), 41))
    factor = divide(data_ts_delta_low, data_ts_mean_multiply_low_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()