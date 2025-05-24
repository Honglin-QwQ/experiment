import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_mean, ts_zscore, ts_corr, rank, adv

def factor_5791(data, **kwargs):
    """
    因子名称: VolumeVolatilityAdjustedLowPrice_42431
    数学表达式: ts_mean(low, 15) * ts_zscore(adv(20), 252) - rank(ts_corr(vol, close, 15))
    中文描述: 该因子结合了最低价格的长期平均水平、平均成交量的长期波动性以及成交量与收盘价的短期相关性。
            首先计算过去15天最低价的平均值，作为衡量股票长期价格支撑的指标。
            然后计算过去20天平均成交量在过去252天内的Z得分，以衡量当前成交量相对于长期平均水平的异常程度。
            最后，计算过去15天成交量与收盘价的相关性，并对其进行排名，反映短期量价关系的强度。
            最终因子表达式为前两项的乘积减去第三项的排名。
            该因子试图识别那些在长期价格支撑位附近、同时伴随异常成交量波动且短期量价关系较强的股票，可能预示着潜在的交易机会或风险。
            相较于参考因子，该因子引入了成交量的长期波动性（通过Z得分衡量），并将其与最低价的长期平均值相结合，形成一个乘积项，增强了因子对价格和成交量相互作用的敏感性。
            同时，保留了短期量价相关性的排名，作为对短期市场情绪的考量。
    因子应用场景：
    1. 识别潜在的交易机会或风险。
    2. 辅助判断股票的长期价格支撑、成交量波动以及短期量价关系。
    """
    # 1. 计算 ts_mean(low, 15)
    data_ts_mean_low = ts_mean(data['low'], 15)
    # 2. 计算 adv(20)
    data_adv = adv(data['vol'], 20)
    # 3. 计算 ts_zscore(adv(20), 252)
    data_ts_zscore_adv = ts_zscore(data_adv, 252)
    # 4. 计算 ts_corr(vol, close, 15)
    data_ts_corr_vol_close = ts_corr(data['vol'], data['close'], 15)
    # 5. 计算 rank(ts_corr(vol, close, 15))
    data_rank_ts_corr_vol_close = rank(data_ts_corr_vol_close, 2)
    # 6. 计算 ts_mean(low, 15) * ts_zscore(adv(20), 252)
    data_multiply = data_ts_mean_low * data_ts_zscore_adv
    # 7. 计算 ts_mean(low, 15) * ts_zscore(adv(20), 252) - rank(ts_corr(vol, close, 15))
    factor = data_multiply - data_rank_ts_corr_vol_close

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()