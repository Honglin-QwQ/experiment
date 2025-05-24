import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, abs, subtract, ts_decay_exp_window, divide

def factor_5812(data, **kwargs):
    """
    数学表达式: divide(ts_std_dev(vwap, 10), abs(subtract(vwap, ts_decay_exp_window(vwap, 20, 0.8))))
    中文描述: 该因子计算过去10天VWAP标准差与当前VWAP和过去20天指数衰减加权平均VWAP差值的绝对值的比值。相较于参考因子，该因子在波动率计算中使用了更短的时间窗口（10天）以捕捉短期波动，同时引入了指数衰减加权平均VWAP（20天窗口，0.8衰减因子）来衡量VWAP的长期趋势，并计算当前VWAP与该长期趋势的偏离。这种结构旨在捕捉短期波动与长期趋势偏离之间的关系，可能更有效地识别VWAP在趋势中的相对波动性，从而提高因子的预测能力。分母使用指数衰减平均值与当前值的差值，相较于简单的滞后差值，更能反映VWAP相对于其平滑趋势的偏离程度，降低了对短期噪音的敏感度，并对近期数据赋予更高的权重，符合改进建议中引入趋势过滤器和平滑波动率的思路。同时，分母使用绝对值，确保因子值为正，避免了负值带来的解释困难。
    因子应用场景：
    1. 波动性分析：用于衡量VWAP的短期波动相对于长期趋势偏离的程度。
    2. 趋势识别：辅助识别VWAP在趋势中的相对波动性，可能预示趋势的强弱或反转。
    3. 风险管理：可用于评估资产价格的波动风险，特别是在趋势变化时。
    """
    # 1. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev = ts_std_dev(data['vwap'], 10)
    # 2. 计算 ts_decay_exp_window(vwap, 20, 0.8)
    data_ts_decay_exp_window = ts_decay_exp_window(data['vwap'], 20, 0.8)
    # 3. 计算 subtract(vwap, ts_decay_exp_window(vwap, 20, 0.8))
    data_subtract = subtract(data['vwap'], data_ts_decay_exp_window)
    # 4. 计算 abs(subtract(vwap, ts_decay_exp_window(vwap, 20, 0.8)))
    data_abs = abs(data_subtract)
    # 5. 计算 divide(ts_std_dev(vwap, 10), abs(subtract(vwap, ts_decay_exp_window(vwap, 20, 0.8))))
    factor = divide(data_ts_std_dev, data_abs)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()