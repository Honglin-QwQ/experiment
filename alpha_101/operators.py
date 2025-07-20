import numpy as np
import pandas as pd

def log(x):
    if np.isscalar(x):
        return np.log(x)
    else:
        return np.log(x).sort_index()

def divide(s1, s2):
    result = s1 / s2
    if isinstance(result, pd.Series):
        return result.sort_index()
    else:
        return result

def arc_cos(x):
    if hasattr(x, 'index'):  # 检查是否为Series类型
        # 使用向量化操作
        result = x.copy()
        mask = (x >= -1) & (x <= 1)
        # 对于在有效范围内的值，使用numpy的arccos计算
        result[mask] = np.arccos(x[mask])
        # 对于范围外的值，设置为NaN
        result[~mask] = np.nan
        # 确保返回的Series包含正确的索引并排序
        return result.sort_index()
    else:  # 标量输入
        if -1 <= x <= 1:
            return np.arccos(x)
        else:
            return np.nan

def arc_tan(x):
    if hasattr(x, 'index') and hasattr(x, 'values'):
        # 向量化处理Series
        result = np.arctan(x)
        return result.sort_index()
    else:
        # 处理标量输入
        return np.arctan(x)

def sqrt(x):
    if isinstance(x, (float, int)):
        # 处理标量值
        if x >= 0:
            return np.sqrt(x)
        else:
            return float('nan')
    else:
        # 处理Series
        # 使用布尔索引直接处理负值
        result = x.copy()
        mask = x < 0
        result[~mask] = np.sqrt(x[~mask])
        result[mask] = float('nan')
        return result.sort_index()

def sigmoid(x):
    if hasattr(x, 'index'):  # 检查是否为Series类型
        # 处理数值溢出问题
        result = x.copy()
        
        # 处理NaN和无穷大值
        mask_large = x > 34
        mask_small = (x <= 34) & np.isfinite(x)
        
        # 对于x值过大的情况，直接设为1
        result[mask_large] = 1.0
        # 对于NaN或无穷大，保持原值
        # 对于x值过小的情况，使用exp计算
        safe_x = x[mask_small]
        result[mask_small] = 1.0 / (1.0 + np.exp(-safe_x))
        
        return result.sort_index()
    else:  # 处理标量输入
        # 处理NaN和无穷大值
        if not np.isfinite(x):
            return x  # 保持NaN或无穷大不变
        # 处理数值溢出
        if x > 34:  # 当x很大时，sigmoid接近1
            return 1.0
        else:
            return 1.0 / (1.0 + np.exp(-x))

def reverse(x):
    result = -x
    if hasattr(x, 'index'):
        return result.sort_index()
    return result

def adv(s, d = 10):
# 计算过去window天的平均日成交量,输入序列为'vol'
    d = int(d)
    return s.groupby('symbol').rolling(d).mean().droplevel(0).sort_index()

def ts_rank(s, d = 6, constant=0):
    d = int(d)
    constant = int(constant)
    def rolling_rank(x):
        if len(x) < d:
            return pd.Series([np.nan] * len(x), index = x.index)
        return x.rolling(d).rank()
    return s.groupby('symbol').transform(rolling_rank).sort_index()+constant

def ts_std_dev(x, d=6):
    d = int(d)
    return x.groupby('symbol').transform(
        lambda s: s.rolling(window=d).std().reindex(s.index)
    ).sort_index()

def signed_power(x, y):
    result = np.power(x, y)
    sign_x = np.sign(x)
    sign_result = np.sign(result)
    if isinstance(result, pd.Series):
        error = sign_x != sign_result
        result[error] = -result[error]
        return result.sort_index()
    else:
        if sign_x != sign_result:
            return -result
        else:
            return result

def rank(x, rate=2):
# Ranks the input among all the instruments and returns an equally distributed number between 0.0 and 1.0. For precise sort, use the rate as 0
    rate = int(rate)
    if rate == 2:
        return x.groupby('dt').rank(pct=True).sort_index()
    else:
        return x.groupby('dt').rank().sort_index()

def ts_delta(s, d = 2):
    d = int(d)
    return s.groupby('symbol').diff(d).sort_index()

