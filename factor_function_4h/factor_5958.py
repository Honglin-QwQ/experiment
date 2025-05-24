import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_std_dev, jump_decay, ts_zscore

def factor_5958(data, **kwargs):
    """
    因子名称: VolatilityJumpZScore_33858
    数学表达式: ts_zscore(jump_decay(ts_std_dev(open, 10), d=5, sensitivity=0.6, force=0.2), 15)
    中文描述: 该因子借鉴了历史因子的波动率Z-Score思想，并结合了改进建议中提到的jump_decay操作符，以及对波动率变化和参数优化的考量。首先，它计算过去10天开盘价的标准差（ts_std_dev(open, 10)），作为衡量短期开盘价波动率的基础。然后，使用jump_decay操作符（d=5, sensitivity=0.6, force=0.2）来平滑和捕捉开盘价波动率序列中的“跳跃”或显著变化，这比直接对波动率进行Z-Score更能反映波动率的动态特征和潜在的市场情绪突变。最后，对经过jump_decay处理后的波动率序列计算过去15天内的Z-Score（ts_zscore(..., 15)）。这个Z-Score衡量了近期波动率跳跃相对于更长期的波动率跳跃均值和标准差的异常程度。高或低的Z-Score可能预示着市场情绪的剧烈变化或潜在的趋势反转。相较于原始因子，本因子通过jump_decay操作符更精细地捕捉波动率的突变，并将其标准化，期望能提升因子的预测能力和稳定性，特别是在市场波动加剧或趋势反转初期。
    因子应用场景：
    1. 波动率分析：用于衡量市场波动率的异常程度，高值可能预示市场波动加剧。
    2. 趋势反转预警：Z-Score的高低值可能指示潜在的市场趋势反转点。
    3. 风险管理：帮助识别市场风险较高的时期，辅助调整仓位。
    """
    # 1. 计算 ts_std_dev(open, 10)
    data_ts_std_dev = ts_std_dev(data['open'], d=10)
    # 2. 计算 jump_decay(ts_std_dev(open, 10), d=5, sensitivity=0.6, force=0.2)
    data_jump_decay = jump_decay(data_ts_std_dev, d=5, sensitivity=0.6, force=0.2)
    # 3. 计算 ts_zscore(jump_decay(ts_std_dev(open, 10), d=5, sensitivity=0.6, force=0.2), 15)
    factor = ts_zscore(data_jump_decay, d=15)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()