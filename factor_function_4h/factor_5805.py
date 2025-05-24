import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_zscore, ts_delta, divide

def factor_5805(data, **kwargs):
    """
    因子名称: LowPriceVolatility_Correlation_TradeVolumeRatio_81681
    数学表达式: ts_corr(ts_zscore(ts_delta(low,3), 22), divide(vol, trades), 10)
    中文描述: 该因子结合了参考因子一《低价波动的时序标准化因子》和参考因子二的元素，并引入新的量价关系视角。首先，它计算过去3天最低价变化的22天时序Z分数，捕捉标准化后的短期低价波动。然后，计算成交量与交易笔数的比值（vol/trades），这可以视为单笔交易的平均成交量，反映市场活跃度和订单规模。最后，计算这两个序列在过去10天内的相关性。创新点在于将标准化后的低价波动与单笔交易的平均成交量进行关联，旨在探索低价区域的波动性与市场微观结构的潜在关系。较高的相关性可能表明低价区域的波动与大额订单交易活动同步增加，可能预示着某种市场行为或趋势的形成。该因子可用于识别在低价区域伴随特定交易特征的波动模式，辅助进行技术分析和交易策略制定。
    因子应用场景：
    1. 识别低价区域的波动性与市场微观结构的潜在关系。
    2. 辅助进行技术分析和交易策略制定。
    """
    # 1. 计算 ts_delta(low,3)
    data_ts_delta_low = ts_delta(data['low'], 3)
    # 2. 计算 ts_zscore(ts_delta(low,3), 22)
    data_ts_zscore = ts_zscore(data_ts_delta_low, 22)
    # 3. 计算 divide(vol, trades)
    data_divide = divide(data['vol'], data['trades'])
    # 4. 计算 ts_corr(ts_zscore(ts_delta(low,3), 22), divide(vol, trades), 10)
    factor = ts_corr(data_ts_zscore, data_divide, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()