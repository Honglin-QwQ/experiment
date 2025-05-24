import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_decay_exp_window, adv, ts_delta, ts_percentage

def factor_5977(data, **kwargs):
    """
    因子名称: VolPriceMomentumRatio_77637
    数学表达式: divide(ts_decay_exp_window(adv(vol, 30), d = 60, factor = 0.6), ts_delta(ts_percentage(close, 15, percentage = 0.8), 5))
    中文描述: 该因子旨在捕捉成交量的指数衰减动量与价格百分位变化率之间的关系。分子计算过去30天平均成交量的60天指数衰减加权平均值，赋予近期成交量更高的权重，反映成交量的短期趋势和强度。分母计算过去15天收盘价的80%百分位数在过去5天内的变化，反映价格在近期高位附近的动量。将成交量动量除以价格百分位变化率，可以识别在成交量持续活跃或增长的情况下，价格是否能维持或加速其向上动量。如果分子较高而分母较低（价格在高位附近变化不大或回落），可能预示着在高成交量下价格上涨乏力，存在潜在的卖压。反之，如果分子较高且分母较高（价格在高位附近持续上涨），可能预示着强劲的买盘支撑和持续的上涨动能。创新点在于结合了成交量的指数衰减加权平均和价格高百分位的变化率，构建了一个新的比例因子，更精细地衡量市场力量和价格动量的相互作用。
    因子应用场景：
    1. 量价关系分析：用于识别成交量和价格动量之间的背离或共振关系，辅助判断趋势的持续性。
    2. 市场情绪监测：通过成交量和价格的相对变化，评估市场参与者的情绪和交易行为。
    3. 交易信号生成：结合其他技术指标，可以生成买入或卖出信号，尤其是在成交量异常放大或价格动量发生变化时。
    """
    # 1. 计算 adv(vol, 30)
    data_adv_vol = adv(data['vol'], d = 30)
    # 2. 计算 ts_decay_exp_window(adv(vol, 30), d = 60, factor = 0.6)
    data_ts_decay_exp_window = ts_decay_exp_window(data_adv_vol, d = 60, factor = 0.6)
    # 3. 计算 ts_percentage(close, 15, percentage = 0.8)
    data_ts_percentage = ts_percentage(data['close'], d = 15, percentage = 0.8)
    # 4. 计算 ts_delta(ts_percentage(close, 15, percentage = 0.8), 5)
    data_ts_delta = ts_delta(data_ts_percentage, d = 5)
    # 5. 计算 divide(ts_decay_exp_window(adv(vol, 30), d = 60, factor = 0.6), ts_delta(ts_percentage(close, 15, percentage = 0.8), 5))
    factor = divide(data_ts_decay_exp_window, data_ts_delta)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()