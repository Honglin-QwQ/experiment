import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5922(data, **kwargs):
    """
    因子名称: VolWeightedPriceMomentumSkew_77215
    数学表达式: ts_skewness(ts_returns(divide(close, vwap), 5, mode = 1), 60)
    中文描述: 该因子计算过去60天内收盘价与成交量加权平均价（VWAP）比值的5日算术收益率的偏度。首先，计算收盘价与VWAP的比值，反映当前价格相对于平均交易成本的偏离。然后，计算这个比值的5日收益率，捕捉价格偏离平均成本的短期动量。最后，计算这个短期动量的偏度，以识别价格偏离平均成本的动量分布特征，特别是是否存在极端动量（正偏度表示存在较多正向极端动量，负偏度表示存在较多负向极端动量）。这可以用于衡量市场情绪在短期价格偏离上的极端程度或潜在的价格反转信号。相较于参考因子，该因子引入了收益率的概念，计算的是价格偏离动量的偏度，而非直接价格偏离的偏度，更能捕捉价格变化的动态特征，并根据评估报告的建议，通过计算收益率的偏度来改进因子逻辑，具有创新性。
    因子应用场景：
    1. 衡量市场情绪在短期价格偏离上的极端程度。
    2. 识别潜在的价格反转信号。
    """
    # 1. 计算 divide(close, vwap)
    data_divide = divide(data['close'], data['vwap'])
    # 2. 计算 ts_returns(divide(close, vwap), 5, mode = 1)
    data_ts_returns = ts_returns(data_divide, 5, mode = 1)
    # 3. 计算 ts_skewness(ts_returns(divide(close, vwap), 5, mode = 1), 60)
    factor = ts_skewness(data_ts_returns, 60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()