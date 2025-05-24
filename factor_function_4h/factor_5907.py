import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, divide

def factor_5907(data, **kwargs):
    """
    因子名称: VolWeightedPriceVolatilitySkew_80310
    数学表达式: ts_skewness(divide(close, vwap), 60)
    中文描述: 该因子计算过去60天内收盘价与成交量加权平均价（VWAP）比值的偏度。VWAP反映了市场平均交易成本，收盘价与VWAP的比值则可以衡量当前价格相对于平均成本的偏离程度。计算这个比值的偏度，可以捕捉价格偏离平均成本的分布特征，特别是是否存在极端偏离（正偏度表示存在较多正向极端偏离，负偏度表示存在较多负向极端偏离）。这可以用于识别价格波动的不对称性，例如在上涨行情中收盘价持续高于VWAP，而在下跌行情中收盘价持续低于VWAP，或者存在突然的大幅上涨或下跌。相较于参考因子，该因子结合了VWAP和收盘价，并利用偏度来捕捉价格相对于平均成本的波动特征，具有创新性。可以用于衡量市场情绪的极端程度或潜在的价格反转信号。
    因子应用场景：
    1. 衡量市场情绪的极端程度
    2. 潜在的价格反转信号识别
    3. 识别价格波动的不对称性
    """
    # 1. 计算 divide(close, vwap)
    data_divide = divide(data['close'], data['vwap'])
    # 2. 计算 ts_skewness(divide(close, vwap), 60)
    factor = ts_skewness(data_divide, d = 60)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()