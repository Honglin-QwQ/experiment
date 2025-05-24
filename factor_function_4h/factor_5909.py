import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, jump_decay
import pandas as pd

def factor_5909(data, **kwargs):
    """
    因子名称: VolumeAmountJumpDecayRatio_66919
    数学表达式: divide(jump_decay(vol, d = 10, sensitivity = 0.2, force = 0.05), jump_decay(amount, d = 10, sensitivity = 0.2, force = 0.05))
    中文描述: 该因子计算过去10天内交易量跳跃衰减值与交易额跳跃衰减值的比值。跳跃衰减值用于平滑序列，捕捉数据相对于历史数据的显著变化并进行衰减处理。通过比较交易量和交易额的跳跃衰减比值，该因子旨在识别市场活跃度和资金流动中是否存在不寻常的、经过平滑处理的相对变化。如果该比值较高，可能意味着交易量相对于其历史均值存在较大的、经过衰减的跳跃，而交易额的跳跃相对较小，这可能预示着市场活跃度在经历非线性变化，而资金流动相对稳定。反之，如果比值较低，则可能意味着交易额的跳跃较大而交易量跳跃较小，可能预示着资金流动在经历非线性变化，而活跃度相对稳定。该因子在历史输出因子的基础上，引入了'jump_decay'操作符，对交易量和交易额的原始数据进行了非线性平滑处理，并捕捉了跳跃变化，从而更精细地分析市场波动特征和资金流动的非线性动态，是对现有波动率因子的创新性改进。
    因子应用场景：
    1. 市场活跃度分析：用于识别交易量相对于交易额的异常波动，判断市场活跃度的变化。
    2. 资金流动分析：用于识别资金流动相对于交易量的异常波动，判断资金流动的变化。
    3. 波动率预测：结合其他波动率因子，提高波动率预测的准确性。
    """
    # 1. 计算 jump_decay(vol, d = 10, sensitivity = 0.2, force = 0.05)
    data_jump_decay_vol = jump_decay(data['vol'], d = 10, sensitivity = 0.2, force = 0.05)
    # 2. 计算 jump_decay(amount, d = 10, sensitivity = 0.2, force = 0.05)
    data_jump_decay_amount = jump_decay(data['amount'], d = 10, sensitivity = 0.2, force = 0.05)
    # 3. 计算 divide(jump_decay(vol, d = 10, sensitivity = 0.2, force = 0.05), jump_decay(amount, d = 10, sensitivity = 0.2, force = 0.05))
    factor = divide(data_jump_decay_vol, data_jump_decay_amount)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()