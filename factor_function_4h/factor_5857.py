import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, divide, ts_std_dev, ts_arg_max, ts_decay_linear, ts_corr, multiply

def factor_5857(data, **kwargs):
    """
    因子名称: VolWeightedPrice_VolatilityRatio_ARGMAX_Decay_56683
    数学表达式: multiply(rank(divide(ts_std_dev(vwap, 10), ts_std_dev(amount, 10))), ts_arg_max(ts_decay_linear(ts_corr(vwap, vol, 60), 90), 120))
    中文描述: 该因子旨在改进基于历史输出的因子，通过调整计算逻辑和引入新的操作符来提升预测能力和稳定性。
            首先，它计算过去10天VWAP标准差与过去10天交易额标准差的比值的排名，使用更短的时间窗口来捕捉短期波动。
            然后，计算过去60天VWAP与交易量的相关性，并对该相关性应用90天的线性衰减加权，赋予近期相关性更高的权重。
            最后，找到过去120天内衰减加权相关性的最大值出现的相对位置。
            最终因子值为波动率比值排名与衰减加权相关性最大值位置的乘积。
            相较于原因子，该因子通过缩短波动率窗口提高对短期变化的敏感性，通过线性衰减加权相关性来强调近期趋势，
            并结合rank和ts_arg_max操作符，旨在捕捉短期量价背离与长期衰减加权相关性的结合信号，可能预示着更具爆发力的动量或反转机会，同时通过rank操作符增强鲁棒性。
    因子应用场景：
    1. 波动率分析： 用于衡量成交量加权平均价（VWAP）和交易额的波动率比率，并通过排名来识别异常波动情况。
    2. 量价关系分析： 结合成交量和价格的相关性，通过线性衰减加权和最大值位置的计算，捕捉量价关系的趋势和转折点。
    3. 趋势反转预测： 通过综合考虑波动率比率和量价关系，辅助判断潜在的趋势反转机会。
    """
    # 1. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 10)
    # 2. 计算 ts_std_dev(amount, 10)
    data_ts_std_dev_amount = ts_std_dev(data['amount'], 10)
    # 3. 计算 divide(ts_std_dev(vwap, 10), ts_std_dev(amount, 10))
    data_divide = divide(data_ts_std_dev_vwap, data_ts_std_dev_amount)
    # 4. 计算 rank(divide(ts_std_dev(vwap, 10), ts_std_dev(amount, 10)))
    data_rank = rank(data_divide, 2)
    # 5. 计算 ts_corr(vwap, vol, 60)
    data_ts_corr = ts_corr(data['vwap'], data['vol'], 60)
    # 6. 计算 ts_decay_linear(ts_corr(vwap, vol, 60), 90)
    data_ts_decay_linear = ts_decay_linear(data_ts_corr, 90)
    # 7. 计算 ts_arg_max(ts_decay_linear(ts_corr(vwap, vol, 60), 90), 120)
    data_ts_arg_max = ts_arg_max(data_ts_decay_linear, 120)
    # 8. 计算 multiply(rank(divide(ts_std_dev(vwap, 10), ts_std_dev(amount, 10))), ts_arg_max(ts_decay_linear(ts_corr(vwap, vol, 60), 90), 120))
    factor = multiply(data_rank, data_ts_arg_max)

    # 删除中间变量
    del data_ts_std_dev_vwap
    del data_ts_std_dev_amount
    del data_divide
    del data_rank
    del data_ts_corr
    del data_ts_decay_linear
    del data_ts_arg_max

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()