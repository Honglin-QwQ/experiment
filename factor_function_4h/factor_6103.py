import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import add, ts_decay_exp_window, sigmoid, scale, ts_corr

def factor_6103(data, **kwargs):
    """
    因子名称: ts_decay_exp_corr_vol_tbase_tquote_nonlinear_momentum_32535
    数学表达式: add(ts_decay_exp_window(sigmoid(scale(ts_corr(vol, tbase, 10))), 5, factor = 0.7), ts_decay_exp_window(sigmoid(scale(ts_corr(vol, tquote, 10))), 5, factor = 0.7))
    中文描述: 该因子在原有成交量与主动买卖数量相关性因子的基础上进行创新。首先，计算成交量(vol)与主动买入基础币种数量(tbase)以及成交量(vol)与主动买入计价币种数量(tquote)在过去10天内的相关性。然后，对这些相关系数进行标准化（scale）和非线性变换（sigmoid），以增强因子对不同股票的区分度并捕捉潜在的非线性关系。最后，通过过去5天的指数衰减加权平均（ts_decay_exp_window）来突出近期相关性的影响，并将两个衰减后的结果相加。相较于原始因子，引入非线性变换旨在更精细地捕捉市场动态，提高因子的预测能力。因子值高可能表明近期成交量与主动买卖行为呈现较强的非线性正相关，预示着潜在的上涨动能；反之，低值可能暗示负相关或相关性减弱，可能预示下跌或盘整。该因子适用于波动率较高或震荡市场。
    因子应用场景：
    1. 动量分析：捕捉成交量与主动买卖行为之间的非线性关系，识别潜在的上涨或下跌动能。
    2. 市场情绪监测：通过成交量与主动买卖相关性的变化，评估市场参与者的情绪和交易行为。
    3. 波动率策略：适用于波动率较高或震荡的市场环境，辅助判断趋势方向和强度。
    """
    # 1. 计算 ts_corr(vol, tbase, 10)
    data_ts_corr_vol_tbase = ts_corr(data['vol'], data['tbase'], 10)
    # 2. 计算 scale(ts_corr(vol, tbase, 10))
    data_scale_ts_corr_vol_tbase = scale(data_ts_corr_vol_tbase)
    # 3. 计算 sigmoid(scale(ts_corr(vol, tbase, 10)))
    data_sigmoid_scale_ts_corr_vol_tbase = sigmoid(data_scale_ts_corr_vol_tbase)
    # 4. 计算 ts_decay_exp_window(sigmoid(scale(ts_corr(vol, tbase, 10))), 5, factor = 0.7)
    data_ts_decay_exp_window_1 = ts_decay_exp_window(data_sigmoid_scale_ts_corr_vol_tbase, 5, factor = 0.7)

    # 5. 计算 ts_corr(vol, tquote, 10)
    data_ts_corr_vol_tquote = ts_corr(data['vol'], data['tquote'], 10)
    # 6. 计算 scale(ts_corr(vol, tquote, 10))
    data_scale_ts_corr_vol_tquote = scale(data_ts_corr_vol_tquote)
    # 7. 计算 sigmoid(scale(ts_corr(vol, tquote, 10)))
    data_sigmoid_scale_ts_corr_vol_tquote = sigmoid(data_scale_ts_corr_vol_tquote)
    # 8. 计算 ts_decay_exp_window(sigmoid(scale(ts_corr(vol, tquote, 10))), 5, factor = 0.7)
    data_ts_decay_exp_window_2 = ts_decay_exp_window(data_sigmoid_scale_ts_corr_vol_tquote, 5, factor = 0.7)

    # 9. 计算 add(ts_decay_exp_window(sigmoid(scale(ts_corr(vol, tbase, 10))), 5, factor = 0.7), ts_decay_exp_window(sigmoid(scale(ts_corr(vol, tquote, 10))), 5, factor = 0.7))
    factor = add(data_ts_decay_exp_window_1, data_ts_decay_exp_window_2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()