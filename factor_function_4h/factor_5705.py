import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, divide, ts_sum, multiply

def factor_5705(data, **kwargs):
    """
    因子名称: VolumeWeightedPriceChangeSkewness_40878
    数学表达式: ts_skewness(divide(ts_sum(multiply(close, vol), 15), ts_sum(vol, 15)), 7)
    中文描述: 该因子计算过去7天内，基于成交量加权的平均价格（VWAP）的偏度。首先计算过去15天的成交量加权平均价格（VWAP），然后计算该VWAP序列在过去7天内的偏度。偏度衡量了VWAP分布的非对称性。正偏度表明近期VWAP上涨的幅度大于下跌的幅度，可能预示着上涨动能增强；负偏度则相反。相较于简单的VWAP变化，偏度能提供关于价格变动方向和强度的更精细信息，有助于识别潜在的市场情绪变化和趋势的持续性。创新点在于将偏度分析应用于成交量加权平均价格，结合了价格、成交量和统计分布特征，以期捕捉更复杂的市场动态。
    因子应用场景：
    1. 趋势识别：识别价格趋势的潜在变化和市场情绪。
    2. 风险管理：评估价格分布的偏斜程度，辅助风险管理。
    """
    # 1. 计算 multiply(close, vol)
    data_multiply = multiply(data['close'], data['vol'])
    # 2. 计算 ts_sum(multiply(close, vol), 15)
    data_ts_sum_multiply = ts_sum(data_multiply, 15)
    # 3. 计算 ts_sum(vol, 15)
    data_ts_sum_vol = ts_sum(data['vol'], 15)
    # 4. 计算 divide(ts_sum(multiply(close, vol), 15), ts_sum(vol, 15))
    data_divide = divide(data_ts_sum_multiply, data_ts_sum_vol)
    # 5. 计算 ts_skewness(divide(ts_sum(multiply(close, vol), 15), ts_sum(vol, 15)), 7)
    factor = ts_skewness(data_divide, 7)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()