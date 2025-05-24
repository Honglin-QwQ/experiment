import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_co_skewness, multiply

def factor_5784(data, **kwargs):
    """
    因子名称: Volume_Price_Interaction_Skewness_74555
    数学表达式: ts_co_skewness(multiply(vol, close), close, 10)
    中文描述: 该因子计算过去10天内成交量加权收盘价与收盘价之间的协偏度。协偏度衡量了两个变量共同偏离其均值的程度和方向。正的协偏度表示当收盘价偏离均值时，成交量加权收盘价倾向于同方向偏离，且偏离程度更大；负的协偏度则表示反向偏离。这个因子旨在捕捉成交量与价格之间的非线性关系，尤其是在极端价格波动时的表现。相较于简单的相关性或标准差比率，协偏度更能反映成交量在价格偏离均值时的不对称影响，可能用于识别由成交量驱动的非对称价格风险或机会。
    因子应用场景：
    1. 识别成交量与价格之间的非线性关系。
    2. 捕捉极端价格波动时成交量的影响。
    3. 用于识别由成交量驱动的非对称价格风险或机会。
    """
    # 1. 计算 multiply(vol, close)
    data_multiply = multiply(data['vol'], data['close'])
    # 2. 计算 ts_co_skewness(multiply(vol, close), close, 10)
    factor = ts_co_skewness(data_multiply, data['close'], 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()