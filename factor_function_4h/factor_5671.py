import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import log, divide, ts_delay, ts_std_dev

def factor_5671(data, **kwargs):
    """
    因子名称: factor_0001_13971
    数学表达式: ts_std_dev(log(divide(close, ts_delay(close, 5))), 5)
    中文描述: 该因子计算过去5天收盘价对数收益率的标准差，衡量短期价格波动率。相比于直接使用收益率计算标准差，该因子首先对收盘价进行对数变换，然后计算过去5天的对数收益率，最后计算这些对数收益率的标准差。这种处理方式可以更好地反映价格的相对变化，并减少极端值的影响。创新点在于将对数收益率和波动率结合，能更准确地捕捉市场波动。
    因子应用场景：
    1. 波动率衡量：该因子可用于衡量股票的短期价格波动率，数值越高表示波动越大。
    2. 风险管理：可用于风险管理，识别高风险股票。
    3. 趋势跟踪：结合趋势指标，可用于识别趋势中的波动机会。
    """
    # 1. 计算 ts_delay(close, 5)
    data_ts_delay_close = ts_delay(data['close'], 5)
    # 2. 计算 divide(close, ts_delay(close, 5))
    data_divide = divide(data['close'], data_ts_delay_close)
    # 3. 计算 log(divide(close, ts_delay(close, 5)))
    data_log = log(data_divide)
    # 4. 计算 ts_std_dev(log(divide(close, ts_delay(close, 5))), 5)
    factor = ts_std_dev(data_log, 5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()