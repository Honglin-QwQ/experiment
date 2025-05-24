import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_std_dev, divide

def factor_5951(data, **kwargs):
    """
    数学表达式: divide(ts_skewness(vol, 60), ts_std_dev(vol, 60))
    中文描述: 该因子计算的是过去60天交易量的时间序列偏度与标准差之比。交易量的偏度衡量了交易量分布的对称性，正偏度表示极端高交易量出现的频率高于极端低交易量，负偏度则相反。交易量的标准差衡量了交易量的波动性。将偏度除以标准差可以得到一个标准化后的偏度指标，反映了在考虑交易量波动性的前提下，极端交易量事件的倾向性。这个因子可以用于捕捉市场情绪的非对称性变化以及潜在的交易量动量或反转信号。例如，高值可能表明交易量在波动中倾向于出现极端高峰，这可能预示着市场情绪的剧烈波动或特定事件的影响。
    因子应用场景：
    1. 市场情绪分析： 通过观察偏度与标准差的比率，可以判断市场情绪的非对称性。
    2. 交易量动量或反转信号： 该因子可以用于识别交易量动量或反转的潜在信号。
    3. 风险管理： 因子值较高时，可能预示着市场情绪的剧烈波动或特定事件的影响，有助于风险管理。
    """
    # 1. 计算 ts_skewness(vol, 60)
    data_ts_skewness = ts_skewness(data['vol'], d = 60)
    # 2. 计算 ts_std_dev(vol, 60)
    data_ts_std_dev = ts_std_dev(data['vol'], d = 60)
    # 3. 计算 divide(ts_skewness(vol, 60), ts_std_dev(vol, 60))
    factor = divide(data_ts_skewness, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()