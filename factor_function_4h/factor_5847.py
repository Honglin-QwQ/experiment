import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_mean, ts_decay_linear, ts_delta, divide

def factor_5847(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Decay_Ratio_Improved_49560
    数学表达式: divide(divide(ts_std_dev(vwap, 15),ts_mean(vwap,15)), ts_decay_linear(ts_delta(vwap, 1), 15, dense=True))
    中文描述: 该因子是基于历史因子VWAP_Volatility_Decay_Ratio的改进版本，旨在提高其预测能力和稳定性。分子部分计算过去15天VWAP的标准差与过去15天VWAP均值的比值，从而对波动率进行标准化，提高不同股票之间的可比性。分母部分计算过去15天VWAP日间变化的线性衰减加权平均值，与原因子不同的是，这里保留了价格变化的方向信息，使用ts_delta(vwap, 1)而不是abs(ts_delta(vwap, 1))，以捕捉价格趋势的方向。通过divide操作将标准化波动率与考虑方向的近期平均价格变动幅度相除，得到一个更全面反映波动率和趋势信息的指标。相较于原因子，创新点在于引入了标准化波动率和价格趋势方向信息，并调整了时间窗口，预期能提高因子在趋势性行情中的表现和整体稳定性。
    因子应用场景：
    1. 波动率分析：用于衡量股票价格波动程度，并进行标准化处理，提高不同股票之间的可比性。
    2. 趋势跟踪：结合价格变化的方向信息，捕捉价格趋势，辅助判断股票的上涨或下跌趋势。
    3. 风险管理：综合考虑波动率和趋势，为投资组合的风险管理提供参考。
    """
    # 1. 计算 ts_std_dev(vwap, 15)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 15)
    # 2. 计算 ts_mean(vwap, 15)
    data_ts_mean_vwap = ts_mean(data['vwap'], 15)
    # 3. 计算 divide(ts_std_dev(vwap, 15),ts_mean(vwap,15))
    data_divide_std_mean = divide(data_ts_std_dev_vwap, data_ts_mean_vwap)
    # 4. 计算 ts_delta(vwap, 1)
    data_ts_delta_vwap = ts_delta(data['vwap'], 1)
    # 5. 计算 ts_decay_linear(ts_delta(vwap, 1), 15, dense=True)
    data_ts_decay_linear_delta = ts_decay_linear(data_ts_delta_vwap, 15, dense=True)
    # 6. 计算 divide(divide(ts_std_dev(vwap, 15),ts_mean(vwap,15)), ts_decay_linear(ts_delta(vwap, 1), 15, dense=True))
    factor = divide(data_divide_std_mean, data_ts_decay_linear_delta)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()