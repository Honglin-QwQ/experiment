import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_weighted_decay, ts_corr, ts_std_dev
import pandas as pd

def factor_5878(data, **kwargs):
    """
    因子名称: ts_corr_amount_vol_decay_std_ratio_54626
    数学表达式: divide(ts_weighted_decay(ts_corr(amount, vol, 15), k=0.4), ts_std_dev(amount, 30))
    中文描述: 该因子旨在捕捉交易额和成交量之间经过加权衰减的相关性，并用交易额的波动性进行标准化。首先，计算过去15天内交易额（amount）和成交量（vol）的相关性（ts_corr），反映资金流动强度与交易活跃度的关系。然后，对该相关性应用一个加权衰减（ts_weighted_decay），权重因子k=0.4，使得近期的相关性影响更大。最后，将衰减后的相关性除以过去30天交易额的标准差（ts_std_dev），以交易额的波动性进行标准化。因子值较高可能表明在相对稳定的交易额波动下，近期资金流动强度与交易活跃度呈现较强的正相关，可能预示着趋势的持续。相较于参考因子，该因子创新性地使用了交易额（amount）作为核心变量，并结合了加权衰减和波动性标准化，旨在更全面地评估资金流动与交易活跃度的关系，并考虑了市场的波动环境。同时，根据改进建议，引入了ts_weighted_decay操作符来增强近期数据的敏感性，并利用ts_std_dev对波动性进行标准化，以提高因子的稳定性和预测能力。该因子适用于捕捉资金驱动的市场趋势。
    因子应用场景：
    1. 资金流动性分析：用于衡量交易额和成交量之间的关系，判断市场资金的活跃程度。
    2. 趋势判断：结合加权衰减，可以更敏感地捕捉近期资金流动与交易活跃度的相关性，辅助判断市场趋势。
    3. 波动率标准化：通过交易额的标准差进行标准化，可以降低市场波动对因子值的影响，提高因子的稳定性。
    """
    # 1. 计算 ts_corr(amount, vol, 15)
    data_ts_corr = ts_corr(data['amount'], data['vol'], d=15)
    # 2. 计算 ts_weighted_decay(ts_corr(amount, vol, 15), k=0.4)
    data_ts_weighted_decay = ts_weighted_decay(data_ts_corr, k=0.4)
    # 3. 计算 ts_std_dev(amount, 30)
    data_ts_std_dev = ts_std_dev(data['amount'], d=30)
    # 4. 计算 divide(ts_weighted_decay(ts_corr(amount, vol, 15), k=0.4), ts_std_dev(amount, 30))
    factor = divide(data_ts_weighted_decay, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()