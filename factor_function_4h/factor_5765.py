import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delta, adv, abs, divide

def factor_5765(data, **kwargs):
    """
    因子名称: volatility_volume_oscillation_ratio_73378
    数学表达式: divide(ts_std_dev(returns, 20), abs(ts_delta(adv(vol, 10), 1)))
    中文描述: 该因子衡量短期收益率波动率与超短期平均成交量变化绝对值之间的比率。具体来说，它计算过去20天的日收益率标准差（衡量短期波动率），然后计算过去10天平均成交量相对于前一天的变化（衡量超短期成交量动量），并取其绝对值。最后，用短期波动率除以超短期成交量变化绝对值。该因子旨在捕捉市场在波动与即时成交量变化之间的关系。当波动率相对较高而成交量变化较小时，因子值较大，可能指示市场处于震荡或犹豫状态；当波动率相对较低而成交量变化较大时，因子值较小，可能指示市场正在形成趋势。创新点在于结合了不同时间尺度的波动率和成交量指标，并使用比率来衡量它们之间的相对强度，同时通过取成交量变化的绝对值来关注其变化幅度而非方向，以应对改进建议中提到的可能存在的逻辑问题和参数优化方向，并尝试使用divide和abs操作符来提升因子的表现。
    因子应用场景：
    1. 震荡市场识别：因子值较高可能指示市场处于震荡或犹豫状态。
    2. 趋势形成判断：因子值较低可能指示市场正在形成趋势。
    3. 波动率与成交量关系分析：该因子可以帮助分析师理解波动率与成交量变化之间的关系。
    """
    # 1. 计算 ts_std_dev(returns, 20)
    data_ts_std_dev = ts_std_dev(data['returns'], 20)
    # 2. 计算 adv(vol, 10)
    data_adv = adv(data['vol'], 10)
    # 3. 计算 ts_delta(adv(vol, 10), 1)
    data_ts_delta = ts_delta(data_adv, 1)
    # 4. 计算 abs(ts_delta(adv(vol, 10), 1))
    data_abs = abs(data_ts_delta)
    # 5. 计算 divide(ts_std_dev(returns, 20), abs(ts_delta(adv(vol, 10), 1)))
    factor = divide(data_ts_std_dev, data_abs)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()