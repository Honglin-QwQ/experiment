import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev
import pandas as pd

def factor_5754(data, **kwargs):
    """
    数学表达式: divide(ts_std_dev(volume, 120), ts_std_dev(close, 120))
    中文描述: 该因子计算过去120天交易量标准差与收盘价标准差的比值。它旨在衡量交易量的波动性相对于价格波动性的强度。当交易量波动性远大于价格波动性时，可能预示着市场情绪的剧烈波动或潜在的价格异动。创新点在于通过比较两种不同维度的波动性来捕捉市场信号，而非仅仅关注单一维度的波动。这可以帮助识别那些交易活跃但价格相对稳定的股票，或者交易不活跃但价格剧烈波动的股票，为投资决策提供新的视角。改进方向上，参考了评估结果中关于参数优化的建议，将时间窗口设置为120天，以捕捉更长期的波动特征，并使用了divide操作符来计算比值，直接衡量两种波动性的相对强度。
    因子应用场景：
    1. 波动性分析：用于衡量交易量波动性与价格波动性的相对强度。
    2. 市场情绪监测：交易量波动性远大于价格波动性时，可能预示市场情绪的剧烈波动。
    3. 股票筛选：识别交易活跃但价格相对稳定的股票，或交易不活跃但价格剧烈波动的股票。
    """
    # 1. 计算 ts_std_dev(volume, 120)
    volume_std = ts_std_dev(data['vol'], d=120)
    # 2. 计算 ts_std_dev(close, 120)
    close_std = ts_std_dev(data['close'], d=120)
    # 3. 计算 divide(ts_std_dev(volume, 120), ts_std_dev(close, 120))
    factor = divide(volume_std, close_std)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()