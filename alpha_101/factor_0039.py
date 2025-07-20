import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_std_dev, multiply, subtract

def factor_0039(data, **kwargs):
    """
    数学表达式: ((-1 * rank(ts_std_dev(high, 10))) * ts_corr(high, volume, 10))
    中文描述: 该因子首先计算过去10天股价最高价的标准差，然后对标准差进行排序并取负，接着计算过去10天股价最高价和成交量的相关性，最后将负的排序结果与相关性相乘。该因子可能捕捉了股价波动率和量价关系反向变动的趋势，数值较高可能意味着股价波动较小且量价背离。
    因子应用场景：
    1. 识别潜在的反转机会，当因子值较高时，可能预示着超买或超卖状态；
    2. 作为量化交易策略的输入特征，与其他因子结合使用，提高模型预测的准确性；
    3. 用于构建风险模型，评估股票的波动率风险和量价关系风险。
    """
    # 1. 计算 ts_std_dev(high, 10)
    data_ts_std_dev = ts_std_dev(data['high'], 10)
    # 2. 计算 rank(ts_std_dev(high, 10))
    data_rank = rank(data_ts_std_dev, 2)
    # 3. 计算 -1 * rank(ts_std_dev(high, 10))
    data_neg_rank = subtract(0, data_rank)
    # 4. 计算 ts_corr(high, volume, 10)
    data_ts_corr = ts_corr(data['high'], data['vol'], 10)
    # 5. 计算 ((-1 * rank(ts_std_dev(high, 10))) * ts_corr(high, volume, 10))
    factor = multiply(data_neg_rank, data_ts_corr)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()