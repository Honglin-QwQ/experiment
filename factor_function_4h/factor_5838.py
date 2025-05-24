import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import divide, ts_std_dev, multiply

def factor_5838(data, **kwargs):
    """
    因子名称: Volume_Price_Volatility_Ratio_96104
    数学表达式: divide(ts_std_dev(multiply(vol, close), 60), ts_std_dev(divide(close, vol), 60))
    中文描述: 该因子旨在衡量交易量与收盘价乘积的波动性与收盘价除以交易量的波动性之比。首先，计算每日交易量与收盘价的乘积以及收盘价除以交易量的比值。然后，分别计算这两个序列在过去60天内的标准差。最后，将乘积的标准差除以比值的标准差。这个比率可以反映价量关系中不同维度的波动性差异。高比率可能表明价量乘积（代表总交易价值的粗略衡量）的波动性大于单位交易量价格的波动性，可能暗示市场在总交易价值上的波动比单位交易价格的波动更显著。该因子创新性地结合了乘法和除法两种价量关系，并通过波动性比率来捕捉市场在不同价量组合上的风险特征，可用于识别具有特定价量波动模式的股票。
    因子应用场景：
    1. 波动性分析：用于识别价量乘积波动性相对于单位交易量价格波动性较高的股票。
    2. 风险评估：评估市场在总交易价值和单位交易价格上的波动性差异，辅助风险管理。
    3. 选股策略：寻找具有特定价量波动模式的股票，构建量化选股策略。
    """
    # 1. 计算 multiply(vol, close)
    data_multiply_vol_close = multiply(data['vol'], data['close'])
    # 2. 计算 ts_std_dev(multiply(vol, close), 60)
    data_ts_std_dev_multiply_vol_close = ts_std_dev(data_multiply_vol_close, 60)
    # 3. 计算 divide(close, vol)
    data_divide_close_vol = divide(data['close'], data['vol'])
    # 4. 计算 ts_std_dev(divide(close, vol), 60)
    data_ts_std_dev_divide_close_vol = ts_std_dev(data_divide_close_vol, 60)
    # 5. 计算 divide(ts_std_dev(multiply(vol, close), 60), ts_std_dev(divide(close, vol), 60))
    factor = divide(data_ts_std_dev_multiply_vol_close, data_ts_std_dev_divide_close_vol)

    # 删除中间变量
    del data_multiply_vol_close
    del data_ts_std_dev_multiply_vol_close
    del data_divide_close_vol
    del data_ts_std_dev_divide_close_vol

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()