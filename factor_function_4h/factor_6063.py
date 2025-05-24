import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_scale, ts_corr, ts_skewness

def factor_6063(data, **kwargs):
    """
    因子名称: VWAP_Volume_Skewness_Correlation_Scaled_78051
    数学表达式: ts_scale(ts_corr(ts_skewness(vwap, 10), volume, 15), 25, constant = -0.5)
    中文描述: 该因子通过计算VWAP的偏度与成交量之间的相关性，并进行时间序列标准化来捕捉市场情绪和趋势。首先，计算过去10天VWAP的偏度，衡量价格分布的不对称性。然后，计算这个VWAP偏度序列与过去15天成交量序列之间的滚动相关性，以评估价格分布特征与市场活跃度之间的同步性。最后，对这个相关性序列在过去25天的时间窗口内进行标准化缩放，并减去0.5的常数。创新点在于直接计算VWAP偏度与成交量之间的相关性，而非之前历史输出中计算VWAP偏度与成交量标准差的比值，这更直接地反映了价格分布的不对称性是否得到成交量的确认。通过时间序列缩放和偏移，使因子值更易于比较和解释。正的相关性可能表示当前的价格分布趋势（偏度）得到了成交量的支持，增强了趋势延续的可能性；负的相关性可能表示价格分布趋势与成交量出现背离，预示着潜在的反转。这个因子可以用于识别那些价格趋势得到成交量确认的股票，或者出现量价背离的潜在反转信号。
    因子应用场景：
    1. 趋势识别：识别价格趋势得到成交量确认的股票。
    2. 反转信号：识别量价背离的潜在反转信号。
    """
    # 1. 计算 ts_skewness(vwap, 10)
    data_ts_skewness_vwap = ts_skewness(data['vwap'], 10)
    # 2. 计算 ts_corr(ts_skewness(vwap, 10), volume, 15)
    data_ts_corr = ts_corr(data_ts_skewness_vwap, data['vol'], 15)
    # 3. 计算 ts_scale(ts_corr(ts_skewness(vwap, 10), volume, 15), 25, constant = -0.5)
    factor = ts_scale(data_ts_corr, 25, constant = -0.5)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()