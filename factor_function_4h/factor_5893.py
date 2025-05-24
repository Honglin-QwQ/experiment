import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, divide, ts_std_dev, ts_mean

def factor_5893(data, **kwargs):
    """
    因子名称: VolatilityDecayMomentum_82202
    数学表达式: ts_decay_exp_window(divide(ts_std_dev(vol, 10), ts_mean(vol, 10)), d = 20, factor = 0.8) - ts_decay_exp_window(divide(ts_std_dev(vol, 30), ts_mean(vol, 30)), d = 60, factor = 0.6)
    中文描述: 该因子计算了短期波动率变异系数的指数衰减加权平均值与长期波动率变异系数的指数衰减加权平均值之差。短期波动率变异系数窗口期为10天，衰减因子为0.8，衰减窗口期为20天。长期波动率变异系数窗口期为30天，衰减因子为0.6，衰减窗口期为60天。该因子旨在捕捉短期波动率相对于长期波动率的动量效应。当短期波动率变异系数的衰减加权平均值高于长期波动率变异系数的衰减加权平均值时，表明短期波动率相对较强，可能预示着市场活跃度的提升或潜在的价格波动加剧。反之，则表明短期波动率相对较弱。相较于参考因子仅关注成交量最小值位置或简单的波动率比率，该因子引入了时间衰减加权平均，并比较了不同时间尺度的波动率变异系数，更精细地捕捉了波动率的动态变化和动量特征。这可以用于识别波动率趋势的变化，作为风险管理或交易策略的信号。
    因子应用场景：
    1. 波动率趋势识别：用于识别短期波动率相对于长期波动率的趋势变化。
    2. 风险管理：当短期波动率显著高于长期波动率时，可能预示着风险增加，可用于调整仓位。
    3. 交易策略：可作为交易信号，例如，当因子值上升时，采取做多策略，反之则做空。
    """
    # 1. 计算短期波动率变异系数: divide(ts_std_dev(vol, 10), ts_mean(vol, 10))
    short_vol_std = ts_std_dev(data['vol'], d = 10)
    short_vol_mean = ts_mean(data['vol'], d = 10)
    short_vol_coef = divide(short_vol_std, short_vol_mean)

    # 2. 计算长期波动率变异系数: divide(ts_std_dev(vol, 30), ts_mean(vol, 30))
    long_vol_std = ts_std_dev(data['vol'], d = 30)
    long_vol_mean = ts_mean(data['vol'], d = 30)
    long_vol_coef = divide(long_vol_std, long_vol_mean)

    # 3. 计算短期波动率变异系数的指数衰减加权平均值: ts_decay_exp_window(divide(ts_std_dev(vol, 10), ts_mean(vol, 10)), d = 20, factor = 0.8)
    short_decay = ts_decay_exp_window(short_vol_coef, d = 20, factor = 0.8)

    # 4. 计算长期波动率变异系数的指数衰减加权平均值: ts_decay_exp_window(divide(ts_std_dev(vol, 30), ts_mean(vol, 30)), d = 60, factor = 0.6)
    long_decay = ts_decay_exp_window(long_vol_coef, d = 60, factor = 0.6)

    # 5. 计算因子值: short_decay - long_decay
    factor = short_decay - long_decay

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()