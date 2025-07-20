import inspect
from operators import *

def factor_0025(data, **kwargs):
    """
    数学表达式: ts_rank(multiply(ts_decay_linear(ts_corr(rank(ts_std_dev(returns, 5)), rank(subtract(vwap, ts_delay(vwap, 3))), 8), 12), signed_power(ts_delta(turnover_ratio, 2), 0.5)), 10)
    中文描述: 该因子结合了波动率、价格动量和流动性变化的自适应特征。首先计算5日收益率标准差的排名，反映短期波动率水平；然后计算VWAP与3日前VWAP差值的排名，捕捉价格动量；接着计算这两个排名序列在8日内的相关性，识别波动率与动量的同步性；对相关性进行12日线性衰减加权，强调近期信息；同时计算换手率2日变化的平方根，捕捉流动性冲击；将衰减加权的相关性与流动性变化相乘，最后计算10日时序排名。该因子能够识别在波动率上升的同时价格动量增强且伴随适度流动性变化的股票，通常预示着趋势延续或反转的机会。
    应用场景：
    1. 动量策略增强，在传统动量基础上加入波动率和流动性约束
    2. 风险管理，识别波动率与动量背离的异常股票
    3. 择时交易，捕捉市场结构性变化带来的交易机会
    """
    # 1. 计算5日收益率标准差
    volatility = ts_std_dev(data['returns'], 5)
    
    # 2. 对波动率进行排名
    ranked_volatility = rank(volatility)
    
    # 3. 计算VWAP的3日变化
    vwap_lag3 = ts_delay(data['vwap'], 3)
    vwap_momentum = subtract(data['vwap'], vwap_lag3)
    
    # 4. 对VWAP动量进行排名
    ranked_momentum = rank(vwap_momentum)
    
    # 5. 计算波动率排名与动量排名的8日相关性
    vol_momentum_corr = ts_corr(ranked_volatility, ranked_momentum, 8)
    
    # 6. 对相关性进行12日线性衰减加权
    decayed_corr = ts_decay_linear(vol_momentum_corr, 12)
    
    # 7. 计算换手率的2日变化
    turnover_delta = ts_delta(data['turnover_ratio'], 2)
    
    # 8. 对换手率变化取平方根（保持符号）
    liquidity_shock = signed_power(turnover_delta, 0.5)
    
    # 9. 将衰减相关性与流动性冲击相乘
    combined_signal = multiply(decayed_corr, liquidity_shock)
    
    # 10. 计算10日时序排名
    factor = ts_rank(combined_signal, 10)
    
    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()