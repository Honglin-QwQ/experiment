import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, multiply

def factor_0005(data, **kwargs):
    """
    数学表达式: (-1 * ts_corr(open, volume, 10))
    中文描述: 详细描述：这个因子计算过去10天开盘价和成交量的相关系数，然后取负值。相关系数衡量了两个变量之间的线性关系强度和方向，取负值后，原本正相关的股票会变成负值，原本负相关的股票会变成正值，没有相关性的股票接近于零。金融意义在于，如果开盘价和成交量呈现负相关，意味着开盘价越高，成交量反而越低，反之亦然。
    因子应用场景：
    1. 可以用于识别开盘价和成交量之间存在异常关系的股票，例如，高开低走且成交量萎缩的股票，可能预示着下跌风险。
    2. 可以构建配对交易策略，寻找开盘价和成交量相关性相反的股票进行配对。
    3. 可以作为其他复杂量化模型的输入特征，帮助模型更好地理解市场情绪和交易行为。
    """
    # 1. 计算 ts_corr(open, volume, 10)
    data_ts_corr = ts_corr(data['open'], data['vol'], 10)
    # 2. 计算 -1 * ts_corr(open, volume, 10)
    factor = multiply(-1, data_ts_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()