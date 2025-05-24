import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide
from operators import ts_entropy
from operators import ts_std_dev
from operators import log

def factor_5649(data, **kwargs):
    """
    因子名称: VolumeAdjustedVolatilityEntropy_21009
    数学表达式: divide(ts_entropy(ts_std_dev(close, 5), 31), ts_std_dev(log(vol), 66))
    中文描述: 该因子旨在衡量经成交量波动率调整后的价格波动不确定性。因子首先计算过去5天收盘价标准差，再计算过去31天收盘价标准差的信息熵，然后除以过去66天成交量取对数后的标准差。这与之前的因子相比，创新之处在于使用收盘价标准差的熵，而非收益率的熵，试图捕捉市场在不同成交量水平下的价格波动信息含量。该因子可能用于识别在成交量较低迷时期价格波动信息量异常高的股票，或者在成交量剧烈波动时期价格波动信息量相对稳定的股票。
    因子应用场景：
    1. 识别成交量低迷时期价格波动信息量异常高的股票。
    2. 识别成交量剧烈波动时期价格波动信息量相对稳定的股票。
    """
    # 1. 计算 ts_std_dev(close, 5)
    data_ts_std_dev_close = ts_std_dev(data['close'], 5)
    # 2. 计算 ts_entropy(ts_std_dev(close, 5), 31)
    data_ts_entropy = ts_entropy(data_ts_std_dev_close, 31)
    # 3. 计算 log(vol)
    data_log_vol = log(data['vol'])
    # 4. 计算 ts_std_dev(log(vol), 66)
    data_ts_std_dev_log_vol = ts_std_dev(data_log_vol, 66)
    # 5. 计算 divide(ts_entropy(ts_std_dev(close, 5), 31), ts_std_dev(log(vol), 66))
    factor = divide(data_ts_entropy, data_ts_std_dev_log_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()