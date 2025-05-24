import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_std_dev, ts_delta, multiply

def factor_5753(data, **kwargs):
    """
    因子名称: VolSkewMomentum_StdDev_81196
    数学表达式: ts_skewness(vol, 5) * ts_std_dev(ts_delta(amount, 3), 10)
    中文描述: 该因子结合了成交量的短期偏度和交易额长期变化的波动性。首先计算过去5天成交量的偏度，衡量短期成交量的分布是否对称。然后计算过去10天交易额3日差值的标准差，反映交易额变化幅度的波动性。将两者相乘，旨在捕捉成交量分布的异常与交易额波动的结合效应，可能预示着市场情绪或资金流动的变化。相较于参考因子仅使用平均成交量和其标准差，该因子引入了成交量的偏度和交易额的动态变化，结构更具创新性，并利用了'amount'数据作为新的元素组成。
    因子应用场景：
    1. 市场情绪捕捉： 通过成交量偏度和交易额波动性的结合，可能反映市场参与者的情绪波动，例如恐慌性抛售或过度乐观。
    2. 资金流动预警： 交易额的显著波动可能预示着资金的大规模流入或流出，结合成交量偏度可以更准确地判断资金流动的性质。
    """
    # 1. 计算 ts_skewness(vol, 5)
    data_ts_skewness_vol = ts_skewness(data['vol'], 5)
    # 2. 计算 ts_delta(amount, 3)
    data_ts_delta_amount = ts_delta(data['amount'], 3)
    # 3. 计算 ts_std_dev(ts_delta(amount, 3), 10)
    data_ts_std_dev_delta_amount = ts_std_dev(data_ts_delta_amount, 10)
    # 4. 计算 ts_skewness(vol, 5) * ts_std_dev(ts_delta(amount, 3), 10)
    factor = multiply(data_ts_skewness_vol, data_ts_std_dev_delta_amount)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()