def ts_corr(s1, s2, d = 6):
    d = int(d)
    s = pd.concat([s1, s2], axis = 1)
    s.columns = columns = ['s1', 's2']
    return s.reset_index().set_index('dt').groupby('symbol')[columns].rolling(d).corr().droplevel(2).iloc[::2, 1].sort_index()

def ts_covariance(s1, s2, d = 6):
    d = int(d)
    s = pd.concat([s1, s2], axis = 1)
    columns = s.columns
    return s.reset_index().set_index('dt').groupby('symbol')[columns].rolling(d).cov().droplevel(2).iloc[::2, 1].sort_index()

def ts_delay(s, d = 6):
    d = int(d)
    return s.groupby('symbol').shift(d).sort_index()

def ts_sum(s, d = 10):
    d = int(d)
    return s.groupby('symbol').rolling(d).sum().droplevel(0).sort_index()

def ts_min(s, d = 10):
    d = int(d)
    return s.groupby('symbol').rolling(d).min().droplevel(0).sort_index()

def ts_max(s, d = 10):
    d = int(d)
    return s.groupby('symbol').rolling(d).max().droplevel(0).sort_index()

def ts_scale(x, d = 6, constant=0):
    d = int(d)
    def rolling_scale(series):
        if len(series) < d:
            return pd.Series([np.nan] * len(series), index=series.index)
        min_x = series.rolling(d).min()
        max_x = series.rolling(d).max()
        return (series - min_x) / (max_x - min_x).replace(0, np.nan) + constant
    return x.groupby('symbol').transform(rolling_scale).sort_index()
    
def abs(x):
    if isinstance(x, pd.Series):
        return x.abs().sort_index()
    else:
        return np.abs(x)

def sign(x):
    if hasattr(x, 'index'):
        # 处理Series输入
        result = np.sign(x)
        return result.sort_index()
    else:
        # 处理标量输入
        if np.isnan(x):
            return np.nan
        return np.sign(x)

def exp(s):
    if isinstance(s, pd.Series):
        return s.apply(np.exp).sort_index()
    else:
        return np.exp(s)
    
def arc_sin(s):
    if isinstance(s, pd.Series):
        return s.transform(lambda x: np.arcsin(x) if -1 <= x <= 1 else float('NaN')).sort_index()
    else:
        return np.arcsin(s) if -1 <= s <= 1 else float('NaN')


def min(*args):
    if len(args) < 2:
        raise ValueError("At least 2 inputs are required")

    # 处理第一个参数
    result = args[0]

    # 逐个比较后续参数
    for arg in args[1:]:
        if hasattr(result, 'index') and hasattr(arg, 'index'):
            # 两个都是Series
            aligned_result, aligned_arg = result.align(arg, fill_value=float('-inf'))
            result = np.minimum(aligned_result, aligned_arg)
        elif hasattr(result, 'index'):
            # result是Series，arg是标量
            result = np.minimum(result, arg)
        elif hasattr(arg, 'index'):
            # arg是Series，result是标量
            result = np.minimum(arg, result)
        else:
            # 两个都是标量
            result = np.minimum(result, arg)

    # 处理分组逻辑
    if hasattr(result, 'index'):
        result = result.transform(lambda x: x)

    # 如果结果是Series，确保排序
    if hasattr(result, 'index'):
        return result.sort_index()
    return result
def max(*args):
    if len(args) < 2:
        raise ValueError("At least 2 inputs are required")
    
    # 处理第一个参数
    result = args[0]
    
    # 逐个比较后续参数
    for arg in args[1:]:
        if hasattr(result, 'index') and hasattr(arg, 'index'):
            # 两个都是Series
            aligned_result, aligned_arg = result.align(arg, fill_value=float('-inf'))
            result = np.maximum(aligned_result, aligned_arg)
        elif hasattr(result, 'index'):
            # result是Series，arg是标量
            result = np.maximum(result, arg)
        elif hasattr(arg, 'index'):
            # arg是Series，result是标量
            result = np.maximum(arg, result)
        else:
            # 两个都是标量
            result = np.maximum(result, arg)
    
    # 处理分组逻辑
    if hasattr(result, 'index'):
        result = result.transform(lambda x: x)
    
    # 如果结果是Series，确保排序
    if hasattr(result, 'index'):
        return result.sort_index()
    return result

