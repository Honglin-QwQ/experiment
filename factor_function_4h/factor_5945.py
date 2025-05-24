import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_returns, ts_kurtosis, rank, divide

def factor_5945(data, **kwargs):
    """
    因子名称: Volatility_Kurtosis_Rank_Ratio_27904
    数学表达式: divide(rank(ts_std_dev(close, 180)), rank(ts_kurtosis(ts_returns(close, 30), 40)))
    中文描述: 该因子计算了收盘价的长期波动率排名（过去180天的标准差排名）与短期收益率峰度排名（过去30天收益率的40天峰度排名）之比。
    相较于参考因子，该因子进行了创新：
    1. 使用收盘价代替最低价计算波动率，收盘价更能反映市场共识；
    2. 使用收益率的峰度代替成交量峰度，收益率峰度更能捕捉市场极端风险；
    3. 对波动率和峰度都进行了排名处理，以减少异常值的影响并进行截面比较。
    较高的比值可能表明在相对较低的长期价格波动下，短期内出现了收益率的极端波动，这可能预示着潜在的市场情绪变化或价格异动。
    该因子结合了长期价格波动排名和短期收益率极端性排名，具有创新性，可以用于识别潜在的市场拐点或风险事件。
    改进建议中提到的使用收盘价、收益率峰度和Rank操作符都已采纳以提升因子效果。
    因子应用场景：
    1. 识别潜在市场拐点：较高的因子值可能预示着市场即将发生变化。
    2. 风险事件预警：短期收益率的极端波动可能表明存在潜在的风险事件。
    """
    # 1. 计算 ts_std_dev(close, 180)
    data_ts_std_dev = ts_std_dev(data['close'], d = 180)
    # 2. 计算 rank(ts_std_dev(close, 180))
    data_rank_std = rank(data_ts_std_dev)
    # 3. 计算 ts_returns(close, 30)
    data_ts_returns = ts_returns(data['close'], d = 30)
    # 4. 计算 ts_kurtosis(ts_returns(close, 30), 40)
    data_ts_kurtosis = ts_kurtosis(data_ts_returns, d = 40)
    # 5. 计算 rank(ts_kurtosis(ts_returns(close, 30), 40))
    data_rank_kurtosis = rank(data_ts_kurtosis)
    # 6. 计算 divide(rank(ts_std_dev(close, 180)), rank(ts_kurtosis(ts_returns(close, 30), 40)))
    factor = divide(data_rank_std, data_rank_kurtosis)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()