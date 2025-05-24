import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_entropy

def factor_6081(data, **kwargs):
    """
    因子名称: VolPriceEntropyRatio_79281
    数学表达式: divide(ts_entropy(vol, 60), ts_entropy(close, 60))
    中文描述: 该因子计算过去60天内交易量的信息熵与收盘价信息熵的比值。信息熵衡量了数据序列的随机性和不确定性。交易量信息熵高表示交易量变化较大且难以预测，收盘价信息熵高表示价格波动剧烈且无明显趋势。该因子通过比较两者信息熵的相对水平，旨在捕捉市场情绪和价格趋势的微妙变化。例如，当交易量信息熵远高于收盘价信息熵时，可能预示着市场在交易层面存在较大的不确定性，而价格尚未完全反映这种不确定性，可能是一个潜在的交易信号。创新点在于结合了交易量和价格的信息熵，并使用比值来衡量它们之间的相对关系，而非简单的线性组合或相关性。
    因子应用场景：
    1. 市场情绪捕捉： 通过比较交易量和价格的信息熵，识别市场情绪的不确定性。
    2. 趋势潜在信号： 当交易量信息熵远高于收盘价信息熵时，可能预示市场存在潜在的交易机会。
    """
    # 1. 计算 ts_entropy(vol, 60)
    data_ts_entropy_vol = ts_entropy(data['vol'], 60)
    # 2. 计算 ts_entropy(close, 60)
    data_ts_entropy_close = ts_entropy(data['close'], 60)
    # 3. 计算 divide(ts_entropy(vol, 60), ts_entropy(close, 60))
    factor = divide(data_ts_entropy_vol, data_ts_entropy_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()