def add(*args, filter = False):
    if filter:
        args = list(args)
        for i, arg in enumerate(args):
            if not isinstance(arg, pd.Series):
                args[i] = 0
            else:
                args[i] = arg.fillna(0)
    result = 0
    for s in args:
        result = result + s
    if isinstance(result, pd.Series):
        return result.sort_index()
    else:
        return result

def subtract(s1, s2, filter=False):
    if filter:
        if not isinstance(s1, pd.Series):
            s1 = 0
        else:
            s1 = s1.fillna(0)
        if not isinstance(s2, pd.Series):
            s2 = 0
        else:
            s2 = s2.fillna(0)
    result = s1 - s2
    if isinstance(result, pd.Series):
        return result.sort_index()
    else:
        return result
    
def multiply(*args, filter=False):
    if len(args) < 2:
        raise ValueError("At least 2 inputs are required for multiply.")
    
    if filter:
        args = list(args)
        for i, arg in enumerate(args):
            if not isinstance(arg, pd.Series):
                args[i] = 1
            else:
                args[i] = arg.fillna(1) 
    result = args[0]
    for s in args[1:]:
        result = result * s
    if isinstance(result, pd.Series):
        return result.sort_index()
    else:
        return result

def tanh(s):
    if hasattr(s, 'index'):
        return s.apply(np.tanh).sort_index()
    else:
        return np.tanh(s)

def round_down(s, f=1):
    f = float(f)
    def calculate_round_down(x):
        return (x // f) * f
    if isinstance(s, pd.Series):
        return s.transform(calculate_round_down).sort_index()
    else:
        return calculate_round_down(s)

def inverse(s):
    if isinstance(s, pd.Series):
        return (1 / s).sort_index()
    else:
        return 1 / s
    
def s_log_1p(s):
    s_arr = np.array([s]) if np.isscalar(s) else s.values if isinstance(s, pd.Series) else np.array(s)
    abs_s = np.abs(s_arr)
    log_abs = np.log(abs_s + 1)
    signed_log = np.sign(s) * log_abs
    result = signed_log / (1 + log_abs)
    if isinstance(s, pd.Series):
        return pd.Series(result, index=s.index)
    elif np.isscalar(s):
        return result.item()
    
def ts_arg_max(x, d=6):
    d = int(d)
    return (
        x.groupby('symbol')
        .transform(lambda s: s.rolling(window=d, min_periods=d)
            .apply(lambda w: (d - 1 - w.argmax()),raw=True))
        .sort_index()
    )

def ts_arg_min(x, d=5):
    d = int(d)
    return (
        x.groupby('symbol')
        .transform(lambda s: s.rolling(window=d, min_periods=d)
            .apply(lambda w: (d - 1 - w.argmin()),raw=True))
        .sort_index()
    )

def ts_decay_linear(s, d=6, dense=False):
    d = int(d)

    def rolling_decay(x):
        if len(x) < d:
            return np.nan  # 使用 np.nan
        weights = np.arange(d, 0, -1)
        if not dense:
            x = np.nan_to_num(x, nan=0.0) #用numpy替换fillna
        return np.sum(x * weights) / np.sum(weights)

    return s.groupby('symbol').transform(lambda x: x.rolling(d, min_periods=1).apply(rolling_decay, raw=True)).sort_index()

def ts_product(s, d = 5):
    d = int(d)
    return s.groupby('symbol').transform(lambda x: x.rolling(d, min_periods=d).apply(np.prod,raw=True)).sort_index()


def indneutralize(x, g):
    """
    按日期分组进行行业中性化，避免未来函数
    """
    df = pd.DataFrame({'x': x, 'g': g})

    # 按日期分组，每个日期内按行业中性化
    def neutralize_by_date(group):
        means = group.groupby('g')['x'].transform('mean')
        return group['x'] - means

    result = df.groupby(level='dt').apply(neutralize_by_date)
    return result.droplevel(0)