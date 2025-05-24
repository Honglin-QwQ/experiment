import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_rank, multiply, log, add

def factor_5686(data, **kwargs):
    """
    因子名称: factor_0001_78412
    数学表达式: ts_zscore(ts_rank(multiply(close,log(add(vol,1))),15),10)
    中文描述: 本因子首先对收盘价和成交量取对数加1后的乘积进行时间序列排名，然后计算该排名的Z-score。该因子旨在捕捉价格和成交量之间的非线性关系，并衡量这种关系的显著性。成交量取对数是为了减小极端值的影响，排名是为了消除量纲影响，Z-score则是为了标准化数据，使其更易于比较。因子创新点在于将价格和成交量进行结合，并使用时间序列排名和Z-score进行处理，从而提取更丰富的市场信息。
    因子应用场景：
    1. 市场情绪分析：可用于识别市场对特定股票或行业的关注度变化。
    2. 交易量异动检测：通过结合价格和交易量，可以更准确地检测交易量的异常波动。
    """
    # 1. 计算 add(vol,1)
    data_add = add(data['vol'], 1)
    # 2. 计算 log(add(vol,1))
    data_log = log(data_add)
    # 3. 计算 multiply(close,log(add(vol,1)))
    data_multiply = multiply(data['close'], data_log)
    # 4. 计算 ts_rank(multiply(close,log(add(vol,1))),15)
    data_ts_rank = ts_rank(data_multiply, d = 15)
    # 5. 计算 ts_zscore(ts_rank(multiply(close,log(add(vol,1))),15),10)
    factor = ts_zscore(data_ts_rank, d = 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()