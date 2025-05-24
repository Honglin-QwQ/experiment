import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import abs, ts_delta, ts_entropy, divide

def factor_5916(data, **kwargs):
    """
    因子名称: VolPriceChangeEntropyRatio_16857
    数学表达式: divide(abs(ts_delta(vwap, 5)), ts_entropy(vol, 120))
    中文描述: 该因子计算了过去5天成交量加权平均价格（VWAP）绝对变化与过去120天成交量时间序列熵的比例。VWAP的短期绝对变化衡量了在考虑成交量影响下的短期价格动量。成交量时间序列熵衡量了长期成交量分布的不确定性。将VWAP的短期绝对变化除以长期成交量熵，旨在捕捉在长期成交量不确定性背景下，短期价格动量的相对强度。较高的比值可能表明在长期成交量相对混乱的情况下，短期内出现了由成交量驱动的显著价格变化，这可能预示着市场趋势的形成或加速。相较于参考因子，创新点在于：1. 将分子改为成交量加权平均价格（VWAP）的短期绝对变化，而非简单的收盘价变化，更能反映真实交易驱动的价格变动；2. 将分母改为更长期的成交量熵（120天），以捕捉更宏观的成交量不确定性；3. 颠倒了分子分母的位置，将短期价格动量与长期成交量不确定性进行对比，改变了因子的解读逻辑。改进建议的采纳体现在：1. 采纳了使用成交量加权价格的建议，将分子改为`abs(ts_delta(vwap, 5))`；2. 调整了时间窗口参数，将VWAP变化窗口缩小到5天，成交量熵窗口扩大到120天，以期捕捉不同时间尺度的市场特征；3. 颠倒了分子分母，将短期价格变化放在分子，长期成交量熵放在分母，以测试新的逻辑关系。
    因子应用场景：
    1. 市场波动性分析：该因子可用于识别市场中短期价格动量相对于长期成交量不确定性较高的时间段，可能预示着市场波动性的增加。
    2. 趋势跟踪：当因子值持续较高时，可能表明市场正处于由成交量驱动的趋势中，可以作为趋势跟踪策略的辅助指标。
    3. 交易信号生成：结合其他技术指标，该因子可以用于生成交易信号，例如，当因子值突破一定阈值时，可以考虑买入或卖出。
    """
    # 1. 计算 ts_delta(vwap, 5)
    data_ts_delta_vwap = ts_delta(data['vwap'], 5)
    # 2. 计算 abs(ts_delta(vwap, 5))
    data_abs_ts_delta_vwap = abs(data_ts_delta_vwap)
    # 3. 计算 ts_entropy(vol, 120)
    data_ts_entropy_vol = ts_entropy(data['vol'], 120)
    # 4. 计算 divide(abs(ts_delta(vwap, 5)), ts_entropy(vol, 120))
    factor = divide(data_abs_ts_delta_vwap, data_ts_entropy_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()