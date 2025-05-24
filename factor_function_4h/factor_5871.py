import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_decay_linear, multiply, subtract, divide, abs

def factor_5871(data, **kwargs):
    """
    因子名称: VolatilityMomentumRatio_Decay_13630
    数学表达式: divide(ts_std_dev(multiply(abs(subtract(open, close)), vol), 15), ts_decay_linear(multiply(abs(subtract(open, close)), vol), 15))
    中文描述: 该因子计算开盘价与收盘价差值的绝对值与成交量乘积在短期窗口内的标准差与该乘积的线性衰减平均值的比值。开盘价与收盘价的差值反映了日内的价格波动和方向，将其与成交量相乘可以衡量带有市场活跃度的日内波动强度。其标准差衡量了这种带有市场活跃度的日内波动的剧烈程度。乘积的线性衰减平均值则赋予近期带有市场活跃度的日内波动更大的权重，反映了近期该类波动的平均水平。通过将带有市场活跃度的日内波动的标准差与带权重的平均波动相结合，该因子试图捕捉近期带有市场活跃度的日内波动的相对强度和持续性。较高的值可能表示近期带有市场活跃度的日内波动异常剧烈，而较低的值可能表示该类波动相对稳定。这可以用于识别日内交易的潜在机会或风险。相较于参考因子，该因子创新性地将开盘价与收盘价差值的绝对值与成交量相乘来衡量带有市场活跃度的日内波动，并结合了标准差和线性衰减平均值来分析其特征，同时使用了除法操作符来衡量两者的相对关系，提供了更丰富的市场信息。此外，该因子在分母中使用了乘积的绝对值，避免了负值的影响，提高了因子的稳定性。改进方向根据评估报告，引入了成交量来增强因子对市场活跃度的捕捉能力，并调整了时间窗口参数，期望提升因子的预测能力和稳定性。
    因子应用场景：
    1. 识别日内交易的潜在机会或风险。
    2. 衡量市场活跃度的日内波动强度。
    """
    # 1. 计算 subtract(open, close)
    data_subtract = subtract(data['open'], data['close'])
    # 2. 计算 abs(subtract(open, close))
    data_abs = abs(data_subtract)
    # 3. 计算 multiply(abs(subtract(open, close)), vol)
    data_multiply = multiply(data_abs, data['vol'])
    # 4. 计算 ts_std_dev(multiply(abs(subtract(open, close)), vol), 15)
    data_ts_std_dev = ts_std_dev(data_multiply, d=15)
    # 5. 计算 ts_decay_linear(multiply(abs(subtract(open, close)), vol), 15)
    data_ts_decay_linear = ts_decay_linear(data_multiply, d=15)
    # 6. 计算 divide(ts_std_dev(multiply(abs(subtract(open, close)), vol), 15), ts_decay_linear(multiply(abs(subtract(open, close)), vol), 15))
    factor = divide(data_ts_std_dev, data_ts_decay_linear)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()