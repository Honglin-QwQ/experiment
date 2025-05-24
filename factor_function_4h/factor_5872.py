import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, divide, ts_decay_exp_window, ts_entropy, sqrt, ts_std_dev

def factor_5872(data, **kwargs):
    """
    数学表达式: rank(divide(ts_decay_exp_window(ts_entropy(vol, 15), 25, factor = 0.8), sqrt(ts_std_dev(vol, 25))))
    中文描述: 该因子计算过去25天内经过指数衰减加权处理的成交量时间序列熵与成交量标准差平方根的比值的排名。相较于参考因子，该因子：1. 调整了熵计算的窗口期（从20天缩短至15天），以更关注近期的成交量分布复杂性。2. 调整了指数衰减加权的窗口期（从31天缩短至25天）和衰减因子（从0.7调整至0.8），赋予近期数据更高的权重，并缩短了历史数据的影响范围。3. 将分母的成交量标准差替换为其平方根，引入非线性变换，可能更好地捕捉波动率的非线性特征。4. 最后对计算结果进行了排名处理，降低异常值的影响并增强因子的区分度。高排名可能表明近期成交量波动模式复杂且信息丰富，且这种复杂性正在衰减，而低排名可能表明近期成交量波动相对简单或随机，或者复杂性正在增强，并对近期市场行为赋予更高的关注度。这可以用于识别市场情绪变化或潜在的价格变动驱动因素，并对近期市场行为赋予更高的关注度，且对极端值不敏感。
    因子应用场景：
    1. 市场情绪识别：通过成交量熵的变化，识别市场参与者的情绪状态。
    2. 波动率预测：结合成交量熵与标准差，预测未来的波动率水平。
    3. 交易信号生成：根据因子排名，生成买入或卖出信号。
    """
    # 1. 计算 ts_entropy(vol, 15)
    data_ts_entropy = ts_entropy(data['vol'], 15)
    # 2. 计算 ts_decay_exp_window(ts_entropy(vol, 15), 25, factor = 0.8)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_entropy, 25, factor = 0.8)
    # 3. 计算 ts_std_dev(vol, 25)
    data_ts_std_dev = ts_std_dev(data['vol'], 25)
    # 4. 计算 sqrt(ts_std_dev(vol, 25))
    data_sqrt = sqrt(data_ts_std_dev)
    # 5. 计算 divide(ts_decay_exp_window(ts_entropy(vol, 15), 25, factor = 0.8), sqrt(ts_std_dev(vol, 25)))
    data_divide = divide(data_ts_decay_exp_window, data_sqrt)
    # 6. 计算 rank(divide(ts_decay_exp_window(ts_entropy(vol, 15), 25, factor = 0.8), sqrt(ts_std_dev(vol, 25))))
    factor = rank(data_divide, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()