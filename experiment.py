import random
import sys
import time as time_module
from datetime import timedelta

path_dr = '/root/autodl-tmp'
base_compute_frequency = '12小时'
max_cor = 0.5
max_read = 5
mp_context = 'spawn'
num_process_2=6
num_process=12
chunksize_n=2
chunksize_m=100
sys.path.append(f"{path_dr}/experiment")
from operators import *

import matplotlib.pyplot as plt
import warnings
from backtest import WeightBacktest

import importlib

import logging


from tqdm import tqdm
from scipy.stats import spearmanr
import pandas as pd
import numpy as np
import multiprocessing
from multiprocessing import shared_memory
from concurrent.futures import ProcessPoolExecutor
import time as pytime
import os
import gc
import traceback
import uuid
from tqdm.auto import tqdm
from scipy import stats

warnings.filterwarnings('ignore')


plt.style.use('default')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

codes = ['SOLUSDT', 'XRPUSDT', 'BNBUSDT', "LTCUSDT", "AAVEUSDT", "LINKUSDT", "XLMUSDT", "DOGEUSDT",
         "BCHUSDT", "ADAUSDT", "AVAXUSDT", "ETCUSDT", "TRXUSDT", "FILUSDT", "BTCUSDT", "ETHUSDT"]


def resample_kline(df, target: str):
    """
    将1分钟K线数据重采样为更大周期的K线，使用固定的时间边界（向量化优化版本）

    参数:
    df: DataFrame, 包含1分钟K线数据，必须包含以下列：
       "symbol", "dt", "open", "close", "high", "low", "vol", "amount", "trades", "tbase", "tquote"
    target: str, 目标周期，支持 '15分钟', '30分钟', '1小时', '2小时', '4小时', '6小时', '8小时', '12小时', '日线'

    返回:
    DataFrame, 重采样后的K线数据
    """
    import pandas as pd
    import numpy as np
    from datetime import timedelta

    # 创建副本避免修改原始数据
    df_copy = df.copy()

    # 确保数据按时间排序
    df_copy = df_copy.sort_values(by=['symbol', 'dt'])

    # 确保dt列是datetime类型
    if not pd.api.types.is_datetime64_any_dtype(df_copy['dt']):
        df_copy['dt'] = pd.to_datetime(df_copy['dt'])

    # 如果需要调整时间，确保清楚为什么要减去1分钟
    df_copy['dt'] = df_copy['dt'] - timedelta(minutes=1)

    # 为VWAP计算添加price_volume列
    df_copy['price_volume'] = df_copy['close'] * df_copy['vol']

    # 向量化计算时间分组
    # 重要：将pandas Series转换为numpy array来避免索引错误
    dates = df_copy['dt'].dt.date.values
    hours = df_copy['dt'].dt.hour.values
    minutes = df_copy['dt'].dt.minute.values

    # 创建group_key列用于分组
    if target == '15分钟':
        # 创建分钟分组索引: 0-14->0, 15-29->1, 30-44->2, 45-59->3
        minute_group = np.floor(minutes / 15).astype(int)

        # 创建下一个时间点
        next_minutes = np.array([15, 30, 45, 0])[minute_group]
        next_hours = hours.copy()
        next_dates = [pd.Timestamp(d) for d in dates]  # 转换为Timestamp对象列表

        # 对于45-59分钟组修正时间和日期
        hour_adjust_mask = minute_group == 3
        next_hours[hour_adjust_mask] = (hours[hour_adjust_mask] + 1) % 24

        # 对23:45-23:59的情况，日期需要+1
        date_adjust_mask = (hour_adjust_mask) & (hours == 23)
        for i in np.where(date_adjust_mask)[0]:
            next_dates[i] = next_dates[i] + pd.Timedelta(days=1)

        # 格式化时间
        timestamps = []
        for i in range(len(df_copy)):
            hour_str = f"{next_hours[i]:02d}"
            minute_str = f"{next_minutes[i]:02d}"
            timestamps.append(f"{next_dates[i]} {hour_str}:{minute_str}:00")

        df_copy['group_key'] = pd.to_datetime(timestamps)

    elif target == '30分钟':
        # 创建分钟分组索引: 0-29->0, 30-59->1
        minute_group = np.floor(minutes / 30).astype(int)

        # 创建下一个时间点
        next_minutes = np.array([30, 0])[minute_group]
        next_hours = hours.copy()
        next_dates = [pd.Timestamp(d) for d in dates]

        # 对于30-59分钟组修正时间和日期
        hour_adjust_mask = minute_group == 1
        next_hours[hour_adjust_mask] = (hours[hour_adjust_mask] + 1) % 24

        # 对23:30-23:59的情况，日期需要+1
        date_adjust_mask = (hour_adjust_mask) & (hours == 23)
        for i in np.where(date_adjust_mask)[0]:
            next_dates[i] = next_dates[i] + pd.Timedelta(days=1)

        # 格式化时间
        timestamps = []
        for i in range(len(df_copy)):
            hour_str = f"{next_hours[i]:02d}"
            minute_str = f"{next_minutes[i]:02d}"
            timestamps.append(f"{next_dates[i]} {hour_str}:{minute_str}:00")

        df_copy['group_key'] = pd.to_datetime(timestamps)

    elif target == '1小时':
        # 对于1小时，直接计算下一个整点时间
        next_hours = (hours + 1) % 24
        next_dates = [pd.Timestamp(d) for d in dates]

        # 对23点的K线，日期需要加1
        date_adjust_mask = hours == 23
        for i in np.where(date_adjust_mask)[0]:
            next_dates[i] = next_dates[i] + pd.Timedelta(days=1)

        # 格式化时间
        timestamps = []
        for i in range(len(df_copy)):
            hour_str = f"{next_hours[i]:02d}"
            timestamps.append(f"{next_dates[i]} {hour_str}:00:00")

        df_copy['group_key'] = pd.to_datetime(timestamps)

    elif target == '2小时':
        # 计算所在的2小时段并找到下一个2小时段的开始时间
        hour_group = (hours // 2) * 2
        next_2hours = (hour_group + 2) % 24
        next_dates = [pd.Timestamp(d) for d in dates]

        # 对于22-23点的K线，日期需要加1
        date_adjust_mask = hour_group == 22
        for i in np.where(date_adjust_mask)[0]:
            next_dates[i] = next_dates[i] + pd.Timedelta(days=1)

        # 格式化时间
        timestamps = []
        for i in range(len(df_copy)):
            hour_str = f"{next_2hours[i]:02d}"
            timestamps.append(f"{next_dates[i]} {hour_str}:00:00")

        df_copy['group_key'] = pd.to_datetime(timestamps)

    elif target == '4小时':
        # 对于4小时，我们可以将一天分为6个时段: 0-3, 4-7, 8-11, 12-15, 16-19, 20-23
        hour_group_index = hours // 4
        next_4hours_array = np.array([4, 8, 12, 16, 20, 0])
        next_4hours = np.zeros(len(hours), dtype=int)

        # 使用numpy索引而不是pandas索引
        for i in range(len(hours)):
            idx = hour_group_index[i]
            if idx < len(next_4hours_array):  # 确保索引有效
                next_4hours[i] = next_4hours_array[idx]

        next_dates = [pd.Timestamp(d) for d in dates]

        # 对于20-23点的K线，日期需要加1
        date_adjust_mask = (hours >= 20) & (hours <= 23)
        for i in np.where(date_adjust_mask)[0]:
            next_dates[i] = next_dates[i] + pd.Timedelta(days=1)

        # 格式化时间
        timestamps = []
        for i in range(len(df_copy)):
            hour_str = f"{next_4hours[i]:02d}"
            timestamps.append(f"{next_dates[i]} {hour_str}:00:00")

        df_copy['group_key'] = pd.to_datetime(timestamps)

    elif target == '6小时':
        # 对于6小时，我们可以将一天分为4个时段: 0-5, 6-11, 12-17, 18-23
        hour_group_index = hours // 6  # 这是numpy数组，可以直接用于索引
        next_6hours_array = np.array([6, 12, 18, 0])
        next_6hours = np.zeros(len(hours), dtype=int)

        for i in range(len(hours)):
            idx = hour_group_index[i]
            if idx < len(next_6hours_array):  # 确保索引有效
                next_6hours[i] = next_6hours_array[idx]

        next_dates = [pd.Timestamp(d) for d in dates]

        # 对于18-23点的K线，日期需要加1
        date_adjust_mask = (hours >= 18) & (hours <= 23)
        for i in np.where(date_adjust_mask)[0]:
            next_dates[i] = next_dates[i] + pd.Timedelta(days=1)

        # 格式化时间
        timestamps = []
        for i in range(len(df_copy)):
            hour_str = f"{next_6hours[i]:02d}"
            timestamps.append(f"{next_dates[i]} {hour_str}:00:00")

        df_copy['group_key'] = pd.to_datetime(timestamps)

    elif target == '8小时':
        # 对于8小时，我们可以将一天分为3个时段: 0-7, 8-15, 16-23
        hour_group_index = hours // 8
        next_8hours_array = np.array([8, 16, 0])
        next_8hours = np.zeros(len(hours), dtype=int)

        for i in range(len(hours)):
            idx = hour_group_index[i]
            if idx < len(next_8hours_array):
                next_8hours[i] = next_8hours_array[idx]

        next_dates = [pd.Timestamp(d) for d in dates]

        # 对于16-23点的K线，日期需要加1
        date_adjust_mask = (hours >= 16) & (hours <= 23)
        for i in np.where(date_adjust_mask)[0]:
            next_dates[i] = next_dates[i] + pd.Timedelta(days=1)

        # 格式化时间
        timestamps = []
        for i in range(len(df_copy)):
            hour_str = f"{next_8hours[i]:02d}"
            timestamps.append(f"{next_dates[i]} {hour_str}:00:00")

        df_copy['group_key'] = pd.to_datetime(timestamps)

    elif target == '12小时':
        # 对于12小时，我们可以将一天分为2个时段: 0-11, 12-23
        hour_group_index = hours // 12
        next_12hours_array = np.array([12, 0])
        next_12hours = np.zeros(len(hours), dtype=int)

        for i in range(len(hours)):
            idx = hour_group_index[i]
            if idx < len(next_12hours_array):
                next_12hours[i] = next_12hours_array[idx]

        next_dates = [pd.Timestamp(d) for d in dates]

        # 对于12-23点的K线，日期需要加1
        date_adjust_mask = (hours >= 12) & (hours <= 23)
        for i in np.where(date_adjust_mask)[0]:
            next_dates[i] = next_dates[i] + pd.Timedelta(days=1)

        # 格式化时间
        timestamps = []
        for i in range(len(df_copy)):
            hour_str = f"{next_12hours[i]:02d}"
            timestamps.append(f"{next_dates[i]} {hour_str}:00:00")

        df_copy['group_key'] = pd.to_datetime(timestamps)

    elif target == '日线':
        # 对于日线，结束时间为次日00:00
        next_dates = [pd.Timestamp(d) + pd.Timedelta(days=1) for d in dates]

        # 格式化时间
        timestamps = []
        for i in range(len(df_copy)):
            timestamps.append(f"{next_dates[i]} 00:00:00")

        df_copy['group_key'] = pd.to_datetime(timestamps)

    else:
        raise ValueError(f"不支持的目标周期: {target}")

    # 按symbol和组标识进行聚合
    resampled = df_copy.groupby(['symbol', 'group_key']).agg({
        'dt': 'last',  # 取每组最后一个时间点作为K线时间点
        'open': 'first',  # 取每组第一个开盘价
        'high': 'max',  # 取每组最高价
        'low': 'min',  # 取每组最低价
        'close': 'last',  # 取每组最后一个收盘价
        'vol': 'sum',  # 成交量求和
        'amount': 'sum',  # 成交额求和
        'trades': 'sum',  # 成交笔数求和
        'tbase': 'sum',  # 基础资产成交量求和
        'tquote': 'sum',  # 报价资产成交量求和
        'price_volume': 'sum'  # 价格乘以成交量之和，用于计算VWAP
    }).reset_index()

    # 向量化计算VWAP (成交量加权平均价格)
    mask = resampled['vol'] > 0
    resampled['vwap'] = np.nan  # 默认为NaN
    resampled.loc[mask, 'vwap'] = resampled.loc[mask, 'price_volume'] / resampled.loc[mask, 'vol']
    if resampled['dt'].iloc[-1]+timedelta(minutes=1)<resampled['group_key'].iloc[-1]:
        resampled=resampled[:-1]


    # 使用group_key作为最终的dt
    resampled['dt'] = resampled['group_key']

    # 删除不需要的列
    resampled = resampled.drop(['group_key', 'price_volume'], axis=1)

    return resampled
def get_factor_returns(arg):
    """
    Vectorized version of get_factor_returns function.

    Parameters:
    arg : tuple
        Contains (values, factor, date_symbol_index)

    Returns:
    pd.DataFrame
        DataFrame with factor returns
    """
    import pandas as pd

    df, factor, date_symbol_index = arg

    # 使用向量化操作处理，不需要复制整个DataFrame
    # 只创建必要的Series和计算
    values = df[factor]
    # 创建返回计算时需要的数据
    returns = values * df['target_1'].values

    # 创建一个包含日期、股票和返回值的临时DataFrame
    # 这样可以避免复制整个shared_df
    temp_df = pd.DataFrame({
        'date': df['date'].values,
        'symbol': df['symbol'].values,
        'return': returns
    })

    # 使用DataFrame的向量化聚合函数
    # 按日期和股票分组求和
    daily_symbol_returns = temp_df.groupby(['date', 'symbol'])['return'].sum()

    # 重新索引，将缺失值填充为0
    complete_daily_returns = daily_symbol_returns.reindex(date_symbol_index, fill_value=0)

    # 按日期分组计算平均收益（向量化操作）
    factor_returns = complete_daily_returns.groupby('date').mean()

    # 创建结果DataFrame
    factor_df = pd.DataFrame({factor: factor_returns})

    return factor_df


def calculate_block_size(total_columns, base_memory_percentage, current_frequency,
                         base_frequency=base_compute_frequency):
    """
    根据当前频率和基础内存使用情况计算最优块大小

    Args:
        total_columns (int): 总列数
        base_memory_percentage (float): 基础内存使用百分比（基于4小时频率）
        current_frequency (str): 当前频率 ('4小时', '60分钟', '30分钟', '15分钟')
        base_frequency (str): 基础频率

    Returns:
        int: 建议的列块大小
    """
    # 频率到行数比例映射
    frequency_multiplier = {
        '12小时': 1,
        '8小时': 2,
        '4小时': 6,
        '6小时': 6,
        '2小时': 8,
        '1小时': 16,
        '30分钟': 32
    }

    # 计算频率系数
    freq_factor = frequency_multiplier.get(current_frequency, 1) / frequency_multiplier.get(base_frequency, 1)

    # 计算内存使用系数（当前内存使用率越高，块越小）
    memory_factor = base_memory_percentage

    # 计算总体系数 (频率因素 * 内存因素)
    combined_factor = freq_factor * memory_factor

    # 基础块大小（如果内存和频率都理想，使用较大块）
    base_block_size = max(200, total_columns)

    # 计算块大小，确保至少5列每块，且不超过原始列数
    block_size = max(5, min(total_columns, int(base_block_size / combined_factor)))

    return block_size


def split_columns_into_blocks(columns, base_memory_percentage=0.65, current_frequency='4小时'):
    """
    将列分成块以管理内存使用

    Args:
        columns (list): 列名列表
        base_memory_percentage (float): 基础内存使用百分比
        current_frequency (str): 当前频率

    Returns:
        list: 列块列表
    """
    total_columns = len(columns)

    # 计算块大小
    block_size = calculate_block_size(
        total_columns,
        base_memory_percentage,
        current_frequency
    )

    # 创建列块
    column_blocks = [columns[i:i + block_size] for i in range(0, total_columns, block_size)]

    print(
        f"将{total_columns}列分成{len(column_blocks)}块，每块约{block_size}列")

    return column_blocks


def process_features(df: pd.DataFrame) -> pd.DataFrame:
    """处理特征工程的主函数

    Args:
        df: 输入的DataFrame，包含价格和交易量数据

    Returns:
        添加了所有特征的DataFrame
    """
    logger.info("开始特征工程处理")

    # 确保数据按日期排序
    df = df.sort_values(['symbol', 'dt']).reset_index(drop=True)

    def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
        """计算不同时间窗口的收益率"""
        # 确保按日期排序
        df = df.sort_values(['symbol', 'dt']).reset_index(drop=True)

        # 计算不同时间窗口的收益率
        for lag in [1, 2, 3, 6, 9, 12]:
            df[f'F#return_{lag}'] = df.groupby('symbol')['close'].pct_change(lag)

        # 去除异常值
        outlier_cutoff = 0.01
        for col in [f'F#return_{lag}' for lag in [1, 2, 3, 6, 9, 12]]:
            q_low = df[col].quantile(outlier_cutoff)
            q_high = df[col].quantile(1 - outlier_cutoff)
            df[col] = df[col].clip(lower=q_low, upper=q_high)

        # 计算规范化的收益率（几何平均）
        for lag in [2, 3, 6, 9, 12]:
            df[f'F#norm_return_{lag}'] = (df[f'F#return_{lag}'] + 1) ** (1 / lag) - 1

        return df

    # 1. 计算收益率
    # logger.info("计算收益率特征")
    df = calculate_returns(df)

    def calculate_momentum_factors(df: pd.DataFrame) -> pd.DataFrame:
        """计算动量因子"""
        # 计算不同时间窗口的动量因子
        for lag in [2, 3, 6, 9, 12]:
            df[f'F#momentum_{lag}'] = df[f'F#return_{lag}'] - df['F#return_1']

        # 计算3个月和12个月收益率差异
        df['F#momentum_3_12'] = df['F#return_12'] - df['F#return_3']

        return df

    # 2. 计算动量因子
    # logger.info("计算动量因子")
    df = calculate_momentum_factors(df)

    def calculate_volatility_factors(df: pd.DataFrame) -> pd.DataFrame:
        """计算波动率因子"""
        # 计算不同时间窗口的波动率
        for window in [5, 10, 20, 30]:
            # 计算收盘价的滚动标准差
            df[f'F#volatility_{window}'] = df.groupby('symbol')['close'].transform(
                lambda x: x.pct_change().rolling(window=window).std()
            )

            # 计算交易量的滚动标准差
            df[f'F#vol_volatility_{window}'] = df.groupby('symbol')['vol'].transform(
                lambda x: x.rolling(window=window).std() / x.rolling(window=window).mean()
            )

        return df

    # 3. 计算波动率因子
    # logger.info("计算波动率因子")
    df = calculate_volatility_factors(df)

    def calculate_technical_factors(df: pd.DataFrame) -> pd.DataFrame:
        """计算技术指标因子"""
        # RSI
        for window in [6, 14, 20]:
            delta = df.groupby('symbol')['close'].diff()
            gain = delta.where(delta > 0, 0).groupby(df['symbol']).rolling(window=window).mean().reset_index(0,
                                                                                                             drop=True)
            loss = -delta.where(delta < 0, 0).groupby(df['symbol']).rolling(window=window).mean().reset_index(0,
                                                                                                              drop=True)
            rs = gain / loss
            df[f'F#rsi_{window}'] = 100 - (100 / (1 + rs))

        # MACD
        df['F#ema_12'] = df.groupby('symbol')['close'].transform(lambda x: x.ewm(span=12, adjust=False).mean())
        df['F#ema_26'] = df.groupby('symbol')['close'].transform(lambda x: x.ewm(span=26, adjust=False).mean())
        df['F#macd_line'] = df['F#ema_12'] - df['F#ema_26']
        df['F#macd_signal'] = df.groupby('symbol')['F#macd_line'].transform(
            lambda x: x.ewm(span=9, adjust=False).mean())
        df['F#macd_histogram'] = df['F#macd_line'] - df['F#macd_signal']

        # 布林带
        for window in [20, 40]:
            rolling_mean = df.groupby('symbol')['close'].transform(lambda x: x.rolling(window=window).mean())
            rolling_std = df.groupby('symbol')['close'].transform(lambda x: x.rolling(window=window).std())
            df[f'F#bb_upper_{window}'] = rolling_mean + (rolling_std * 2)
            df[f'F#bb_lower_{window}'] = rolling_mean - (rolling_std * 2)
            df[f'F#bb_width_{window}'] = (df[f'F#bb_upper_{window}'] - df[f'F#bb_lower_{window}']) / rolling_mean
            df[f'F#bb_position_{window}'] = (df['close'] - df[f'F#bb_lower_{window}']) / (
                    df[f'F#bb_upper_{window}'] - df[f'F#bb_lower_{window}'])

        # 删除中间变量
        df = df.drop(columns=['F#ema_12', 'F#ema_26'], errors='ignore')

        return df

    # 4. 计算技术指标
    # logger.info("计算技术指标因子")
    df = calculate_technical_factors(df)

    def calculate_volume_factors(df: pd.DataFrame) -> pd.DataFrame:
        """计算交易量相关因子"""
        # OBV (On-Balance Volume)
        df['F#price_change'] = df.groupby('symbol')['close'].pct_change()
        df['F#obv_signal'] = np.where(df['F#price_change'] > 0, 1, np.where(df['F#price_change'] < 0, -1, 0))

        # 修复OBV计算
        for symbol, group in df.groupby('symbol'):
            df.loc[group.index, 'F#obv'] = (group['F#obv_signal'] * group['vol']).cumsum()

        # 相对交易量
        for window in [5, 10, 20]:
            df[f'F#rel_vol_{window}'] = df.groupby('symbol')['vol'].transform(
                lambda x: x / x.rolling(window=window).mean()
            )

        # Chaikin Money Flow
        df['F#mf_multiplier'] = ((df['close'] - df['low']) - (df['high'] - df['close'])) / (df['high'] - df['low'])
        df['F#money_flow_volume'] = df['F#mf_multiplier'] * df['vol']

        # 修复CMF计算
        for window in [10, 20]:
            for symbol, group in df.groupby('symbol'):
                mfv_sum = group['F#money_flow_volume'].rolling(window=window).sum()
                vol_sum = group['vol'].rolling(window=window).sum()
                df.loc[group.index, f'F#cmf_{window}'] = mfv_sum / vol_sum

        # 主动交易因子
        df['F#taker_buy_ratio'] = df['tbase'] / (df['vol'] + 1e-9)  # 避免除以零
        df['F#taker_buy_amount_ratio'] = df['tquote'] / (df['amount'] + 1e-9)  # 避免除以零

        # 删除中间变量
        df = df.drop(columns=['F#price_change', 'F#obv_signal', 'F#mf_multiplier', 'F#money_flow_volume'],
                     errors='ignore')

        return df

    # 5. 计算交易量因子
    # logger.info("计算交易量因子")
    df = calculate_volume_factors(df)

    def calculate_lagged_features(df: pd.DataFrame) -> pd.DataFrame:
        """添加滞后特征"""
        # 添加价格滞后特征
        for t in range(1, 7):
            df[f'F#close_t-{t}'] = df.groupby('symbol')['close'].shift(t)
            df[f'F#return_1_t-{t}'] = df.groupby('symbol')['F#return_1'].shift(t)

        # 添加交易量滞后特征
        for t in range(1, 4):
            df[f'F#vol_t-{t}'] = df.groupby('symbol')['vol'].shift(t)

        return df

    # 6. 添加滞后特征
    # logger.info("添加滞后特征")
    df = calculate_lagged_features(df)

    # # 7. 计算滚动因子贝塔
    # logger.info("计算滚动因子贝塔")
    # df = calculate_rolling_factor_betas(df)
    def create_target_variables(df: pd.DataFrame) -> pd.DataFrame:
        """创建目标变量(未来收益率)

        Args:

            df: 输入的DataFrame

        Returns:
            添加了目标变量的DataFrame
        """
        # 创建未来不同周期的收益率作为目标变量
        for symbol, dfg in df.groupby("symbol"):

            for n in [1, 2, 3, 5, 8, 10, 13]:
                dfg[f'target_{n}'] = dfg["close"].shift(-n) / dfg["close"] - 1
                df.loc[dfg.index, f'target_{n}'] = dfg[f'target_{n}'].fillna(0)

        return df

    # 8. 创建目标变量
    # logger.info("创建目标变量")
    df = create_target_variables(df)

    return df


def process_single_factor(args):
    """
    处理单个因子函数的并行处理函数

    Args:
        args (tuple): (filename, df_subset)，包含文件名和数据子集

    Returns:
        tuple: (filename, processed_df) 或在出错时 (filename, None, error_message)
    """
    df_subset, filename, yinzi = args
    function_name = filename[:-3]

    try:
        # 动态导入模块

        # module_path = f"examples.Streamlit.factor_function_{yinzi}.{function_name}"
        module_path = f"factor_function_{yinzi}.{function_name}"
        module = importlib.import_module(module_path)

        # 获取并执行同名函数
        if hasattr(module, function_name):
            func = getattr(module, function_name)
            processed_df = func(df_subset)

            return filename, processed_df, None
        else:
            return filename, None, f"函数 {function_name} 未在模块中找到"
    except Exception as e:
        error_message = f"执行函数 {function_name} 出错: {str(e)}"
        return filename, None, error_message


# --- Helper: NumPy Layering (Corrected) ---
def _feature_cross_layering_np_mimic(
        dt_ids: np.ndarray,
        factor_values: np.ndarray,
        n_layers: int,
        use_qcut_logic: bool,
        global_unique_factor_values_sorted: np.ndarray = None
):
    """
    Internal NumPy implementation MIMICKING the original Pandas feature_cross_layering.
    Applies either quantile-based or global-rank-based layering based on the flag.
    Output layers are integers: -1 for NaN, 0 to n_layers-1 otherwise.
    """
    layer_col = np.full(factor_values.shape, -1, dtype=np.int8)
    is_nan_factor = np.isnan(factor_values)

    global_value_to_rank = None
    if not use_qcut_logic:
        if global_unique_factor_values_sorted is None:
            raise ValueError("global_unique_factor_values_sorted required when use_qcut_logic=False")
        # Ranks are 0 to len(uniques)-1, which is <= n_layers-1
        global_value_to_rank = {
            val: rank for rank, val in enumerate(global_unique_factor_values_sorted)
        }

    # Efficiently process by date without explicit pandas groupby
    unique_dts, dt_indices, dt_inverse = np.unique(
        dt_ids, return_index=True, return_inverse=True
    )

    for i, dt_val in enumerate(unique_dts):
        dt_mask = (dt_inverse == i)
        current_factors = factor_values[dt_mask]
        current_is_nan = is_nan_factor[dt_mask]

        valid_factors = current_factors[~current_is_nan]
        # Get the original indices within the full array corresponding to valid_factors for this dt
        original_indices_for_valid = np.where(dt_mask)[0][~current_is_nan]

        if len(valid_factors) == 0:
            continue  # Skip date if no valid factors, layer_col remains -1

        group_layers_valid = np.full(len(valid_factors), -1, dtype=np.int8)  # Layers only for valid factors

        if use_qcut_logic:
            # --- Quantile Logic (Mimic pd.qcut within date group) ---
            try:
                # Need unique values *within the group* for qcut
                unique_valid_factors = np.unique(valid_factors)
                if len(unique_valid_factors) > 1:
                    quantiles = np.linspace(0, 1, n_layers + 1)
                    # Use nanquantile on the valid factors of the group
                    bins = np.nanquantile(valid_factors, quantiles)
                    bins = np.unique(bins)  # Mimics duplicates='drop'

                    if len(bins) < 2:  # Not enough distinct bins possible
                        group_layers_valid[:] = 0  # Assign all to layer 0
                    else:
                        # layers are 0 to n_layers-1
                        group_layers_valid = np.digitize(
                            valid_factors, bins[1:], right=False  # layers 0 to len(bins)-2
                        ).astype(np.int8)
                        # Ensure layers don't exceed n_layers-1 if bins were reduced
                        group_layers_valid = np.clip(group_layers_valid, 0, n_layers - 1)
                elif len(valid_factors) > 0:  # Only one unique value in the group
                    group_layers_valid[:] = 0  # Assign all to layer 0
                # else: No valid factors, group_layers_valid remains empty / unused

            except Exception as qcut_err:
                # Fallback: Assign 0 if qcut fails within the group
                # print(f"Warning: Quantile layering failed dt {dt_val} for factor: {qcut_err}. Assigning 0.")
                if len(valid_factors) > 0:
                    group_layers_valid[:] = 0
        else:
            # --- Global Rank Logic (Mimic sorted_x.index(x)) ---
            if global_value_to_rank is not None and len(valid_factors) > 0:
                # Map each valid factor to its rank (0 to k-1, where k <= n_layers)
                group_layers_valid = np.array(
                    [global_value_to_rank.get(val, -1) for val in valid_factors],
                    dtype=np.int8
                )
                # Handle potential misses (shouldn't happen ideally)
                missing_mask = group_layers_valid == -1
                if np.any(missing_mask):
                    # print(f"Warning: Factor value in dt {dt_val} not in global uniques (<=n). Assigning 0.")
                    group_layers_valid[missing_mask] = 0  # Assign 0 if missing

        # Place the calculated layers back into the correct positions in the main layer_col
        if len(valid_factors) > 0:
            layer_col[original_indices_for_valid] = group_layers_valid

    return layer_col


# --- Helper: NumPy Auto Reverse (Corrected Logic for Edge Cases) ---
def _auto_reverse_np_mimic(dt_ids: np.ndarray,
                           factor_values: np.ndarray,
                           target_values: np.ndarray,
                           x_col: str,  # Keep for potential debugging messages
                           n_layers: int = 5):
    """
    NumPy implementation mimicking the core logic of the original Pandas auto_reverse.
    Includes corrections for all-NaN and single-unique-value factors.
    """
    valid_factor_mask = ~np.isnan(factor_values)

    # --- Correction 1 & 2: Handle All-NaN and Single Unique Value Cases ---
    # Check unique values *only* among non-NaNs
    valid_factors_only = factor_values[valid_factor_mask]
    if len(valid_factors_only) == 0:  # Factor is all NaN
        return 0  # Drop (Matches Pandas behavior)

    global_unique_values = np.unique(valid_factors_only)
    global_nunique = len(global_unique_values)

    if global_nunique <= 1:  # Factor has only one unique value (or was all NaN)
        return 0  # Drop (Matches Pandas behavior)
    # --- End Corrections ---

    # Decide layering strategy (as before)
    use_qcut_logic = (global_nunique > n_layers)
    global_unique_sorted = None
    if not use_qcut_logic:
        global_unique_sorted = global_unique_values  # Already sorted by np.unique

    # --- 1. Perform Layering ---
    layer_ids = _feature_cross_layering_np_mimic(
        dt_ids, factor_values, n_layers, use_qcut_logic, global_unique_sorted
    )  # Output: -1 for NaNs, 0 to n-1 for layers (int8)

    # --- 2. Filter Target and Layers ---
    valid_target_mask = ~np.isnan(target_values)
    # Combine masks: need valid target AND valid layer (0 to n-1) for grouping
    combined_mask = valid_target_mask & (layer_ids != -1)

    if not np.any(combined_mask):
        # If no data points have both a valid target and a valid layer assignment,
        # we cannot calculate monotonicity. Pandas would likely result in sum=0 -> drop.
        return 0  # Drop

    dt_ids_final = dt_ids[combined_mask]
    layer_ids_final = layer_ids[combined_mask]  # Layers are 0 to n-1
    target_values_final = target_values[combined_mask]

    if len(dt_ids_final) == 0:  # Double check after masking
        return 0  # Drop

    # --- 3. Group by (dt, layer) and calculate mean target ---
    try:
        # Use float64 for sums/means to avoid potential overflow/precision issues
        target_values_final = target_values_final.astype(np.float64)

        # Create composite keys (dt_id, layer_id)
        # Use a stable approach for unique rows
        composite_data = np.stack([dt_ids_final, layer_ids_final], axis=1)
        # Using lexsort provides indices to reconstruct the sorted order if needed,
        # but np.unique with axis=0 is often sufficient and clearer here.
        composite_keys, group_indices = np.unique(
            composite_data, axis=0, return_inverse=True
        )
        # composite_keys is now shape (num_unique_groups, 2) -> [[dt_id, layer_id], ...]
        # group_indices maps each row in target_values_final back to its group index

        # Calculate sum and count per group using bincount
        target_sums = np.bincount(group_indices, weights=target_values_final)  # Sum of targets for each group
        group_counts = np.bincount(group_indices)  # Count of items in each group

        # Calculate mean, avoiding division by zero
        group_means = np.full(len(target_sums), np.nan, dtype=np.float64)
        valid_counts_mask = group_counts > 0
        group_means[valid_counts_mask] = target_sums[valid_counts_mask] / group_counts[valid_counts_mask]

    except Exception as group_err:
        # print(f"Error during grouping/mean calculation for {x_col}: {group_err}")
        return 1  # Keep on calculation error (safer than dropping potentially good factor)

    # --- 4. Aggregate Means by Layer (Mimic Pivot + Sum) ---
    # Extract layer IDs corresponding to each calculated group mean
    layers_in_unique_groups = composite_keys[:, 1].astype(int)  # Layer IDs (0 to n-1)

    # Filter out any groups where mean calculation resulted in NaN (shouldn't happen with float64 target)
    valid_means_mask = np.isfinite(group_means)
    if not np.any(valid_means_mask):
        # If all group means are somehow NaN, cannot calculate monotonicity
        return 0  # Drop

    layers_for_valid_means = layers_in_unique_groups[valid_means_mask]
    valid_group_means = group_means[valid_means_mask]

    # Sum the valid group means for each layer (0 to n-1)
    # `minlength=n_layers` ensures the output array has size n_layers,
    # with layers having no contribution summing to 0 (matches fillna(0))
    total_mean_sum_by_layer = np.bincount(
        layers_for_valid_means,
        weights=valid_group_means,
        minlength=n_layers
    )  # Shape: (n_layers,)

    # --- 5. Calculate Monotonicity ---
    # The monotonicity function itself is assumed to be correct and consistent
    m = monotonicity(total_mean_sum_by_layer)

    # --- 6. Decide action (Identical logic to Pandas) ---
    if abs(m) < 0.8:
        return 0  # Drop
    elif m < 0:
        return -1  # Reverse
    else:  # m >= 0.8
        return 1  # Keep


# --- Your `monotonicity` Function (Using SciPy) - No changes needed ---
def monotonicity(sequence):
    """计算序列的单调性 (using SciPy/NumPy)"""
    seq_array = np.asarray(sequence)
    # Ensure input is treated as float for isnan checks if it's integer
    seq_array = seq_array.astype(float)
    seq_array = seq_array[np.isfinite(seq_array)]  # Filter NaNs and Infs
    if len(seq_array) < 2:
        return 0.0
    # Check for constant sequence *after* filtering NaNs
    # Use tolerance for float comparison
    if np.allclose(seq_array, seq_array[0]):
        return 0.0
    try:
        # Calculate Spearman correlation
        m, p_value = spearmanr(seq_array, range(len(seq_array)))
        # Handle potential NaN result from spearmanr itself
        return m if np.isfinite(m) else 0.0
    except ValueError:  # Handle other errors from spearmanr
        return 0.0


# --- Worker Function (Reads SHM, calls NumPy logic) ---
def process_auto_reverse_optimized_shm(item):
    """
    Worker function using Shared Memory. Reads data, calls NumPy mimic logic.
    """
    (
        shm_dt_name, shm_target_name, shm_factors_name,
        shm_dt_shape, shm_dt_dtype,
        shm_target_shape, shm_target_dtype,
        shm_factors_shape, shm_factors_dtype,
        factor_col_idx_in_block, factor_col_name, n_layers
    ) = item

    shm_dt = shm_target = shm_factors = None
    array_dt = array_target = array_factors = None

    try:
        # Attach to SHM
        shm_dt = shared_memory.SharedMemory(name=shm_dt_name)
        array_dt = np.ndarray(shm_dt_shape, dtype=shm_dt_dtype, buffer=shm_dt.buf)
        shm_target = shared_memory.SharedMemory(name=shm_target_name)
        array_target = np.ndarray(shm_target_shape, dtype=shm_target_dtype, buffer=shm_target.buf)
        shm_factors = shared_memory.SharedMemory(name=shm_factors_name)
        array_factors = np.ndarray(shm_factors_shape, dtype=shm_factors_dtype, buffer=shm_factors.buf)

        # Select specific factor data column
        # Use a copy to avoid potential read-write conflicts if logic were more complex,
        # though it's likely read-only here. Better safe than sorry with SHM.
        factor_data = array_factors[:, factor_col_idx_in_block].copy()

        # Call the NumPy mimic logic
        values = _auto_reverse_np_mimic(
            dt_ids=array_dt,  # Pass dt IDs directly
            factor_values=factor_data,
            target_values=array_target,  # Pass target values directly
            x_col=factor_col_name,
            n_layers=n_layers
        )

        if values not in [0, -1, 1]:
            print(f"Warning: Unexpected result {values} for factor {factor_col_name}. Defaulting to 1 (keep).")
            values = 1
        return values, factor_col_name

    except FileNotFoundError:
        print(f"Error: SHM block not found in worker for {factor_col_name}.")
        # Decide error handling: Keep (1) or Drop (0)? Keep is safer default.
        return 1, factor_col_name
    except Exception as e:
        print(f"Error processing factor {factor_col_name} in worker: {type(e).__name__} - {e}")
        traceback.print_exc()  # Print full traceback for worker errors
        return 1, factor_col_name  # Keep on error
    finally:
        # Clean up SHM handles in worker
        if shm_dt: shm_dt.close()
        if shm_target: shm_target.close()
        if shm_factors: shm_factors.close()
        # Explicitly delete numpy array views to release buffer reference
        del array_dt, array_target, array_factors, factor_data
        # gc.collect() # Usually not necessary in worker process unless large intermediate objects created


# --- Main Blocking Function (SHM, Integer Index Input) ---
def process_auto_reverse_blocked(result_df, n_jobs,
                                 current_frequency='4小时',  # Still used by split_columns_into_blocks
                                 time=pd.to_datetime('2024-01-01')):  # Default time updated
    """
    分块处理因子自动反转 (Shared Memory version).
    Assumes result_df has an integer index and 'dt', 'target_1' columns.

    Args:
        result_df (pd.DataFrame): Input DataFrame with integer index.
        n_jobs (int): Number of parallel processes.
        current_frequency (str): Frequency string for block splitting logic.
        time (pd.Timestamp or str): Filter data up to this time (inclusive).

    Returns:
        pd.DataFrame: Processed DataFrame with integer index.
    """
    if not isinstance(time, pd.Timestamp):
        time = pd.to_datetime(time)

    print(f"Starting auto-reverse process (Shared Memory, Target Time: {time}).")
    start_time = pytime.time()

    # --- 1. Initial Setup & Validation ---
    required_base_cols = ['dt', 'target_1']  # 'symbol' not strictly needed for this logic
    factor_cols = sorted([col for col in result_df.columns if col.startswith('F#')])

    if not factor_cols:
        print("No factor columns (starting with 'F#') found.")
        return result_df

    required_cols = required_base_cols + factor_cols
    missing_cols = [col for col in required_cols if col not in result_df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in result_df: {missing_cols}")

    # Ensure dt is datetime type
    if not pd.api.types.is_datetime64_any_dtype(result_df['dt']):
        try:
            result_df['dt'] = pd.to_datetime(result_df['dt'])
        except Exception as e:
            raise ValueError(f"Failed to convert 'dt' column to datetime: {e}")

    # --- 2. Filter Data ---
    # Use boolean indexing on the integer-indexed DataFrame
    time_filter_mask = result_df['dt'] <= time
    df_filtered = result_df.loc[time_filter_mask, required_cols].copy()

    if df_filtered.empty:
        print(f"No data found at or before {time}.")
        # Return the original df structure but potentially empty if time filter removes all data
        # Or decide if you want to return the original unmodified df
        return result_df[
            factor_cols]  # Return only factor cols if empty after filter? Or result_df.iloc[0:0]? Choose best fit.

    print(f"Filtered DataFrame shape: {df_filtered.shape}")

    # --- 3. Split Columns (Using external function) ---
    # Ensure 'split_columns_into_blocks' is available in the calling scope
    try:
        column_blocks = split_columns_into_blocks(
            factor_cols,
            base_memory_percentage=1,  # Example value, adjust as needed
            current_frequency=current_frequency
        )
        if not column_blocks or not column_blocks[0]:
            print("Warning: split_columns_into_blocks returned empty blocks. No factors processed.")
            return result_df
    except NameError:
        raise NameError("Function 'split_columns_into_blocks' is not defined or imported.")
    except Exception as e:
        raise RuntimeError(f"Error calling split_columns_into_blocks: {e}")

    # --- 4. Prepare Base Data (dt, target) for Shared Memory ---
    print("Preparing base data for Shared Memory...")
    # Factorize 'dt' column directly from the filtered DataFrame
    dt_numeric, _ = pd.factorize(df_filtered['dt'])
    dt_numeric = dt_numeric.astype(np.int32)
    target_numeric = df_filtered['target_1'].to_numpy(dtype=np.float64)  # Use float64

    # --- 5. Create Base Shared Memory Segments ---
    shm_dt = shm_target = None
    # Use process ID in name for better uniqueness across runs if cleanup fails
    pid = os.getpid()
    shm_dt_name = f"shm_dt_{pid}_{uuid.uuid4()}"
    shm_target_name = f"shm_target_{pid}_{uuid.uuid4()}"
    shm_created_list = []  # Track SHM names for final cleanup

    try:
        # Create SHM for dt
        shm_dt = shared_memory.SharedMemory(create=True, size=dt_numeric.nbytes, name=shm_dt_name)
        shm_array_dt = np.ndarray(dt_numeric.shape, dtype=dt_numeric.dtype, buffer=shm_dt.buf)
        shm_array_dt[:] = dt_numeric[:]
        shm_created_list.append(shm_dt_name)
        base_dt_info = {"name": shm_dt_name, "shape": dt_numeric.shape, "dtype": dt_numeric.dtype}
        del shm_array_dt  # Release buffer reference in main process

        # Create SHM for target
        shm_target = shared_memory.SharedMemory(create=True, size=target_numeric.nbytes, name=shm_target_name)
        shm_array_target = np.ndarray(target_numeric.shape, dtype=target_numeric.dtype, buffer=shm_target.buf)
        shm_array_target[:] = target_numeric[:]
        shm_created_list.append(shm_target_name)
        base_target_info = {"name": shm_target_name, "shape": target_numeric.shape, "dtype": target_numeric.dtype}
        del shm_array_target  # Release buffer reference

        del dt_numeric, target_numeric  # Base arrays copied to SHM
        gc.collect()
        print("Base dt and target data copied to Shared Memory.")

        # --- 6. Process Each Column Block ---
        results_map = {}  # Store results {col_name: result_code}
        n_layers_for_auto_reverse = 5  # Standard n_layers

        for block_idx, block_cols in enumerate(column_blocks):
            if not block_cols:  # Skip empty blocks
                print(f"Skipping empty block {block_idx + 1}/{len(column_blocks)}")
                continue

            print(f"\nProcessing block {block_idx + 1}/{len(column_blocks)} with {len(block_cols)} factors...")
            block_start_time = pytime.time()

            shm_factors = None
            shm_factors_name = f"shm_factors_{pid}_{uuid.uuid4()}"
            block_shm_created = False

            try:
                # --- a. Create SHM for Factor Block ---
                # Extract factor data for the block from the filtered DataFrame
                block_factors_data = df_filtered[block_cols].to_numpy(dtype=np.float64)

                shm_factors = shared_memory.SharedMemory(create=True, size=block_factors_data.nbytes,
                                                         name=shm_factors_name)
                shm_array_factors = np.ndarray(block_factors_data.shape, dtype=block_factors_data.dtype,
                                               buffer=shm_factors.buf)
                shm_array_factors[:] = block_factors_data[:]
                shm_created_list.append(shm_factors_name)  # Track successful creation
                block_shm_created = True
                block_factors_info = {"name": shm_factors_name, "shape": block_factors_data.shape,
                                      "dtype": block_factors_data.dtype}
                del shm_array_factors, block_factors_data  # Release buffer/data
                gc.collect()
                print(f"Created SHM factor block: {shm_factors_name}, Shape: {block_factors_info['shape']}")

                # --- b. Prepare Tasks for Workers ---
                tasks = []
                for i, col_name in enumerate(block_cols):
                    task_item = (
                        base_dt_info["name"], base_target_info["name"], block_factors_info["name"],
                        base_dt_info["shape"], base_dt_info["dtype"],
                        base_target_info["shape"], base_target_info["dtype"],
                        block_factors_info["shape"], block_factors_info["dtype"],
                        i,  # Index within the block's factor array
                        col_name,  # Original column name
                        n_layers_for_auto_reverse
                    )
                    tasks.append(task_item)

                # --- c. Execute in Parallel using ProcessPoolExecutor ---
                # Adjust chunksize calculation as needed
                optimal_chunksize = max(1, min(chunksize_m,
                                               len(tasks) // (n_jobs * chunksize_n) if n_jobs > 0 else len(tasks)))
                print(f"Using chunksize: {optimal_chunksize}, Workers: {n_jobs}")

                # Set context if needed, though spawn is usually set globally
                # mp_context = multiprocessing.get_context('spawn')
                # with ProcessPoolExecutor(max_workers=n_jobs, mp_context=mp_context) as executor:

                with ProcessPoolExecutor(max_workers=n_jobs,
                                         mp_context=multiprocessing.get_context(mp_context)) as executor:
                    # Use tqdm for progress bar
                    future_results = executor.map(
                        process_auto_reverse_optimized_shm,  # Use the SHM worker
                        tasks,
                        chunksize=optimal_chunksize
                    )
                    # Collect results as they complete
                    for result_code, factor_name in tqdm(future_results, total=len(tasks),
                                                         desc=f"Block {block_idx + 1} Auto-Reverse"):
                        results_map[factor_name] = result_code

                elapsed = pytime.time() - block_start_time
                print(f"Block {block_idx + 1} processed in {elapsed:.2f} seconds.")

            except Exception as e:
                print(f"Error processing block {block_idx + 1}: {e}")
                traceback.print_exc()
                # Mark factors in this block as 'keep' (1) on error
                for col_name in block_cols:
                    results_map.setdefault(col_name, 1)
            finally:
                # --- d. Clean Up Factor Block SHM ---
                if shm_factors:
                    shm_factors.close()
                if block_shm_created:
                    try:
                        # Use existing name for unlinking
                        temp_shm = shared_memory.SharedMemory(name=shm_factors_name)
                        temp_shm.close()
                        temp_shm.unlink()
                        print(f"Unlinked SHM factor block: {shm_factors_name}")
                        if shm_factors_name in shm_created_list:
                            shm_created_list.remove(shm_factors_name)
                    except FileNotFoundError:  # Already unlinked or error during creation
                        if shm_factors_name in shm_created_list:
                            shm_created_list.remove(shm_factors_name)
                    except Exception as unlink_e:
                        print(f"Error unlinking block SHM {shm_factors_name}: {unlink_e}")
                # gc.collect() # Optional, might slow down block transition
                # pytime.sleep(0.05) # Shorter pause

        # --- 7. Apply Results to Original DataFrame ---
        # IMPORTANT: Apply results to the *original* result_df (integer index)
        print("\nApplying results to original DataFrame...")
        n_dropped, n_reversed, n_kept = 0, 0, 0
        cols_to_drop = []
        result_df_processed = result_df.copy()
        reverse_dict = {}  # Create copy to modify safely
        reverse_dict['keep'] = []
        reverse_dict['drop'] = []
        reverse_dict['reverse'] = []
        for f_col in factor_cols:
            # Default to keep (1) if missing from results (e.g., block error)
            result_code = results_map.get(f_col, 1)

            if f_col not in result_df_processed.columns:
                # This shouldn't happen if processing started with these cols, but safety check
                print(f"Warning: Factor {f_col} missing from DataFrame before applying results. Skipping.")
                continue

            if result_code == 0:
                reverse_dict['drop'].append(f_col)
                cols_to_drop.append(f_col)
                n_dropped += 1
            elif result_code == -1:
                reverse_dict['reverse'].append(f_col)
                # Apply reversal directly TO THE COPY
                result_df_processed[f_col] = -result_df_processed[f_col]
                n_reversed += 1
            else:  # result_code == 1 or error default
                reverse_dict['keep'].append(f_col)
                n_kept += 1

        # Drop columns from the copy
        # if cols_to_drop:
        #     print(f"Dropping {len(cols_to_drop)} columns...")
        #     result_df_processed = result_df_processed.drop(columns=cols_to_drop)
        # else:
        #     print("No columns marked for dropping.")

        print(f"Auto-reverse finished. Kept: {n_kept}, Reversed: {n_reversed}, Dropped: {n_dropped}")

    except Exception as main_e:
        print(f"An critical error occurred during the main processing: {main_e}")
        traceback.print_exc()
        # Decide what to return on major failure: original df? or raise error?
        # Returning original df might be safer in a pipeline.
        result_df_processed = result_df
    finally:
        # --- 8. Final Cleanup of Base Shared Memory ---
        print("Final cleanup of base shared memory...")
        if shm_dt: shm_dt.close()
        if shm_target: shm_target.close()

        # Unlink all tracked SHM segments that might remain
        # Use a copy of the list for safe iteration while removing
        for shm_name in shm_created_list[:]:
            try:
                temp_shm = shared_memory.SharedMemory(name=shm_name)
                temp_shm.close()
                temp_shm.unlink()
                print(f"Unlinked SHM: {shm_name}")
                shm_created_list.remove(shm_name)  # Remove from original list on success
            except FileNotFoundError:
                # Already unlinked or maybe never fully created/tracked correctly
                if shm_name in shm_created_list: shm_created_list.remove(shm_name)
            except Exception as e:
                print(f"Error during final unlinking of {shm_name}: {e}")

        if shm_created_list:
            print(f"Warning: Potentially unlinked SHM segments may remain: {shm_created_list}")

        print(f"Total processing time: {pytime.time() - start_time:.2f} seconds.")
        gc.collect()

    # Return the modified DataFrame (or original on error), preserving integer index
    return result_df_processed, reverse_dict


def run_all_factor_functions(df, yinzi, n_jobs=None, current_frequency='4小时', ):
    """
    分块并行运行目录中的所有因子计算函数，控制内存使用

    Args:
        df: 输入的DataFrame
        n_jobs: 并行进程数，默认为None (使用CPU核心数-1)

    Returns:
        添加了因子的DataFrame
    """
    # 如果没有指定并行线程数，则使用CPU核心数-1
    if n_jobs is None:
        n_jobs = max(1, os.cpu_count() - 1)  # type: ignore #
    # df_cols = pd.read_csv(
    #     f"{path_dr}/experiment/factor_function_{yinzi}/cols.csv")
    # my_list = df_cols['factor'].tolist()
    # py_files = [f'{f}.py' for f in my_list]
    path = f"{path_dr}/experiment/factor_function_{yinzi}"
    py_files = [f for f in os.listdir(path) if f.endswith('.py')]

    if not py_files:
        return df

    print(f"使用 {n_jobs} 个进程并行处理 {len(py_files)} 个因子函数")

    # 创建DataFrame的副本以避免修改原始数据
    result_df = df.copy()
    column_blocks = split_columns_into_blocks(
        py_files,
        base_memory_percentage=3,  # 基于4小时数据的内存使用
        current_frequency=current_frequency
    )
    # 使用分块处理

    # 逐块处理文件
    for block_idx, block_files in enumerate(column_blocks):
        print(f"处理块 {block_idx + 1}/{len(column_blocks)} 包含 {len(block_files)} 个因子函数")

        feature_list = [
            (result_df[
                 ["open", "close", "high", "low", "vol", "amount", "trades", "tbase", "tquote", "vwap",
                  "returns"]].copy(),
             filename, yinzi)
            for filename in block_files
        ]

        # 计算最佳的分块大小
        optimal_chunksize = max(1, min(chunksize_m, len(block_files) // (n_jobs * chunksize_n)))

        with ProcessPoolExecutor(
                max_workers=n_jobs,
                mp_context=multiprocessing.get_context(mp_context)
        ) as executor:
            bar = tqdm(total=len(block_files), desc=f"块 {block_idx + 1} 因子计算")

            # 使用map方法并行处理，只传递列名
            for filename, processed_df, error_message in executor.map(process_single_factor,
                                                                      feature_list,
                                                                      chunksize=optimal_chunksize
                                                                      ):
                bar.update(1)

                if error_message:
                    logger.error(error_message)
                elif processed_df is not None:
                    # 将处理后的DataFrame中的新列合并到结果DataFrame中
                    new_columns = set(processed_df.columns) - {"open", "close", "high", "low",
                                                               "vol",
                                                               "amount", "trades", "tbase", "tquote", "vwap",
                                                               "returns"}
                    for col in new_columns:
                        df[col] = processed_df[col]

    return df


def full_feature_engineering(df: pd.DataFrame, n_jobbs, c, yinzi) -> pd.DataFrame:
    """完整的特征工程处理流程

    Args:
        df: 输入的DataFrame，包含价格和交易量数据

    Returns:
        添加了所有特征的DataFrame
    """
    # 第一步：执行基础特征工程
    df = process_features(df)

    # 第二步：运行所有自定义因子函数
    df['returns'] = df['F#return_1']

    df.set_index(["symbol", "dt"], inplace=True)
    df = run_all_factor_functions(df, yinzi, n_jobbs, c)
    df = df.reset_index()

    # 第三步：计算后续N根bar的累计收益，用于回测分析
    total_cols = df.shape[1]

    # Calculate the split points for 4 segments
    col_segment_size = total_cols // 4
    split_points = [0, col_segment_size, 2 * col_segment_size, 3 * col_segment_size, total_cols]

    # Process each segment separately
    segments = []
    for i in range(4):
        # Extract segment
        segment = df.iloc[:, split_points[i]:split_points[i + 1]].copy()

        # Apply operations
        segment = pd.DataFrame(segment.values, columns=segment.columns)
        segment = segment.replace([np.inf, -np.inf], np.nan)
        segment = segment.fillna(0)
        segments.append(segment)

    # Combine the processed segments back together
    df_processed = pd.concat(segments, axis=1)
    return df_processed




def calculate_factor(frequency, n_jobbs, d, yinzi,sdt,edt):
    """计算所有股票的量价因子"""
    try:
        dfk = pd.read_feather(f"{path_dr}/experiment/file/klines_{frequency}_{d}_{yinzi}.feather")
        dfk = full_feature_engineering(dfk, n_jobbs, frequency, yinzi)

        factor_cols = [col for col in dfk.columns if col.startswith('F#')]

        # 计算每个因子列的0值占比
        zero_ratios = {}
        for col in factor_cols:
            zero_ratio = (dfk[col] == 0).mean()
            if zero_ratio > 0.2:  # 如果0值占比超过30%
                zero_ratios[col] = zero_ratio

        # 获取需要删除的列名
        cols_to_drop = list(zero_ratios.keys())
        existing_cols = [col for col in cols_to_drop if col in dfk.columns]
        if existing_cols:
            dfk = dfk.drop(columns=existing_cols)
        dfk = dfk.sort_values(['symbol', 'dt']).reset_index(drop=True)

        return dfk

    except FileNotFoundError:
        logger.warning("没有k线数据")
        return


def calculate_factor_returns_blocked(df, n_jobs=None, current_frequency='4小时',
                                     split_time=pd.to_datetime('2024-01-01')):
    """
    分块计算因子收益，控制内存使用

    Args:
        df (pd.DataFrame): 输入的DataFrame
        output_file (str): 输出文件路径
        n_jobs (int): 并行线程数
        current_frequency (str): 当前频率
        split_time:时间

    Returns:
        pd.DataFrame: 因子收益DataFrame
    """
    try:
        # 检查是否存在必需的列
        if 'dt' not in df.columns or 'target_1' not in df.columns:
            raise ValueError("输入文件必须包含 'dt' 和 'target_1' 列")

        # 识别因子列（以"F#"开头的列）
        factor_columns = [col for col in df.columns if col.startswith("F#")]
        if not factor_columns:
            raise ValueError("未找到因子列（以'F#'开头的列）")

        print(f"找到 {len(factor_columns)} 个因子列")

        df['dt'] = pd.to_datetime(df['dt'])
        # df=df[df['dt']<=split_time].copy()
        df['date'] = df['dt'].dt.date

        # 预先创建所有可能的日期-股票组合
        all_dates = df['date'].unique()
        all_symbols = df['symbol'].unique()
        date_symbol_index = pd.MultiIndex.from_product(
            [all_dates, all_symbols],
            names=['date', 'symbol']
        )

        # 将因子列分成块
        column_blocks = split_columns_into_blocks(
            factor_columns,
            base_memory_percentage=0.45,  # 基于4小时数据的内存使用
            current_frequency=current_frequency
        )

        # 存储所有因子DataFrame的列表
        all_factor_dfs = []
        for block_idx, block_cols in enumerate(column_blocks):
            print(f"处理块 {block_idx + 1}/{len(column_blocks)} 包含 {len(block_cols)} 列")

            feature_list = [(df[['target_1', 'dt', 'symbol', 'date', col]].copy(), col, date_symbol_index)
                            for col in block_cols]

            # 计算最佳的分块大小
            optimal_chunksize = max(1, min(chunksize_m, len(block_cols) // (n_jobs * chunksize_n)))
            factor_dfs = []
            with ProcessPoolExecutor(
                    max_workers=n_jobs,
                    mp_context=multiprocessing.get_context(mp_context)

            ) as executor:
                bar = tqdm(total=len(block_cols), desc=f"块 {block_idx + 1} 因子收益计算")
                for factor_df in executor.map(get_factor_returns, feature_list, chunksize=optimal_chunksize):
                    bar.update(1)
                    factor_dfs.append(factor_df)

            # 将当前块的结果添加到总结果
            all_factor_dfs.extend(factor_dfs)

        # 合并所有因子DataFrame
        print("合并因子结果...")
        result_df = pd.concat(all_factor_dfs, axis=1)

        # 重置索引使日期成为列
        result_df.reset_index(inplace=True)
        result_df.rename(columns={'date': 'dt'}, inplace=True)

        # 保存到文件

        return result_df

    except Exception as e:
        print(f"错误: {e}")
        raise


def cross_normalize_numpy(dt_array, x_array, method='zscore', **kwargs):
    """
    基于NumPy的列标准化函数 (Preserved Core Logic).

    Args:
        dt_array (np.ndarray): 日期数组 (factorized or datetime representation used for comparison)
        x_array (np.ndarray): 需要标准化的单列因子值数组
        method (str): 标准化方法
        **kwargs: 其他参数 (winsorize, q, n)

    Returns:
        np.ndarray: 标准化后的值数组，与输入 x_array 顺序相同
    """
    # 检查是否有NaN值 - Preserved Original Check
    # Note: Consider if NaN handling should be different (e.g., skip row, fill with 0)
    # This implementation *errors* on NaN.
    nan_mask = np.isnan(x_array)
    if np.any(nan_mask):
        # Option 1: Error out (Original behavior)
        raise ValueError(f"因子有缺失值，缺失数量为：{np.sum(nan_mask)}")
        # Option 2: Return NaNs where input was NaN, process rest (Alternative)
        # result_with_nan = np.full(x_array.shape, np.nan, dtype=np.float64)
        # valid_mask = ~nan_mask
        # if np.any(valid_mask):
        #     normalized_valid = cross_normalize_numpy(dt_array[valid_mask], x_array[valid_mask], method, **kwargs)
        #     result_with_nan[valid_mask] = normalized_valid
        # return result_with_nan

    # 获取参数
    winsorize = kwargs.get("winsorize", False)
    q = kwargs.get("q", 0.05)
    n = kwargs.get("n", 3)

    # 创建结果数组，初始化为 NaN 或 0 (using 0 matches original init)
    result = np.zeros_like(x_array, dtype=np.float64)  # Use float64 for calculations

    # 获取所有唯一日期 (using unique on potentially factorized integers is fine)
    unique_dates, dt_inverse = np.unique(dt_array, return_inverse=True)

    # 按日期分组处理数据 (Loop preserved for logic consistency)
    for i, dt in enumerate(unique_dates):
        # 创建当前日期的掩码 (more efficient using inverse map)
        dt_mask = (dt_inverse == i)

        # 获取当前日期的原始索引位置 (needed to place results back)
        dt_indices = np.where(dt_mask)[0]

        # 提取当前时间截面的数据
        dt_x_values = x_array[dt_mask]

        # 检查数据点数量
        if len(dt_x_values) <= 1:
            # print(f'日期 {dt} 数据点数量不足 ({len(dt_x_values)}), 跳过标准化. Values remain 0.')
            # Original code implicitly left result as 0 here, so we continue
            continue

        # --- Winsorize (Optional) ---
        if winsorize:
            try:
                lower, upper = np.quantile(dt_x_values, q), np.quantile(dt_x_values, 1 - q)
                # Avoid clipping if lower==upper (constant data)
                if lower < upper:
                    dt_x_values = np.clip(dt_x_values, lower, upper)
            except Exception as win_err:
                print(f"Warning: Winsorizing failed for date {dt}: {win_err}. Using original data.")
                # Continue with original dt_x_values if clipping fails

        # --- Apply Normalization Method ---
        normalized = np.zeros_like(dt_x_values)  # Init for this group

        try:  # Wrap calculation in try block per date
            if method == "zscore":
                mean = np.mean(dt_x_values)
                std = np.std(dt_x_values)
                if std > 1e-9:  # Use tolerance for std check
                    normalized = (dt_x_values - mean) / std
                # else: normalized remains 0

            elif method == "zscore_clip":
                mean = np.mean(dt_x_values)
                std = np.std(dt_x_values)
                if std > 1e-9:
                    normalized = (dt_x_values - mean) / std
                    normalized = np.clip(normalized, -1, 1)
                # else: normalized remains 0

            elif method == "zscore_maxmin":
                mean = np.mean(dt_x_values)
                std = np.std(dt_x_values)
                if std > 1e-9:
                    z = (dt_x_values - mean) / std
                    max_abs = np.max(np.abs(z))  # More robust than max(abs(max), abs(min))
                    if max_abs > 1e-9:
                        normalized = z / max_abs
                    else:
                        normalized = z  # Or 0 if max_abs is near zero
                # else: normalized = np.zeros_like(dt_x_values)

            elif method == "max_min":
                # Scale by max absolute value to [-1, 1]
                max_abs_val = np.max(np.abs(dt_x_values))
                if max_abs_val > 1e-9:
                    normalized = dt_x_values / max_abs_val
                # else: normalized remains 0

            elif method == "sum":
                # Normalize by sum of absolute values
                sum_abs = np.sum(np.abs(dt_x_values))
                if sum_abs > 1e-9:
                    normalized = dt_x_values / sum_abs
                # else: normalized remains 0

            elif method == "rank_s":
                # Standard percentile rank scaled to [-1, 1]
                ranks = stats.rankdata(dt_x_values)  # Default method='average'
                n_valid = len(dt_x_values)
                # Formula adjustment for clarity and potential 0/0
                if n_valid > 0:
                    percentiles = ranks / (n_valid + 1)  # Avoids reaching exactly 1
                    # Scale to [-1, 1] (alternative: 2 * percentiles - 1)
                    normalized = 2 * (ranks - (n_valid + 1) / 2) / n_valid  # Centers around 0
                    # Original formula: 2 * (ranks - 0.5 / n_valid) - 1 -- check desired scale/centering
                # else: normalized remains 0

            elif method == "rank_balanced":
                # Balanced rank transformation
                ranks = stats.rankdata(dt_x_values)
                n_valid = len(dt_x_values)
                if n_valid > 0:
                    percentiles = ranks / (n_valid + 1)  # Use percentiles centered away from 0/1
                    normalized = stats.norm.ppf(percentiles)  # Inverse CDF (probit)
                    # Clip infinite values resulting from ppf near 0/1
                    normalized = np.clip(normalized, -5, 5)  # Adjust clip range as needed
                    # Original formula seemed different, using standard normal quantile transform here
                # else: normalized remains 0


            elif method == "rank_c":
                # Custom rank (top/bottom n)
                n_valid = len(dt_x_values)
                if n_valid > 0:  # Ensure n is not larger than available data
                    actual_n = min(n, n_valid)
                    rank_asc = stats.rankdata(dt_x_values, method='ordinal')
                    rank_desc = stats.rankdata(-dt_x_values, method='ordinal')

                    # Apply weighting for top n (highest values)
                    top_mask = (rank_desc <= actual_n)
                    normalized[top_mask] = (actual_n - (rank_desc[top_mask] - 1)) / actual_n

                    # Apply weighting for bottom n (lowest values)
                    bottom_mask = (rank_asc <= actual_n)
                    # Use negative sign for bottom ranks, ensure weighting is correct
                    normalized[bottom_mask] = -((actual_n - (rank_asc[bottom_mask] - 1)) / actual_n)
                    # Note: If top_mask and bottom_mask overlap (small N), top wins here. Adjust if needed.
                # else: normalized remains 0


            elif method == "rank_q":
                # Quantile rank - requires pre-defined bins or logic not easily done per group here
                print(f"Warning: Method 'rank_q' not directly implemented in numpy version for date {dt}. Returning 0.")
                # normalized remains 0

            else:
                # Keep original error for unsupported methods
                raise ValueError(f"不支持的标准化方法: {method}.")

            # --- Store Rounded Results ---
            # Rounding to 2 decimal places as in original code
            result[dt_indices] = np.round(normalized, 2)

        except Exception as calc_err:
            print(f"Error calculating normalization for date {dt}, method {method}: {calc_err}")
            # Leave result[dt_indices] as 0 on error for this date group

    return result


# ================================================================
# Worker Function (Using Shared Memory - Block Strategy)
# ================================================================

def cross_normal_shared_memory(args):
    """
    Worker using Shared Memory (Block Strategy). Processes one column.

    Args:
        args (tuple): (col_name, col_idx_in_block,
                       dt_shm_name, dt_shape, dt_dtype,
                       factors_shm_name, factors_shape, factors_dtype,
                       method, kwargs)

    Returns:
        tuple: (column_name, normalized_values_array) or (column_name, None) on error
    """
    (
        col_name, col_idx_in_block,
        dt_shm_name, dt_shape, dt_dtype,
        factors_shm_name, factors_shape, factors_dtype,
        method, kwargs  # Pass kwargs through
    ) = args

    shm_dt = shm_factors = None
    array_dt = array_factors = None
    col_data_view = None  # Keep track of view/copy

    try:
        # Connect to shared memory
        shm_dt = shared_memory.SharedMemory(name=dt_shm_name)
        shm_factors = shared_memory.SharedMemory(name=factors_shm_name)

        # Create NumPy array views
        array_dt = np.ndarray(dt_shape, dtype=dt_dtype, buffer=shm_dt.buf)
        array_factors = np.ndarray(factors_shape, dtype=factors_dtype, buffer=shm_factors.buf)

        # Get a view of the specific column data (more efficient than copy)
        # Ensure it's treated as float64 for calculations downstream
        col_data_view = array_factors[:, col_idx_in_block].astype(np.float64, copy=False)

        # Call the core NumPy normalization function
        # Pass kwargs down to the numpy function
        normalized_values = cross_normalize_numpy(array_dt, col_data_view, method, **kwargs)

        # Close SHM connections (don't unlink here)
        shm_dt.close()
        shm_factors.close()

        return col_name, normalized_values

    except ValueError as ve:  # Catch the specific NaN error from cross_normalize_numpy
        print(f"处理列 {col_name} 时出错 (ValueError): {ve}")
        # Return None for this column as per original error handling logic implicit in cross_normalize_numpy raising error
        return col_name, None  # Or re-raise if needed
    except FileNotFoundError:
        print(f"Error: SHM block not found in worker for {col_name}.")
        return col_name, None
    except Exception as e:
        print(f"处理列 {col_name} 时出现意外错误: {type(e).__name__} - {e}")
        traceback.print_exc()
        return col_name, None  # Return None on other errors too
    finally:
        # Ensure buffer references are released
        del array_dt, array_factors, col_data_view
        if shm_dt: shm_dt.close()
        if shm_factors: shm_factors.close()
        # gc.collect() # Optional: uncomment if memory issues persist in workers


# ================================================================
# Main Orchestrator (Parallel, Blocked SHM)
# ================================================================

def normalize_column_parallel_blocked(df, factor_cols, method='zscore', n_jobs=None,
                                      current_frequency='4小时', **kwargs):
    """
    使用共享内存(Block Strategy)分块并行处理列标准化.

    Args:
        df (pd.DataFrame): 输入DataFrame，必须包含 'dt' 列.
        factor_cols (list): 需要标准化的因子列名列表.
        method (str): 标准化方法.
        n_jobs (int, optional): 并行进程数. Defaults to CPU count - 1.
        current_frequency (str): 用于 split_columns_into_blocks 的频率字符串.
        **kwargs: Additional arguments passed to cross_normalize_numpy (e.g., winsorize=True, q=0.01).

    Returns:
        pd.DataFrame: 包含标准化后因子列的DataFrame副本.
    """
    if n_jobs is None:
        n_jobs = max(1, multiprocessing.cpu_count() - 1)
    if n_jobs <= 0:
        print("Warning: n_jobs <= 0. Running in single-threaded mode (less efficient).")
        n_jobs = 1  # Ensure at least 1 job for sequential processing

    if 'dt' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'dt' column.")

    if not factor_cols:
        print("No factor columns provided for normalization.")
        return df.copy()

    # Ensure factor columns exist
    missing_factors = [f for f in factor_cols if f not in df.columns]
    if missing_factors:
        raise ValueError(f"Factor columns not found in DataFrame: {missing_factors}")

    print(f"启动并行标准化 (方法: {method}, 线程数: {n_jobs}, 因子数: {len(factor_cols)})")
    start_time = pytime.time()

    # 创建结果数据框副本
    result_df = df.copy()

    # --- 1. Split Columns into Blocks ---
    print("Splitting columns into blocks...")
    try:
        # Assume split_columns_into_blocks is available
        column_blocks = split_columns_into_blocks(
            factor_cols,
            base_memory_percentage=0.4,  # Adjust memory factor as needed
            current_frequency=current_frequency
        )
        if not column_blocks or not any(column_blocks):
            print("Warning: split_columns_into_blocks returned no valid blocks.")
            return result_df  # Return copy if no blocks
    except NameError:
        print("\nERROR: The required function 'split_columns_into_blocks' was not found.")
        raise
    except Exception as e:
        raise RuntimeError(f"Error calling split_columns_into_blocks: {e}")

    n_blocks = len(column_blocks)
    print(f"Split into {n_blocks} blocks.")

    # --- 2. Prepare Base 'dt' Data for Shared Memory ---
    print("Preparing 'dt' data for Shared Memory...")
    # Factorize 'dt' for efficient grouping/comparison in NumPy
    # Store original dtype for potential reconstruction if needed, but factorized is used internally
    dt_factorized, unique_dts = pd.factorize(df['dt'])
    dt_factorized = dt_factorized.astype(np.int32)  # Use int32 for space efficiency

    shm_dt = None
    pid = os.getpid()
    shm_dt_name = f"norm_shm_dt_{pid}_{uuid.uuid4()}"
    shm_created_list = []  # Track all created SHM objects for cleanup

    try:
        shm_dt = shared_memory.SharedMemory(create=True, size=dt_factorized.nbytes, name=shm_dt_name)
        shm_array_dt = np.ndarray(dt_factorized.shape, dtype=dt_factorized.dtype, buffer=shm_dt.buf)
        shm_array_dt[:] = dt_factorized[:]
        shm_created_list.append(shm_dt)  # Track the SHM object
        base_dt_info = {"name": shm_dt.name, "shape": dt_factorized.shape, "dtype": dt_factorized.dtype}
        del shm_array_dt  # Release buffer reference in main process
        print(f"Shared memory created for 'dt': {shm_dt.name}")

        # --- 3. Process Each Column Block ---
        results_collector = {}  # To store results temporarily

        for block_idx, block_cols in enumerate(column_blocks):
            if not block_cols:
                print(f"Skipping empty block {block_idx + 1}/{n_blocks}")
                continue

            print(f"\n处理块 {block_idx + 1}/{n_blocks} (因子数: {len(block_cols)})...")
            block_start_time = pytime.time()

            shm_factors_block = None
            shm_factors_name_block = f"norm_shm_factors_{pid}_{block_idx}_{uuid.uuid4()}"
            block_shm_created_flag = False

            try:
                # --- a. Create SHM for Factor Block ---
                # Convert block data to float64 for consistent calculations
                block_factors_data = df[block_cols].to_numpy(dtype=np.float64)

                shm_factors_block = shared_memory.SharedMemory(create=True, size=block_factors_data.nbytes,
                                                               name=shm_factors_name_block)
                shm_array_factors = np.ndarray(block_factors_data.shape, dtype=block_factors_data.dtype,
                                               buffer=shm_factors_block.buf)
                shm_array_factors[:] = block_factors_data[:]
                shm_created_list.append(shm_factors_block)  # Add block SHM to master list
                block_shm_created_flag = True
                block_factors_info = {"name": shm_factors_block.name, "shape": block_factors_data.shape,
                                      "dtype": block_factors_data.dtype}
                del shm_array_factors, block_factors_data
                gc.collect()
                # print(f"  Block SHM created: {shm_factors_block.name}")

                # --- b. Prepare Tasks for Workers ---
                tasks = []
                for i, col_name in enumerate(block_cols):
                    task_item = (
                        col_name, i,  # Pass col name and its index within the block
                        base_dt_info["name"], base_dt_info["shape"], base_dt_info["dtype"],
                        block_factors_info["name"], block_factors_info["shape"], block_factors_info["dtype"],
                        method, kwargs  # Pass method and extra args
                    )
                    tasks.append(task_item)

                # --- c. Execute in Parallel ---
                n_tasks = len(tasks)
                # Adjust chunksize - smaller might be better if tasks are very fast
                chunksize = max(1, min(chunksize_m, n_tasks // (n_jobs * chunksize_n) if n_jobs > 0 else n_tasks))
                print(f"  提交 {n_tasks} 个任务 (chunksize={chunksize})...")

                block_results_temp = {}
                # Using ProcessPoolExecutor consistently
                with ProcessPoolExecutor(max_workers=n_jobs,
                                         mp_context=multiprocessing.get_context(mp_context)) as executor:
                    future_results = executor.map(
                        cross_normal_shared_memory,
                        tasks,
                        chunksize=chunksize
                    )
                    for col, values in tqdm(future_results, total=n_tasks, desc=f"块 {block_idx + 1}/{n_blocks} 标准化",
                                            leave=False):
                        # Store results directly if valid
                        if values is not None:
                            block_results_temp[col] = values
                        else:
                            print(f"  列 {col} 未返回有效结果 (可能包含NaN或处理错误).")

                # --- d. Update main DataFrame with block results ---
                # Update result_df efficiently after collecting all results for the block
                print(f"\n  Updating DataFrame with results for block {block_idx + 1}...")
                update_count = 0
                for col, values in block_results_temp.items():
                    if col in result_df.columns:
                        result_df[col] = values
                        update_count += 1
                    else:
                        print(f"Warning: Column {col} from results not found in result_df during update.")
                print(f"  Updated {update_count} columns for block {block_idx + 1}.")
                results_collector.update(block_results_temp)  # Optional: collect all results if needed elsewhere

                elapsed = pytime.time() - block_start_time
                print(f"块 {block_idx + 1} 处理完毕，耗时 {elapsed:.2f} 秒.")

            except Exception as e:
                print(f"\n处理块 {block_idx + 1} 时发生错误: {e}")
                traceback.print_exc()
                # Decide how to handle block errors - skip block? Stop? Log?
                # Currently, factors in failed blocks won't be updated in result_df
            finally:
                # --- e. Clean Up *This Block's* Factor SHM ---
                if shm_factors_block:
                    shm_factors_block.close()
                    if block_shm_created_flag:
                        try:
                            shm_factors_block.unlink()
                            # print(f"  Unlinked block SHM: {shm_factors_block.name}")
                            if shm_factors_block in shm_created_list:
                                shm_created_list.remove(shm_factors_block)
                        except FileNotFoundError:
                            if shm_factors_block in shm_created_list:
                                shm_created_list.remove(shm_factors_block)
                        except Exception as unlink_e:
                            print(f"  Error unlinking block SHM {shm_factors_block.name}: {unlink_e}")
                gc.collect()
                pytime.sleep(0.05)  # Small pause

    except Exception as main_e:
        print(f"\n标准化过程中发生严重错误: {main_e}")
        traceback.print_exc()
        # Return the initial copy on major failure
        print("由于发生错误，返回原始DataFrame的副本.")
        return df.copy()  # Or potentially result_df up to the point of failure
    finally:
        # --- 4. Final Cleanup of *ALL* Shared Memory ---
        print("\n最终清理共享内存...")
        for shm_instance in shm_created_list[:]:
            try:
                shm_name_final = shm_instance.name
                shm_instance.close()
                shm_instance.unlink()
                # print(f"  清理完毕: {shm_name_final}")
                shm_created_list.remove(shm_instance)
            except FileNotFoundError:
                if shm_instance in shm_created_list: shm_created_list.remove(shm_instance)
            except Exception as e:
                print(f"  清理 SHM {getattr(shm_instance, 'name', 'Unknown')} 时出错: {e}")

        if shm_created_list:
            print(f"警告: {len(shm_created_list)} 个 SHM 段可能未被正确清理.")

        print(f"标准化总耗时: {pytime.time() - start_time:.2f} 秒.")
        gc.collect()

    # Return the DataFrame with normalized columns
    return result_df


def get_backtest_noparall(df, col):
    try:

        wb = WeightBacktest(df, digits=2, fee_rate=0, n_jobs=16, yearly_days=365)
        metrics = wb.stats
        del wb
        return pd.DataFrame([metrics]), col
    except:
        return None, col


def weight_factors(factor_returns_df, selected_factors, factor_metrics_df=None, factor_results=None,
                   method='equal', reverse_weight=False):
    """
    Apply weighting to selected factors to generate a combined strategy

    Args:
        factor_returns_df (pd.DataFrame): DataFrame with factor returns
        selected_factors (list): List of selected factor names
        factor_metrics_df (pd.DataFrame, optional): DataFrame with factor metrics
        factor_results (pd.DataFrame, optional): DataFrame with raw factor values
        method (str): Weighting method - 'equal' or any column name in factor_metrics_df
        reverse_weight (bool): If True, smaller metric values get higher weights

    Returns:
        tuple: (strategy_returns, factor_weights_df)
    """
    if len(selected_factors) == 0:
        return pd.Series(index=factor_returns_df.index), None

    # Case 1: Equal weighting
    if method == 'equal':
        # Calculate strategy returns as simple average
        strategy_returns = factor_returns_df[selected_factors].mean(axis=1)

        # If factor_results is provided, create weight dataframe
        if factor_results is not None:
            # Select only necessary columns"symbol", "dt",
            df1 = factor_results[
                ['dt', 'symbol', 'price', "open", "close", "high", "low", "vol", "amount"] + selected_factors].copy()

            # Calculate strategy weight as average of factor weights
            df1['weight'] = df1[selected_factors].mean(axis=1)

            # Drop factor columns
            df1 = df1.drop(columns=selected_factors)
        else:
            df1 = None

    # Case 2: Weight by a specific metric from factor_metrics_df
    elif method == 'ic':
        # 筛选出选定的因子
        metric_df = factor_metrics_df[factor_metrics_df['factor'].isin(selected_factors)]  # type: ignore #

        # 创建权重Series，索引为因子名称
        weights = pd.Series(index=selected_factors)

        # 从因子名中提取IC值作为权重
        for factor in selected_factors:
            try:
                weights[factor] = float(factor.split("#")[-1])
            except:
                # 如果无法从因子名提取IC值，使用metric_df中的值
                weights[factor] = metric_df.loc[metric_df['factor'] == factor, 'ic'].values[0]

        # 确保所有权重为正
        if weights.min() <= 0:
            offset = abs(weights.min()) + 0.01 if weights.min() < 0 else 0.01
            weights = weights + offset

        # 应用反转权重（如果需要）
        if reverse_weight:
            weights = 1 / weights

        # 归一化权重，使总和为1
        weights = weights / weights.sum()

        # 计算加权策略收益
        weighted_returns = pd.DataFrame()
        for factor in selected_factors:
            weighted_returns[factor] = factor_returns_df[factor] * weights[factor]

        strategy_returns = weighted_returns.sum(axis=1)

        # 如果提供了factor_results，创建权重DataFrame
        if factor_results is not None:
            df1 = factor_results[
                ['dt', 'symbol', 'price', "open", "close", "high", "low", "vol", "amount"] + selected_factors].copy()

            # 对每个因子应用权重
            for factor in selected_factors:
                df1[factor] = df1[factor] * weights[factor]

            # 计算权重作为归一化因子的加权和
            df1['weight'] = df1[selected_factors].sum(axis=1)

            # 删除因子列
            df1 = df1.drop(columns=selected_factors)

    elif factor_metrics_df is not None and method in factor_metrics_df.columns:
        # Get metric values for selected factors
        metric_df = factor_metrics_df[factor_metrics_df['factor'].isin(selected_factors)]
        metric_values = metric_df.set_index('factor')[method]

        # Handle negative or zero values
        if metric_values.min() <= 0:
            # Add a small positive value to make all values positive
            offset = abs(metric_values.min()) + 0.01 if metric_values.min() < 0 else 0.01
            metric_values = metric_values + offset

        # Apply reverse weighting if needed
        if reverse_weight:
            # Invert weights (1/x transforms larger values to smaller weights)
            weights = 1 / metric_values
        else:
            weights = metric_values

        # Normalize weights to sum to 1
        weights = weights / weights.sum()

        # Calculate weighted strategy returns
        weighted_returns = pd.DataFrame()
        for factor in selected_factors:
            weighted_returns[factor] = factor_returns_df[factor] * weights[factor]

        strategy_returns = weighted_returns.sum(axis=1)

        # If factor_results is provided, create weight dataframe
        if factor_results is not None:
            df1 = factor_results[
                ['dt', 'symbol', 'price', "open", "close", "high", "low", "vol", "amount"] + selected_factors].copy()

            # Apply z-score normalization to each factor
            for factor in selected_factors:
                # Apply factor weight
                df1[factor] = df1[factor] * weights[factor]

            # Calculate weight as weighted sum of normalized factors
            df1['weight'] = df1[selected_factors].sum(axis=1)

            # Drop factor columns
            df1 = df1.drop(columns=selected_factors)
        else:
            df1 = None

    else:
        print(f"Warning: Method '{method}' not supported or metrics data not provided. Using equal weighting.")
        return weight_factors(factor_returns_df, selected_factors, factor_metrics_df, factor_results, 'equal')

    return strategy_returns, df1


def filter_factors(metrics_df, column_name, n_factors, ascending=False):
    """
    Filter factors based on a specific metric column.

    Args:
        metrics_df (pd.DataFrame): DataFrame containing factor metrics
        column_name (str): Column name to sort and filter by
        n_factors (int): Number of factors to select
        ascending (bool): Sort order - True for ascending, False for descending

    Returns:
        list: List of selected factor names
    """
    # Check if column exists
    if column_name not in metrics_df.columns:
        raise ValueError(f"Column '{column_name}' not found in metrics DataFrame")

    # Check if factor column exists
    if 'factor' not in metrics_df.columns:
        raise ValueError("No 'factor' column found in metrics DataFrame")

    # Sort the DataFrame by the specified column
    sorted_df = metrics_df.sort_values(by=column_name, ascending=ascending)

    # Handle case where n_factors is greater than available factors
    n_factors = min(n_factors, len(sorted_df))

    # Select the top n factors
    selected_factors = sorted_df.head(n_factors)['factor'].tolist()

    return selected_factors


def filter_factors_by_threshold(metrics_df, column_name, threshold, greater_than=True):
    """
    Filter factors based on a specific metric column and threshold value.

    Args:
        metrics_df (pd.DataFrame): DataFrame containing factor metrics
        column_name (str): Column name to filter by
        threshold (float): Threshold value for filtering
        greater_than (bool): Filter direction - True for values >= threshold,
                            False for values < threshold

    Returns:
        list: List of selected factor names
    """
    # Check if column exists
    if column_name not in metrics_df.columns:
        raise ValueError(f"Column '{column_name}' not found in metrics DataFrame")

    # Check if factor column exists
    if 'factor' not in metrics_df.columns:
        raise ValueError("No 'factor' column found in metrics DataFrame")

    # Filter the DataFrame by the specified threshold
    if greater_than:
        filtered_df = metrics_df[metrics_df[column_name] >= threshold]
    else:
        filtered_df = metrics_df[metrics_df[column_name] < threshold]

    # Get the factor names
    selected_factors = filtered_df['factor'].tolist()

    return selected_factors


def correlation_filter(candidate_factors, target_n, factor_returns_df, sdt=pd.to_datetime('2015-01-01'),
                       edt=pd.to_datetime('2024-01-01'), max_correlation=max_cor):
    """
    Filter factors based on correlation to ensure diversification

    Args:
        candidate_factors (list): List of factor names in priority order
        target_n (int): Target number of factors to select
        max_correlation (float): Maximum allowed correlation between factors

    Returns:
        list: List of selected factors with low correlation
    """
    factor_returns_df['dt'] = pd.to_datetime(factor_returns_df['dt'])
    factor_returns_df = factor_returns_df[(factor_returns_df['dt'] < edt) & (factor_returns_df['dt'] >= sdt)]

    if len(candidate_factors) == 0:
        return []

    # Initialize with the first factor
    selected = [candidate_factors[0]]

    # Try to add more factors while maintaining low correlation
    for factor in candidate_factors[1:]:
        # Skip if we already have enough factors
        if len(selected) >= target_n:
            break

        # Check correlation with all previously selected factors
        is_correlated = False
        factor_returns = factor_returns_df[factor]

        for sel_factor in selected:
            sel_returns = factor_returns_df[sel_factor]
            correlation = factor_returns.corr(sel_returns)

            if abs(correlation) >= max_correlation:
                is_correlated = True
                break

        # Add to selected if not highly correlated with any existing factor
        if not is_correlated:
            selected.append(factor)

    print(
        f"Selected {len(selected)} factors out of {len(candidate_factors)} candidates after correlation filtering")
    return selected


def generate_strategy_with_blocking(factor_returns_df, factor_metrics_df, factor_results,
                                    n_jobs):
    """在generate_strategy_combinations中添加分块处理"""

    filtering_rules = [
        # ('high20_单笔收益', '单笔收益', 20, 0, False),
        ('high20_年化', '年化', 20, 0, False),
        ('high20_夏普', '夏普', 20, 0, False),
        ('high20_日赢面', '日赢面', 20, 0, False),

        # 5. 平衡型筛选组合
        ('balanced_收益风险', '夏普', 25, 0, False),  # 使用balance_strategy处理

        # 6. 多维度组合筛选
        ('multi_dim_alpha', '夏普', 25, 0, False),  # 使用multi_dim_strategy处理
        ('multi_dim_stable', '夏普', 25, 0, False),  # 使用multi_dim_strategy处理

        # 高稳定性高收益组合
        ('balanced_stable_高收益', '夏普', 25, 0, False),
        ('balanced_stable_稳健', '夏普', 25, 0, False)  # 结合高日胜率、高日盈面、高非零覆盖
        # ('balanced_stable_低风险', '夏普', 30, 0, False),         # 结合低回撤、低波动、高胜率

        # # 风险调整收益组合
        # ('balanced_risk_adj_收益', '夏普', 30, 0, False),         # 结合高夏普、高卡玛、低回撤风险

        # # 综合评分组合
        # ('balanced_score_alpha', '夏普', 30, 0, False),           # 结合年化、夏普、卡玛、日盈面
        # ('balanced_score_stable', '夏普', 30, 0, False),          # 结合胜率、非零覆盖、回撤风险、波动率
        # # 防御性组合
        # ('balanced_defensive', '夏普', 30, 0, False),             # 结合低回撤、低波动、高胜率
        # # 进攻性组合
        # ('balanced_aggressive', '夏普', 30, 0, False),            # 结合高年化、高夏普、高卡玛
        # # 高频交易特征
        # ('high_freq', '夏普', 30, 0, False),             # 结合高胜率、高非零覆盖、高日盈面
        # # 低频交易特征
        # ('low_freq', '夏普', 30, 0, False),              # 结合高夏普、高卡玛、低波动
    ]

    strategy_returns_df = pd.DataFrame()
    strategy_returns_df['dt'] = factor_returns_df['dt']

    # 修改后的生成策略部分，使用分块处理selected_factors
    rows = []
    # 处理常规筛选规则
    for strategy_name, column_name, n_factors, n2_factors, ascending in filtering_rules:
        if strategy_name.startswith('balanced_'):
            # 平衡型策略处理
            selected_factors = balance_strategy(factor_metrics_df, strategy_name, n_factors, factor_returns_df)
        elif strategy_name.startswith('multi_dim_'):
            # 多维度策略处理
            selected_factors = multi_dimensional_strategy(factor_metrics_df, strategy_name, n_factors,
                                                          factor_returns_df)
        else:
            # 常规筛选处理
            if n2_factors == 0:
                # 单指标筛选
                candidate_factors = filter_factors(factor_metrics_df, column_name, len(factor_metrics_df),
                                                   ascending)
                selected_factors = correlation_filter(candidate_factors, n_factors, factor_returns_df)
            else:
                # 差集筛选
                candidate_factors = filter_factors(factor_metrics_df, column_name, len(factor_metrics_df),
                                                   ascending)
                selected_factors1 = correlation_filter(candidate_factors, n_factors, factor_returns_df)
                selected_factors2 = correlation_filter(candidate_factors, n2_factors, factor_returns_df)
                selected_factors = list(set(selected_factors1) - set(selected_factors2))

        # 如果有选中的因子，则继续处理
        if len(selected_factors) > 0:
            method_list = [
                {'m': '单笔收益', 'r': False},
                {'m': '夏普', 'r': False},
                {'m': '最大回撤', 'r': True},
            ]

            # 处理每种权重方法
            for method_dict in method_list:
                strategy_returns, strategy_weight = weight_factors(
                    factor_returns_df, selected_factors, factor_metrics_df,
                    factor_results, method=method_dict['m'], reverse_weight=method_dict['r']
                )

                strategy_name_with_method = f'F#{strategy_name}_{method_dict["m"]}'
                strategy_weight['strategy'] = strategy_name_with_method  # type: ignore #
                rows.append(strategy_weight)
                strategy_returns_df[strategy_name_with_method] = strategy_returns
                print(f"创建策略 '{strategy_name_with_method}' 使用 {len(selected_factors)} 个因子")
        else:
            print(f"警告: 策略 '{strategy_name}' 未选择任何因子")

    # 合并策略权重
    strategy_weight_df = pd.concat(rows)

    def get_backtest_noparall(df, col):
        try:

            wb = WeightBacktest(df, digits=2, fee_rate=0, n_jobs=16, yearly_days=365)
            metrics = wb.stats
            del wb
            return pd.DataFrame([metrics]), col
        except:
            return None, col

    dfs = []
    strategy_weight_df['dt'] = pd.to_datetime(strategy_weight_df['dt'])
    for st in strategy_weight_df['strategy'].unique():
        evaluate_df, col = get_backtest_noparall(strategy_weight_df[strategy_weight_df['strategy'] == st],
                                                 f'{st}##全段')
        cols = col.split('##')
        evaluate_df.insert(0, 'factor', col)
        evaluate_df.insert(1, '分区', cols[1])

        dfs.append(evaluate_df)
        evaluate_df, col = get_backtest_noparall(strategy_weight_df[(strategy_weight_df['strategy'] == st) & (
                strategy_weight_df['dt'] >= pd.to_datetime('2024-01-01'))],
                                                 f'{st}##样本外')
        cols = col.split('##')
        evaluate_df.insert(0, 'factor', col)
        evaluate_df.insert(1, '分区', cols[1])

        dfs.append(evaluate_df)
    strategy_metrics_df = pd.concat(dfs)

    return strategy_metrics_df, strategy_weight_df, strategy_returns_df


def get_backtest(arg):
    """
    Processes a single factor's backtest.
    Receives a pre-formatted DataFrame and the original factor column name.

    Args:
        arg (tuple): (df_local, col)
            df_local (pd.DataFrame): DataFrame with columns ['dt', 'symbol', 'price', 'weight'].
            col (str): The original name of the factor column used as 'weight'.

    Returns:
        tuple: (pd.DataFrame(metrics), col) or (pd.DataFrame(), col) on error.
    """

    df_local, col = arg  # Unpack the DataFrame and column name

    try:
        # Instantiate and run the backtest exactly as before
        # n_jobs=1 within WeightBacktest as the parallelism is handled outside
        wb = WeightBacktest(df_local, digits=2, fee_rate=0, n_jobs=1, yearly_days=365)
        metrics = wb.stats  # Access the stats attribute

        # Convert metrics dictionary to a single-row DataFrame
        metrics_df = pd.DataFrame([metrics])

        del wb, df_local  # Explicitly delete large objects passed/created in worker
        gc.collect()

        return metrics_df, col  # Return the result and the column name

    except Exception as e:
        print(f"Error in get_backtest for factor {col}: {type(e).__name__} - {e}")
        # traceback.print_exc() # Uncomment for full traceback in worker errors
        # Return an empty DataFrame to signal failure gracefully
        return pd.DataFrame(), col


def evaluate_factor_rolling_old(df, sdt, edt, decay_rate=2.5, n_jobs=1, current_frequency='4小时'):
    factor_columns = [col for col in df.columns if col.startswith("F#")]

    eva_all_factor_dfs = []
    df = df[(df['dt'] >= sdt) & (df['dt'] <= edt)].copy()
    df = df.sort_values(by=['dt', 'symbol'])
    df['date_only'] = df['dt'].dt.date
    unique_dates = sorted(df['date_only'].unique())
    date_indices = {date: i for i, date in enumerate(unique_dates)}
    time_span = len(unique_dates) - 1
    if time_span == 0:  # 如果只有一个日期
        time_span = 1

    # 合并所有因子DataFrame
    # 使用更强的指数特性
    weights = {}
    for date, idx in date_indices.items():
        # 归一化日期索引到[0,1]范围
        normalized_idx = idx / time_span
        # 应用指数函数: exp(decay_rate * normalized_idx)
        weights[date] = np.exp(decay_rate * normalized_idx)

    # 创建日期到权重的映射Series，便于向量化操作
    weight_series = pd.Series(weights)

    # 方法1：使用 map 和向量化操作（非常高效）
    print("开始高效的时间加权计算...")
    # 创建权重映射列
    df['weight_factor'] = df['date_only'].map(weight_series)

    # 对所有因子列同时应用权重
    for col in tqdm(factor_columns, desc="因子时间加权（向量化）", unit="只"):
        # 直接使用向量化乘法，避免逐行处理
        df[col] = df[col] * df['weight_factor']

    column_blocks = split_columns_into_blocks(
        factor_columns,
        base_memory_percentage=0.3,  # 基于4小时数据的内存使用
        current_frequency=current_frequency
    )
    for block_idx, block_cols in enumerate(column_blocks):
        print(f"处理块 {block_idx + 1}/{len(column_blocks)} 包含 {len(block_cols)} 列")

        feature_list = [(pd.DataFrame({
            'dt': df['dt'],
            'symbol': df['symbol'],
            'price': df['price'],
            'weight': df[col]
        }), col) for col in block_cols]

        # 计算最佳的分块大小
        optimal_chunksize = max(1, min(chunksize_m, len(block_cols) // (n_jobs * chunksize_n)))
        evaluate_dfs = []
        with ProcessPoolExecutor(
                max_workers=n_jobs,
                mp_context=multiprocessing.get_context(mp_context)
        ) as executor:
            bar = tqdm(total=len(block_cols), desc=f"rolling块 {block_idx + 1} 收益计算")
            for evaluate_df, col in executor.map(get_backtest, feature_list, chunksize=optimal_chunksize):
                bar.update(1)
                evaluate_df.insert(0, 'factor', col)
                evaluate_dfs.append(evaluate_df)
            # 将当前块的结果添加到总结果
        eva_all_factor_dfs.extend(evaluate_dfs)

    eva_result_df = pd.concat(eva_all_factor_dfs)

    return eva_result_df


def evaluate_factor_rolling(df, sdt, edt, decay_rate=2.5, n_jobs=None, current_frequency='4小时', mp_context='spawn'):
    """
    分块计算因子滚动回测指标 (Parallelized version using ProcessPoolExecutor).

    Args:
        df (pd.DataFrame): 输入 DataFrame (包含 'dt', 'symbol', 'price', F#...).
        sdt (str or pd.Timestamp): Rolling period start date (inclusive).
        edt (str or pd.Timestamp): Rolling period end date (inclusive).
        decay_rate (float): Exponential decay rate for time weighting.
        n_jobs (int, optional): 并行进程数. Defaults to CPU count - 1.
        current_frequency (str): 用于 split_columns_into_blocks 的频率字符串.
        mp_context (str): Multiprocessing context ('fork', 'spawn'). Defaults to 'spawn'.

    Returns:
        pd.DataFrame: 包含所有因子滚动回测指标的DataFrame.
    """
    if n_jobs is None:
        n_jobs = max(1, multiprocessing.cpu_count() - 1)
    if n_jobs <= 0:
        n_jobs = 1

    print(f"启动因子滚动评估 (Parallelized, 线程数: {n_jobs}, Context: {mp_context})")
    start_time = pytime.time()
    df_weighted_subset = None  # Define outside try for finally block

    try:
        # --- 1. Input Validation and Data Filtering/Sorting ---
        required_cols = ['dt', 'symbol', 'price']  # Base columns needed
        factor_columns = sorted([col for col in df.columns if col.startswith("F#")])
        if not factor_columns:
            print("未找到因子列 (以'F#'开头).")
            return pd.DataFrame()

        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"输入DataFrame缺少必需列: {missing_cols}")

        print(f"找到 {len(factor_columns)} 个因子列.")

        # Convert dt and filter date range
        try:
            df['dt'] = pd.to_datetime(df['dt'])
            sdt_ts = pd.to_datetime(sdt)
            edt_ts = pd.to_datetime(edt)
            df_filtered = df[(df['dt'] >= sdt_ts) & (df['dt'] <= edt_ts)].copy()
            if df_filtered.empty:
                print(f"Warning: No data found between {sdt} and {edt}. Returning empty DataFrame.")
                return pd.DataFrame()
        except Exception as e:
            raise ValueError(f"Error filtering date range or converting 'dt': {e}")

        # Sort for consistent weighting
        df_filtered.sort_values(by=['dt', 'symbol'], inplace=True)

        # --- 2. Calculate Time Weights ---
        print("计算时间权重...")
        df_filtered['date_only'] = df_filtered['dt'].dt.date
        unique_dates = sorted(df_filtered['date_only'].unique())
        date_indices = {date: i for i, date in enumerate(unique_dates)}
        time_span = len(unique_dates) - 1
        if time_span <= 0: time_span = 1  # Avoid division by zero if only one date

        weights = {}
        for date, idx in date_indices.items():
            normalized_idx = idx / time_span
            weights[date] = np.exp(decay_rate * normalized_idx)

        weight_series = pd.Series(weights)
        df_filtered['time_weight_val'] = df_filtered['date_only'].map(weight_series)
        # Handle potential NaNs in weights if date mapping fails (shouldn't happen if logic is sound)
        df_filtered['time_weight_val'].fillna(1.0, inplace=True)  # Default weight 1 if mapping fails

        # --- 3. Apply Time Weights to Factor Columns ---
        print("应用时间权重到因子列...")
        # Select only base columns + factors for the subset to be weighted
        cols_to_process = required_cols + factor_columns
        df_weighted_subset = df_filtered[cols_to_process + ['time_weight_val']].copy()
        del df_filtered  # Free memory
        gc.collect()

        # Apply weights directly - this modifies df_weighted_subset
        for col in tqdm(factor_columns, desc="因子时间加权", unit="因子"):
            df_weighted_subset[col] = df_weighted_subset[col] * df_weighted_subset['time_weight_val']

        # Drop the temporary weight column after applying it
        df_weighted_subset.drop(columns=['time_weight_val'], inplace=True)

        # --- 4. Split Factor Columns (Names) ---
        print("拆分因子列...")
        try:
            column_blocks = split_columns_into_blocks(
                factor_columns,  # Split original names
                base_memory_percentage=0.3,
                current_frequency=current_frequency

            )
            if not column_blocks or not any(column_blocks):
                raise RuntimeError("split_columns_into_blocks returned no valid blocks.")
        except NameError:
            print("\nERROR: The required function 'split_columns_into_blocks' was not found.")
            raise
        except Exception as e:
            raise RuntimeError(f"Error splitting factor columns: {e}")

        n_blocks = len(column_blocks)
        print(f"拆分为 {n_blocks} 个块.")

        # --- 5. Process Each Factor Block ---
        eva_all_factor_dfs = []  # Store resulting metrics DataFrames

        for block_idx, block_cols in enumerate(column_blocks):
            if not block_cols:
                print(f"Skipping empty block {block_idx + 1}/{n_blocks}")
                continue

            print(f"\n处理块 {block_idx + 1}/{n_blocks} (因子数: {len(block_cols)})...")
            block_start_time = pytime.time()

            # --- a. Prepare Tasks for Workers ---
            # Each task: (DataFrame_with_weighted_factor, original_factor_name)
            tasks = []
            # Select base columns ONCE for this block's tasks
            base_data_block = df_weighted_subset[required_cols].copy()
            for col in block_cols:
                # Create the specific DataFrame for the worker:
                # Combine base data with the SINGLE weighted factor column
                df_for_worker = base_data_block.copy()  # Start with base columns
                # Add the already weighted factor column, rename it to 'weight'
                df_for_worker['weight'] = df_weighted_subset[col].copy()
                tasks.append((df_for_worker, col))  # Pass DF and original factor name
            del base_data_block  # Free memory for the block's base data copy
            gc.collect()

            # --- b. Execute in Parallel ---
            n_tasks = len(tasks)
            chunksize = max(1, n_tasks // (n_jobs * chunksize_n))  # Conservative chunking
            chunksize = min(chunksize, chunksize_m)  # Cap chunksize
            print(f"  提交 {n_tasks} 个任务 (chunksize={chunksize})...")

            evaluate_dfs_block = []  # Collect results for this block
            process_context = multiprocessing.get_context(mp_context)
            with ProcessPoolExecutor(
                    max_workers=n_jobs,
                    mp_context=process_context
            ) as executor:
                future_results = executor.map(
                    get_backtest,  # Use the same worker function
                    tasks,
                    chunksize=chunksize
                )
                # Collect valid results
                for metrics_df, factor_name in tqdm(future_results, total=n_tasks,
                                                    desc=f"Rolling块 {block_idx + 1} metric计算", leave=True):
                    if metrics_df is not None and isinstance(metrics_df, pd.DataFrame) and not metrics_df.empty:
                        # Add identifying column AFTER getting result back
                        metrics_df.insert(0, 'factor', factor_name)
                        evaluate_dfs_block.append(metrics_df)
                    # else: # Optional logging
                    #     print(f"  因子 {factor_name} 未返回有效结果.")

            eva_all_factor_dfs.extend(evaluate_dfs_block)
            del tasks, evaluate_dfs_block  # Free memory
            gc.collect()

            elapsed = pytime.time() - block_start_time
            print(f"块 {block_idx + 1} 处理完毕，耗时 {elapsed:.2f} 秒.")

        # --- 6. Combine Final Results ---
        if not eva_all_factor_dfs:
            print("未计算出任何有效回测结果.")
            eva_result_df = pd.DataFrame()
        else:
            print("\n合并所有因子回测结果...")
            try:
                eva_result_df = pd.concat(eva_all_factor_dfs, ignore_index=True)
                eva_result_df.sort_values(by=['factor'], inplace=True)  # Sort for consistency
            except Exception as concat_err:
                print(f"合并回测结果时出错: {concat_err}")
                traceback.print_exc()
                eva_result_df = pd.DataFrame()

    except Exception as main_e:
        print(f"\n因子滚动评估过程中发生严重错误: {main_e}")
        traceback.print_exc()
        eva_result_df = pd.DataFrame()
    finally:
        # --- 7. Final Cleanup ---
        if df_weighted_subset is not None:
            del df_weighted_subset
        gc.collect()
        print(f"\n因子滚动评估总耗时: {pytime.time() - start_time:.2f} 秒.")

    return eva_result_df


def ic_block(args):
    """
    向量化版本的IC计算函数

    参数:
    args: tuple，包含 (col, values)
        col: 因子列名
        values: 因子值数组

    返回:
    tuple: (ic_avg, col)
        ic_avg: 平均IC值
        col: 因子列名
    """
    col, df = args

    df = df.copy()
    corr = []
    for dt, dfg in df.groupby("dt"):
        dfg = dfg.copy().dropna(subset=[col, 'target_1'])

        if dfg.empty or len(dfg) <= 2:
            corr.append([dt, 0])
            # logger.warning(f"{dt} has no enough data, only {len(dfg)} rows")
        else:
            c = dfg[col].corr(dfg['target_1'], method='pearson')
            corr.append([dt, c])

    dft = pd.DataFrame(corr, columns=["dt", "ic"])

    if dft.empty:
        return 0, col

    dft = dft[~dft["ic"].isnull()].copy()
    ic_avg = dft["ic"].mean()

    return ic_avg, col


def ic_blocked(result_df, n_jobs, current_frequency='4小时'):
    # 获取所有因子列
    factor_cols = [col for col in result_df.columns if col.startswith('F#')]

    # 将列分成块
    column_blocks = split_columns_into_blocks(
        factor_cols,
        base_memory_percentage=0.60,  # 基于4小时数据的内存使用
        current_frequency=current_frequency
    )

    # 处理每个列块
    dict = {}
    for block_idx, block_cols in enumerate(column_blocks):
        print(f"计算ic {block_idx + 1}/{len(column_blocks)} 包含 {len(block_cols)} 列")

        feature_list = [(col, result_df[[col, 'dt', 'target_1']].copy()) for col in block_cols]

        # 计算最佳的分块大小
        optimal_chunksize = max(1, min(chunksize_m, len(block_cols) // (n_jobs * chunksize_n)))

        with ProcessPoolExecutor(
                max_workers=n_jobs,
                mp_context=multiprocessing.get_context(mp_context)

        ) as executor:
            bar = tqdm(total=len(block_cols), desc=f"块 {block_idx + 1} 计算ic")
            for ic_avg, col in executor.map(ic_block, feature_list, chunksize=optimal_chunksize):
                bar.update(1)
                dict[col] = ic_avg

    return dict


def filter_factor(factor_returns_df, factor_metrics_df):
    """高级因子筛选函数，提供多维度的筛选规则"""

    # 扩展筛选规则
    filtering_rules = [
        ('high20_单笔收益', '单笔收益', 20, 0, False),
        ('high20_年化', '年化', 20, 0, False),
        ('high20_夏普', '夏普', 20, 0, False),
        ('high20_日赢面', '日赢面', 20, 0, False),

        # 5. 平衡型筛选组合
        ('balanced_收益风险', '夏普', 30, 0, False),  # 使用balance_strategy处理

        # 6. 多维度组合筛选
        ('multi_dim_alpha', '夏普', 20, 0, False),  # 使用multi_dim_strategy处理
        ('multi_dim_stable', '夏普', 20, 0, False),  # 使用multi_dim_strategy处理

        # 高稳定性高收益组合
        ('balanced_stable_高收益', '夏普', 30, 0, False),  # 结合高日胜率、高日盈面、高非零覆盖
        # ('balanced_stable_低风险', '夏普', 30, 0, False),         # 结合低回撤、低波动、高胜率

        # # 风险调整收益组合
        # ('balanced_risk_adj_收益', '夏普', 30, 0, False),         # 结合高夏普、高卡玛、低回撤风险

        # # 综合评分组合
        # ('balanced_score_alpha', '夏普', 30, 0, False),           # 结合年化、夏普、卡玛、日盈面
        # ('balanced_score_stable', '夏普', 30, 0, False),          # 结合胜率、非零覆盖、回撤风险、波动率
        # # 防御性组合
        # ('balanced_defensive', '夏普', 30, 0, False),             # 结合低回撤、低波动、高胜率
        # # 进攻性组合
        # ('balanced_aggressive', '夏普', 30, 0, False),            # 结合高年化、高夏普、高卡玛
        # # 高频交易特征
        # ('high_freq', '夏普', 30, 0, False),             # 结合高胜率、高非零覆盖、高日盈面
        # # 低频交易特征
        # ('low_freq', '夏普', 30, 0, False),              # 结合高夏普、高卡玛、低波动
    ]

    # 存储筛选结果
    rows = {}

    # 处理常规筛选规则
    for strategy_name, column_name, n_factors, n2_factors, ascending in filtering_rules:
        if strategy_name.startswith('balanced_'):
            # 平衡型策略处理
            selected_factors = balance_strategy(factor_metrics_df, strategy_name, n_factors, factor_returns_df)
        elif strategy_name.startswith('multi_dim_'):
            # 多维度策略处理
            selected_factors = multi_dimensional_strategy(factor_metrics_df, strategy_name, n_factors,
                                                          factor_returns_df)
        else:
            # 常规筛选处理
            if n2_factors == 0:
                # 单指标筛选
                candidate_factors = filter_factors(factor_metrics_df, column_name, len(factor_metrics_df), ascending)
                selected_factors = correlation_filter(candidate_factors, n_factors, factor_returns_df)
            else:
                # 差集筛选
                candidate_factors = filter_factors(factor_metrics_df, column_name, len(factor_metrics_df), ascending)
                selected_factors1 = correlation_filter(candidate_factors, n_factors, factor_returns_df)
                selected_factors2 = correlation_filter(candidate_factors, n2_factors, factor_returns_df)
                selected_factors = list(set(selected_factors1) - set(selected_factors2))

        # 保存筛选结果
        if len(selected_factors) > 2:
            rows[strategy_name] = selected_factors
        else:
            print(f"警告: 策略 '{strategy_name}' 未选择任何因子")

    return rows


def balance_strategy(factor_metrics_df, strategy_name, n_factors, factor_returns_df):
    if strategy_name == 'balanced_收益风险':

        df_score = factor_metrics_df.copy()
        df_score['sharpe_rank'] = df_score['夏普'].rank(ascending=False)
        df_score['edge_rank'] = df_score['日赢面'].rank(ascending=False)
        df_score['dd_rank'] = df_score['最大回撤'].rank(ascending=True)

        # 计算总得分（可以调整权重）
        df_score['total_score'] = (
                df_score['sharpe_rank'] * 0.4 +
                df_score['edge_rank'] * 0.5 +
                df_score['dd_rank'] * 0.3
        )

        # 选择得分最高的因子
        top_factors = df_score.sort_values('total_score').head(int(n_factors * 10))['factor'].tolist()

        return correlation_filter(top_factors, n_factors, factor_returns_df)
    elif strategy_name == 'balanced_stable_稳健':
        df_score = factor_metrics_df.copy()
        df_score['dd_rank'] = df_score['最大回撤'].rank(ascending=True)
        df_score['sharpe_rank'] = df_score['夏普'].rank(ascending=False)
        df_score['return_rank'] = df_score['年化'].rank(ascending=False)
        df_score['dan_rank'] = df_score['单笔收益'].rank(ascending=False)
        df_score['total_score'] = (
                df_score['dd_rank'] * 0.3 +
                df_score['sharpe_rank'] * 0.3 +
                df_score['return_rank'] * 0.2 +
                df_score['dan_rank'] * 0.5
        )
        top_factors = df_score.sort_values('total_score').head(int(n_factors * 10))['factor'].tolist()

        return correlation_filter(top_factors, n_factors, factor_returns_df)
    elif strategy_name == 'balanced_stable_高收益':
        df_score = factor_metrics_df.copy()
        df_score['dd_rank'] = df_score['最大回撤'].rank(ascending=True)
        df_score['return_rank'] = df_score['年化'].rank(ascending=False)
        df_score['dan_rank'] = df_score['单笔收益'].rank(ascending=False)
        df_score['total_score'] = (
                df_score['dd_rank'] * 0.3 +
                df_score['return_rank'] * 0.5 +
                df_score['dan_rank'] * 0.5
        )

        # 选择得分最高的因子
        top_factors = df_score.sort_values('total_score').head(int(n_factors * 10))['factor'].tolist()

        return correlation_filter(top_factors, n_factors, factor_returns_df)


def multi_dimensional_strategy(factor_metrics_df, strategy_name, n_factors, factor_returns_df):
    """多维度评分策略，综合考虑多个指标"""

    if strategy_name == 'multi_dim_alpha':
        # 创建综合评分
        # 1. 标准化各指标
        metrics_to_use = ['年化', '夏普', '单笔收益']
        df_score = factor_metrics_df.copy()

        # 对正向指标进行排名（越高越好）
        for metric in metrics_to_use:
            df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=False)

        # 对负向指标进行排名（越低越好）
        for metric in ['最大回撤', '下行波动率']:
            df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=True)

        # 2. 计算综合得分
        rank_columns = [col for col in df_score.columns if col.endswith('_rank')]
        df_score['total_score'] = df_score[rank_columns].sum(axis=1)

        # 3. 选择得分最高的因子
        df_score = df_score.sort_values('total_score')
        top_factors = df_score['factor'].head(int(n_factors * 10)).tolist()

    elif strategy_name == 'multi_dim_stable':
        # 创建稳定性评分
        # 关注稳定性指标

        df_score = factor_metrics_df.copy()

        # 对正向指标进行排名
        for metric in ['夏普', '日胜率', '新高占比', '年化']:
            df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=False)

        # 对负向指标进行排名
        for metric in ['最大回撤', '新高间隔']:
            df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=True)

        # 计算综合得分
        rank_columns = [col for col in df_score.columns if col.endswith('_rank')]
        df_score['total_score'] = df_score[rank_columns].sum(axis=1)

        # 选择得分最高的因子
        df_score = df_score.sort_values('total_score')
        top_factors = df_score['factor'].head(int(n_factors * 10)).tolist()
    elif strategy_name == 'multi_dim_2dan':
        # 创建稳定性评分
        # 关注稳定性指标

        df_score = factor_metrics_df.copy()

        # 对正向指标进行排名
        for metric in ['夏普', '日胜率', '单笔收益', '年化']:
            df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=False)
        df_score[f'单笔收益_rank']=2 * df_score[f'单笔收益_rank']
        # 对负向指标进行排名
        for metric in ['最大回撤']:
            df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=True)

        # 计算综合得分
        rank_columns = [col for col in df_score.columns if col.endswith('_rank')]
        df_score['total_score'] = df_score[rank_columns].sum(axis=1)

        # 选择得分最高的因子
        df_score = df_score.sort_values('total_score')
        top_factors = df_score['factor'].head(int(n_factors * 10)).tolist()
    elif strategy_name == 'multi_dim_dan':
        # 创建稳定性评分
        # 关注稳定性指标

        df_score = factor_metrics_df.copy()

        # 对正向指标进行排名
        for metric in ['夏普', '日胜率', '单笔收益', '年化']:
            df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=False)

        # 对负向指标进行排名
        for metric in ['最大回撤']:
            df_score[f'{metric}_rank'] = df_score[metric].rank(ascending=True)

        # 计算综合得分
        rank_columns = [col for col in df_score.columns if col.endswith('_rank')]
        df_score['total_score'] = df_score[rank_columns].sum(axis=1)

        # 选择得分最高的因子
        df_score = df_score.sort_values('total_score')
        top_factors = df_score['factor'].head(int(n_factors * 10)).tolist()

    # 应用相关性过滤
    return correlation_filter(top_factors, n_factors, factor_returns_df)


class factor_to_strategy():

    def __init__(self, fre='4小时', method=None, method2=None, d='future', yinzi='4h', n_jobs=16, n_jobs2=16) -> None:
        self.reverse_dict = None
        self.filtered_factor_dict = None
        self.split_time = pd.to_datetime('2024-01-01')
        self.if_weight = False
        self.data = d
        self.factor_meric = None
        self.factor_result = None
        self.yinzi = yinzi
        self.evaluate_dfs = []
        self.factor_returns = None
        self.frequency = fre
        self.method = method
        self.method2 = method2
        self.n_jobs = n_jobs
        self.n_jobs2 = n_jobs2
        self.backtest = WeightBacktest
        self.input_file = f"{path_dr}/experiment/file/factor_results_{self.frequency}_{self.data}_{self.yinzi}.feather"
        self.reverse_file = f"{path_dr}/experiment/file/factor_reverse_results_{self.frequency}_{self.data}_{self.yinzi}.feather"
        self.re_dict_file = f"{path_dr}/experiment/file/factor_reverse_dict_{self.frequency}_{self.data}_{self.yinzi}.pkl"
        self.output_file = f"{path_dr}/experiment/file/factor_returns_results_{self.method}_{self.frequency}_{self.data}_{self.yinzi}"
        self.factor_results_normal_file = f"{path_dr}/experiment/file/factor_results_normal_{self.method}_{self.frequency}_{self.data}_{self.yinzi}.feather"
        self.metrics_output_file = f"{path_dr}/experiment/file/factor_risk_metrics_{self.method}_{self.frequency}_{self.data}_{self.yinzi}.feather"
        self.strategy_file = f"{path_dr}/experiment/str/strategy_{self.method}_{self.frequency}_{self.data}_{self.yinzi}"
        self.strategy_weight_file = f"{path_dr}/experiment/str_weight/strategy_weight_{self.method}_{self.frequency}_{self.data}_{self.yinzi}"
        self.strategy_return_df_file = f"{path_dr}/experiment/str_weight/strategy_return_{self.method}_{self.frequency}_{self.data}_{self.yinzi}"
        self.filter_factor_result_cross_normal = f"{path_dr}/experiment/train_and_test/factor_result_cross_normal_{self.method}_{self.frequency}_{self.data}_{self.yinzi}"
        self.fee_rate = 0
        self.digits = 2

    def generate_strategy_with_rolling(self, factor_returns_df, factor_results, train_day, test_day, decay_rate, sel):
        """在generate_strategy_combinations中添加分块处理"""

        filtering_rules = [
            # ('high20_单笔收益', '单笔收益', 20, 0, False),
            ('high20_年化', '年化', 20, 0, False),
            ('high20_夏普', '夏普', 20, 0, False),
            ('high20_日赢面', '日赢面', 20, 0, False),

            # 5. 平衡型筛选组合
            ('balanced_收益风险', '夏普', 25, 0, False),  # 使用balance_strategy处理

            # 6. 多维度组合筛选
            ('multi_dim_alpha', '夏普', 25, 0, False),  # 使用multi_dim_strategy处理
            ('multi_dim_stable', '夏普', 25, 0, False),
            ('multi_dim_dan', '夏普', 25, 0, False), # 使用multi_dim_strategy处理

            # 高稳定性高收益组合
            ('balanced_stable_高收益', '夏普', 25, 0, False),  # 结合高日胜率、高日盈面、高非零覆盖

        ]

        # 参数设置
        training_days = train_day  # 每次训练使用的天数
        prediction_days = test_day  # 每次预测的天数
        step_days = test_day  # 滑动窗口步长

        # 预处理数据
        factor_returns_df['dt'] = pd.to_datetime(factor_returns_df['dt'])
        factor_results['dt'] = pd.to_datetime(factor_results['dt'])
        factor_returns_df = factor_returns_df.sort_values(by=['dt'], ascending=True)
        factor_results = factor_results.sort_values(by=['dt', 'symbol'], ascending=True)
        initial_date = factor_returns_df['dt'].iloc[0]
        # initial_date=pd.to_datetime('2024-06-01')
        end_date = factor_returns_df['dt'].iloc[-1]

        # 创建空的DataFrame来存储所有循环的结果
        all_strategy_returns_df = pd.DataFrame()
        all_strategy_weights = []

        sdt = initial_date
        iteration = 0

        while True:
            iteration += 1
            print(f"处理循环 {iteration}: 从 {sdt} 开始")

            edt = sdt + timedelta(days=training_days)
            pdt = edt + timedelta(days=prediction_days)

            if edt >= end_date:
                print(f"训练结束日期 {edt} 超过了数据结束日期 {end_date}，停止循环")
                break

            # 计算当前训练窗口的因子评价指标
            if sel == 'changed':

                factor_result, r_dict = process_auto_reverse_blocked(
                    factor_results[(factor_results['dt'] >= sdt) & (factor_results['dt'] <= pdt)], self.n_jobs,
                    current_frequency='4小时', time=edt)

                factor_result = self.factor_result.copy()
                factor_result.drop(columns=r_dict['drop'], inplace=True)
                cols = [col for col in factor_result.columns if col.startswith("F#")]
                for col in cols:
                    if col in r_dict['reverse'] and col not in self.reverse_dict['reverse']:
                        factor_result[col] = -factor_result[col]
                        factor_returns_df[col] = -factor_returns_df[col]
                    elif col in self.reverse_dict['reverse'] and col not in r_dict['reverse']:
                        factor_result[col] = -factor_result[col]
                        factor_returns_df[col] = -factor_returns_df[col]

            else:
                factor_result = factor_results
            factor_metrics_df = evaluate_factor_rolling_old(factor_result, sdt, edt, decay_rate, self.n_jobs,
                                                            self.frequency)

            # 创建当前预测窗口的策略收益DataFrame
            current_strategy_returns_df = pd.DataFrame()
            current_strategy_returns_df['dt'] = factor_returns_df['dt']
            current_strategy_returns_df = current_strategy_returns_df[(current_strategy_returns_df['dt'] >= edt) &
                                                                      (current_strategy_returns_df['dt'] < pdt)]

            # 处理常规筛选规则
            rows = []
            for strategy_name, column_name, n_factors, n2_factors, ascending in filtering_rules:
                if strategy_name.startswith('balanced_'):
                    # 平衡型策略处理
                    selected_factors = balance_strategy(factor_metrics_df, strategy_name, n_factors,
                                                        factor_returns_df[(factor_returns_df['dt'] >= sdt) &
                                                                          (factor_returns_df['dt'] < edt)])
                elif strategy_name.startswith('multi_dim_'):
                    # 多维度策略处理
                    selected_factors = multi_dimensional_strategy(factor_metrics_df, strategy_name, n_factors,
                                                                  factor_returns_df[(factor_returns_df['dt'] >= sdt) &
                                                                                    (factor_returns_df['dt'] < edt)])
                else:
                    # 常规筛选处理
                    if n2_factors == 0:
                        # 单指标筛选
                        candidate_factors = filter_factors(factor_metrics_df, column_name, len(factor_metrics_df),
                                                           ascending)
                        selected_factors = correlation_filter(candidate_factors, n_factors,
                                                              factor_returns_df[(factor_returns_df['dt'] >= sdt) &
                                                                                (factor_returns_df['dt'] < edt)])
                    else:
                        # 差集筛选
                        candidate_factors = filter_factors(factor_metrics_df, column_name, len(factor_metrics_df),
                                                           ascending)
                        selected_factors1 = correlation_filter(candidate_factors, n_factors,
                                                               factor_returns_df[(factor_returns_df['dt'] >= sdt) &
                                                                                 (factor_returns_df['dt'] < edt)])
                        selected_factors2 = correlation_filter(candidate_factors, n2_factors,
                                                               factor_returns_df[(factor_returns_df['dt'] >= sdt) &
                                                                                 (factor_returns_df['dt'] < edt)])
                        selected_factors = list(set(selected_factors1) - set(selected_factors2))

                # 如果有选中的因子，则继续处理
                if len(selected_factors) > 0:
                    method_list = [
                        {'m': '单笔收益', 'r': False},
                        {'m': '夏普', 'r': False},
                        {'m': 'equal', 'r': True},
                    ]

                    # 处理每种权重方法
                    for method_dict in method_list:
                        # 获取当前循环的因子权重和收益
                        strategy_returns, strategy_weight = weight_factors(
                            factor_returns_df[(factor_returns_df['dt'] >= edt) & (factor_returns_df['dt'] < pdt)],
                            selected_factors,
                            factor_metrics_df,
                            factor_result[(factor_result['dt'] >= edt) & (factor_result['dt'] < pdt)],
                            method=method_dict['m'],
                            reverse_weight=method_dict['r']
                        )

                        strategy_name_with_method = f'F#{strategy_name}_{method_dict["m"]}'

                        # 添加循环信息到权重DataFrame
                        strategy_weight['strategy'] = strategy_name_with_method

                        # 存储当前循环的权重信息
                        rows.append(strategy_weight)

                        # 将策略收益添加到当前循环的结果中
                        current_strategy_returns_df[strategy_name_with_method] = strategy_returns
                else:
                    print(f"警告: 策略 '{strategy_name}' 未选择任何因子")

            # 将当前循环的权重添加到总权重列表
            all_strategy_weights.extend(rows)

            # 将当前循环的收益结果与总收益结果合并
            if all_strategy_returns_df.empty:
                all_strategy_returns_df = current_strategy_returns_df.copy()
            else:
                # 合并当前循环的结果，按日期对齐
                all_strategy_returns_df = pd.concat([all_strategy_returns_df, current_strategy_returns_df])
                # 删除可能的重复行
                all_strategy_returns_df = all_strategy_returns_df.drop_duplicates(subset=['dt'], keep='last')
                # 按日期重新排序
                all_strategy_returns_df = all_strategy_returns_df.sort_values(by=['dt'])

            # 更新开始日期，滑动到下一个窗口
            sdt = sdt + timedelta(days=step_days)
            print(f"完成循环 {iteration}, 新的开始日期: {sdt}")
            print("-" * 50)

        # 将所有权重转换为一个DataFrame
        strategy_weight_df = pd.concat(all_strategy_weights)
        strategy_weight_df.sort_values(by=['dt', 'symbol'])

        dfs = []

        for st in strategy_weight_df['strategy'].unique():
            evaluate_df, col = get_backtest_noparall(strategy_weight_df[strategy_weight_df['strategy'] == st], st)
            evaluate_df.insert(0, 'factor', col)
            dfs.append(evaluate_df)

        strategy_metrics_df = pd.concat(dfs)

        return strategy_metrics_df, strategy_weight_df, all_strategy_returns_df

    def reverse_factor(self):
        try:
            print(f"检查 {self.reverse_file} 是否存在...")
            self.factor_result = pd.read_feather(self.reverse_file)
            import pickle
            with open(self.re_dict_file, 'rb') as f:
                self.reverse_dict = pickle.load(f)
            print(f"从 {self.reverse_file} 加载现有的 factor_results")

        except FileNotFoundError:
            print(f"未找到文件 {self.reverse_file}. 计算所有因子...")
            self.factor_result["dt"] = pd.to_datetime(self.factor_result["dt"])
            df = self.factor_result.copy()

            # 使用分块方法处理因子自动反转
            self.factor_result, self.reverse_dict = process_auto_reverse_blocked(df, self.n_jobs,
                                                                                 current_frequency=self.frequency)
            cols = [f for f in self.factor_result.columns if f.startswith('F#')]
            d_cols = list(set(cols) - set(self.reverse_dict['drop']))
            del df
            print(f"总因子数量{len(cols)},剩余{len(d_cols)}")
            import pickle
            with open(self.re_dict_file, 'wb') as f:
                pickle.dump(self.reverse_dict, f)
            print(f"保存结果到 {self.reverse_file}...")

            self.factor_result.to_feather(self.reverse_file)
            print("完成!")

    def cal_factor(self):
        try:
            print(f"检查 {self.input_file} 是否存在...")
            self.factor_result = pd.read_feather(self.input_file)
            print(f"从 {self.input_file} 加载现有的 factor_results")

        except FileNotFoundError:
            print(f"未找到文件 {self.input_file}. 计算所有因子...")
            self.factor_result = calculate_factor(self.frequency, self.n_jobs2, self.data, self.yinzi,'20210101','20260101')

            # 保存结果
            self.factor_result.to_feather(self.input_file)
            print(f"将 factor_result 保存到 {self.input_file}...")

    def evaluate_factor(self):
        try:
            print(f"检查 {self.metrics_output_file} 是否存在...")
            self.factor_meric = pd.read_feather(self.metrics_output_file)
            print(f"从 {self.metrics_output_file} 加载现有的风险指标")
        except FileNotFoundError:
            if_weight = True
            print(f"未找到文件 {self.metrics_output_file}. 评估因子...")
            if self.frequency == "2小时":
                n = 8
            elif self.frequency == "60分钟":
                n = 2
            elif self.frequency == "30分钟":
                n = 2
            else:
                n = 16
            self.factor_meric = self.evaluate_factor_blocked(
                self.factor_result, n_jobs=n,
                current_frequency=self.frequency
            )
            # 保存到文件
            print(f"保存结果到 {self.metrics_output_file}...")
            self.factor_meric.to_feather(self.metrics_output_file)
            print("完成!")

    def nor_factor(self):
        try:
            print(f"检查 {self.factor_results_normal_file} 是否存在...")
            self.factor_result = pd.read_feather(self.factor_results_normal_file)
            print(f"从 {self.factor_results_normal_file} 加载现有的因子标准化值")
        except FileNotFoundError:
            factor_cols = [col for col in self.factor_result.columns if
                           col.startswith('F#')]  # type: ignore #
            self.factor_result = self.factor_result.replace(True, 1)  # type: ignore #
            self.factor_result = self.factor_result.replace(False, 0)

            # 使用分块方法进行因子标准化
            self.factor_result = normalize_column_parallel_blocked(
                self.factor_result, factor_cols, method=self.method,  # type: ignore #
                n_jobs=self.n_jobs, current_frequency=self.frequency
            )  # type: ignore #

            print(f"保存结果到 {self.factor_results_normal_file}...")
            self.factor_result.to_feather(self.factor_results_normal_file)
            print("完成!")

    def cal_return(self, selec=None):
        # 检查因子收益文件是否存在
        try:
            print(f"检查 {self.output_file}_{selec}.feather 是否存在...")
            self.factor_returns = pd.read_feather(f'{self.output_file}_{selec}.feather')
            print(f"从 {self.output_file}_{selec}.feather 加载现有的因子收益")
            self.if_weight = False
        except FileNotFoundError:
            self.if_weight = True
            print(f"未找到文件 {self.output_file}_{selec}.feather 计算因子收益...")
            print(f"从 {self.output_file}_{selec}.feather 读取数据...")

            # 使用分块方法计算因子收益
            self.factor_returns = calculate_factor_returns_blocked(
                self.factor_result, n_jobs=self.n_jobs,
                current_frequency=self.frequency, split_time=self.split_time
            )

            self.factor_returns.to_feather(f'{self.output_file}_{selec}.feather')

    def evaluate_factor_blocked(self, df, n_jobs=None, current_frequency='4小时'):
        """
        分块计算因子回测指标 (Parallelized version using ProcessPoolExecutor).

        Args:
            df (pd.DataFrame): 输入 DataFrame (包含 'dt', 'symbol', 'price', 'target_1', F#...).
            split_time (str or pd.Timestamp): The time to split training data (inclusive).
            n_jobs (int, optional): 并行进程数. Defaults to CPU count - 1.
            current_frequency (str): 用于 split_columns_into_blocks 的频率字符串.
            mp_context (str): Multiprocessing context ('fork', 'spawn'). Defaults to 'spawn'.
                               'spawn' is generally safer across platforms.

        Returns:
            pd.DataFrame: 包含所有因子回测指标的DataFrame.
        """
        if n_jobs is None:
            n_jobs = max(1, multiprocessing.cpu_count() - 1)
        if n_jobs <= 0:
            n_jobs = 1

        print(f"启动因子评估 (Parallelized, 线程数: {n_jobs}, Context: {mp_context})")
        start_time = pytime.time()

        try:
            # --- 1. Input Validation and Data Prep ---
            required_cols = ['dt', 'symbol', 'price', 'target_1']  # Checking 'target_1' as per original
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"输入DataFrame缺少必需列: {missing_cols}")

            factor_columns = [col for col in df.columns if col.startswith("F#")]
            factor_columns = list(set(factor_columns) - set(self.reverse_dict['drop']))
            if not factor_columns:
                print("未找到因子列 (以'F#'开头).")
                return pd.DataFrame()

            print(f"找到 {len(factor_columns)} 个因子列.")

            # Prepare the training data subset (df1)
            try:
                df['dt'] = pd.to_datetime(df['dt'])  # Ensure dt is datetime

                # Filter data based on the split time
                df1 = df[df['dt'] <= self.split_time].copy()
                if df1.empty:
                    print(f"Warning: No data found in df for dt <= {self.split_time}. Returning empty DataFrame.")
                    return pd.DataFrame()

                # Select only base columns needed by the worker + all factor columns initially
                base_cols_for_worker = ['dt', 'symbol', 'price']
                df1_subset = df1[base_cols_for_worker + factor_columns].copy()
                del df1  # Free memory early
                gc.collect()

            except Exception as e:
                raise ValueError(f"Error preparing training data subset (df1): {e}")

            # --- 2. Split Factor Columns ---
            print("拆分因子列...")
            try:
                # Pass n_jobs to splitter if it needs it for calculations
                column_blocks = split_columns_into_blocks(
                    factor_columns,
                    base_memory_percentage=0.5,  # As per original code
                    current_frequency=current_frequency
                )
                if not column_blocks or not any(column_blocks):
                    raise RuntimeError("split_columns_into_blocks returned no valid blocks.")
            except NameError:
                print("\nERROR: The required function 'split_columns_into_blocks' was not found.")
                print("Please define it or import it.")
                raise
            except Exception as e:
                raise RuntimeError(f"Error splitting factor columns: {e}")

            n_blocks = len(column_blocks)
            print(f"拆分为 {n_blocks} 个块.")

            # --- 3. Process Each Factor Block ---
            eva_all_factor_dfs = []  # Store resulting metrics DataFrames

            for block_idx, block_cols in enumerate(column_blocks):
                if not block_cols:
                    print(f"Skipping empty block {block_idx + 1}/{n_blocks}")
                    continue

                print(f"\n处理块 {block_idx + 1}/{n_blocks} (因子数: {len(block_cols)})...")
                block_start_time = pytime.time()

                # --- a. Prepare Tasks for Workers ---
                # Each task is a tuple: (DataFrame_for_worker, original_factor_name)
                tasks = []
                for col in block_cols:
                    # Create the specific DataFrame needed by get_backtest for THIS factor
                    df_for_worker = df1_subset[base_cols_for_worker + [col]].copy()
                    df_for_worker.rename(columns={col: 'weight'}, inplace=True)
                    tasks.append((df_for_worker, col))

                # --- b. Execute in Parallel ---
                n_tasks = len(tasks)
                # A reasonable default chunksize calculation
                chunksize = max(1, n_tasks // (n_jobs * chunksize_n))  # More conservative chunking
                chunksize = min(chunksize, chunksize_m)  # Cap chunksize
                print(f"  提交 {n_tasks} 个任务 (chunksize={chunksize})...")

                evaluate_dfs_block = []  # Collect results for this block
                # Get the specified multiprocessing context
                process_context = multiprocessing.get_context(mp_context)
                with ProcessPoolExecutor(
                        max_workers=n_jobs,
                        mp_context=process_context  # Use the specified context
                ) as executor:
                    # Use executor.map for potentially better memory management with large iterables
                    future_results = executor.map(
                        get_backtest,  # Target worker function (unchanged)
                        tasks,
                        chunksize=chunksize
                    )
                    # Collect valid results using tqdm for progress
                    for metrics_df, factor_name in tqdm(future_results, total=n_tasks,
                                                        desc=f"样本内块 {block_idx + 1} metric计算", leave=True):
                        # Check if a valid, non-empty DataFrame was returned
                        if metrics_df is not None and isinstance(metrics_df, pd.DataFrame) and not metrics_df.empty:
                            # Add identifying columns here before appending
                            metrics_df.insert(0, '样本区', '样本内')  # As per original logic
                            metrics_df.insert(0, 'factor', factor_name)
                            evaluate_dfs_block.append(metrics_df)
                        # else: # Optional logging for skipped/failed factors
                        #     print(f"  因子 {factor_name} 未返回有效结果或结果为空.")

                # Extend the main results list with the results from this block
                eva_all_factor_dfs.extend(evaluate_dfs_block)
                del tasks, evaluate_dfs_block  # Explicitly free memory from task list and block results
                gc.collect()

                elapsed = pytime.time() - block_start_time
                print(f"块 {block_idx + 1} 处理完毕，耗时 {elapsed:.2f} 秒.")

            # --- 4. Combine Final Results ---
            if not eva_all_factor_dfs:
                print("未计算出任何有效回测结果.")
                eva_result_df = pd.DataFrame()
            else:
                print("\n合并所有因子回测结果...")
                try:
                    # Concatenate results. ignore_index=True since each result DF is a single row.
                    eva_result_df = pd.concat(eva_all_factor_dfs, ignore_index=True)
                    # Optional: Sort results for consistency
                    eva_result_df.sort_values(by=['factor'], inplace=True)
                except Exception as concat_err:
                    print(f"合并回测结果时出错: {concat_err}")
                    traceback.print_exc()
                    eva_result_df = pd.DataFrame()  # Return empty on merge error

        except Exception as main_e:
            print(f"\n因子评估过程中发生严重错误: {main_e}")
            traceback.print_exc()
            eva_result_df = pd.DataFrame()  # Return empty on major failure
        finally:
            # Cleanup the potentially large subset DataFrame
            if 'df1_subset' in locals():
                del df1_subset
            gc.collect()
            print(f"\n因子评估总耗时: {pytime.time() - start_time:.2f} 秒.")

        return eva_result_df

    def generate_simple_strategy(self, method, decay_rate=2.5, train_day=90, test_day=7, sel='changed'):

        if method == 'rolling':
            try:
                print(f"检查 {self.strategy_file}_{method}_{train_day}_{test_day}_{decay_rate}_{sel}.csv 是否存在...")
                strategy_df = pd.read_csv(
                    f'{self.strategy_file}_{method}_{train_day}_{test_day}_{decay_rate}_{sel}.csv')
                print(f"从 {self.strategy_file}_{method}_{train_day}_{test_day}_{decay_rate}_{sel}.csv 加载策略")
                print(strategy_df)
            except FileNotFoundError:
                if sel == 'changed':
                    df_result = pd.read_feather(self.input_file)
                else:
                    df_result = self.factor_result
                strategy_df, strategy_weight_df, strategy_return_df = self.generate_strategy_with_rolling(
                    self.factor_returns, df_result, train_day, test_day, decay_rate, sel)
                strategy_df.to_csv(f'{self.strategy_file}_{method}_{train_day}_{test_day}_{decay_rate}_{sel}.csv',
                                   encoding='utf-8-sig', index=False)
                strategy_weight_df.to_feather(
                    f'{self.strategy_weight_file}_{method}_{train_day}_{test_day}_{decay_rate}_{sel}.feather')
                strategy_return_df.to_feather(
                    f'{self.strategy_return_df_file}_{method}_{train_day}_{test_day}_{decay_rate}_{sel}.feather')
        elif method == 'blocked':
            strategy_df, strategy_weight_df, strategy_return_df = generate_strategy_with_blocking(
                self.factor_returns, self.factor_meric[self.factor_meric['样本区'] == '样本内'], self.factor_result,
                self.n_jobs)
            strategy_df.to_csv(f'{self.strategy_file}_{method}.csv', encoding='utf-8-sig', index=False)
            strategy_weight_df.to_feather(f'{self.strategy_weight_file}_{method}.feather')
            strategy_return_df.to_feather(f'{self.strategy_return_df_file}_{method}.feather')

        # 保存策略结果

    def get_filter_factor_weight(self):
        self.filtered_factor_dict = filter_factor(self.factor_returns, self.factor_meric)
        for key, value in self.filtered_factor_dict.items():
            value.extend(['dt', 'symbol', 'price', 'target_1'])
            df = self.factor_result[value]  # type: ignore #
            train_df = df[df['dt'] <= self.split_time]
            test_df = df[df['dt'] > self.split_time]
            train_df.to_feather(f'{self.filter_factor_result_cross_normal}_{key}_train.feather')
            test_df.to_feather(f'{self.filter_factor_result_cross_normal}_{key}_use.feather')

    def generate_filter_factor_return(self):
        from skfolio import RiskMeasure
        from skfolio.optimization import MeanRisk, ObjectiveFunction
        from sklearn.model_selection import train_test_split
        from skfolio import PerfMeasure, RatioMeasure
        self.filtered_factor_dict = filter_factor(self.factor_returns, self.factor_meric)
        import plotly.io as pio
        for key, value in self.filtered_factor_dict.items():
            value.append('dt')
            df = self.factor_returns[value].set_index('dt')  # type: ignore #
            X_train, X_test = train_test_split(df, test_size=0.33, shuffle=False)
            model = MeanRisk(
                risk_measure=RiskMeasure.STANDARD_DEVIATION,
                objective_function=ObjectiveFunction.MINIMIZE_RISK,
                efficient_frontier_size=30,
                portfolio_params=dict(name="Variance"),
            )
            model.fit(X_train)
            print(model.weights_.shape)
            population_train = model.predict(X_train)
            population_test = model.predict(X_test)
            population_train.set_portfolio_params(tag="Train")  # type: ignore #
            population_test.set_portfolio_params(tag="Test")  # type: ignore #

            population = population_train + population_test  # type: ignore #
            pio.templates.default = "plotly"
            fig = population.plot_measures(
                x=RiskMeasure.ANNUALIZED_STANDARD_DEVIATION,
                y=PerfMeasure.ANNUALIZED_MEAN,
                color_scale=RatioMeasure.ANNUALIZED_SHARPE_RATIO,
                hover_measures=[RiskMeasure.MAX_DRAWDOWN, RatioMeasure.ANNUALIZED_SORTINO_RATIO],
            )  # type: ignore #

            fig.show()

    def optimize_factor_weights(self):
        """
        使用多种优化模型和参数优化来找到每个因子组的最优权重

        采用以下策略：
        1. 多种优化模型比较（最大夏普比率、最小CVaR、方差优化等）
        2. 正则化参数优化（L1和L2正则化）
        3. 滚动窗口交叉验证
        4. 参数网格搜索
        """
        import os
        import pandas as pd
        from tqdm import tqdm
        import plotly.io as pio

        # 导入所需的skfolio库
        from skfolio import RiskMeasure, Population, PerfMeasure, RatioMeasure
        from skfolio.optimization import (MeanRisk, ObjectiveFunction, InverseVolatility, RiskBudgeting,
                                          NestedClustersOptimization, EqualWeighted, )
        from skfolio.model_selection import WalkForward, cross_val_predict
        from skfolio.distance import KendallDistance
        from skfolio.cluster import HierarchicalClustering, LinkageMethod
        from sklearn.cluster import KMeans
        from skfolio.prior import EmpiricalPrior
        from skfolio.moments import DenoiseCovariance, ShrunkMu

        # 确保目录存在
        if not os.path.exists(
                'C:/Users/Administrator/PycharmProjects/experiment/optimization_results'):
            os.makedirs('C:/Users/Administrator/PycharmProjects/experiment/optimization_results')

        # 获取筛选出的因子分组
        self.filtered_factor_dict = filter_factor(self.factor_returns, self.factor_meric)

        # 滚动窗口设置
        cv = WalkForward(train_size=360, test_size=30)

        # 存储所有优化结果
        results = {}

        # 对每个因子分组进行优化
        for group_name, factors in tqdm(self.filtered_factor_dict.items(), desc="优化因子权重"):
            print(f"\n正在优化因子组: {group_name}")

            # 准备数据
            factors_copy = factors.copy()
            factors_copy.append('dt')
            self.factor_returns['dt'] = pd.to_datetime(self.factor_returns['dt'])  # type: ignore #
            df = self.factor_returns[factors_copy].set_index('dt')  # type: ignore #

            # 划分训练集和测试集
            # X_train, X_test = train_test_split(df, test_size=0.33, shuffle=False)

            X_train = df[df.index <= pd.to_datetime('2024-01-01')].copy()
            X_test2 = df[df.index > pd.to_datetime('2024-01-01')].copy()
            X_test1 = df[df.index > pd.to_datetime('2023-10-01')].copy()
            # 定义不同的模型
            models = {
                # 1. 最大夏普比率模型
                "MaxSharpe": MeanRisk(
                    risk_measure=RiskMeasure.STANDARD_DEVIATION,
                    objective_function=ObjectiveFunction.MAXIMIZE_RATIO,  # 添加年化天数
                    portfolio_params=dict(name="Max Sharpe")
                ),
                "MaxSharpe_shrinkage": MeanRisk(
                    risk_measure=RiskMeasure.VARIANCE,
                    objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                    prior_estimator=EmpiricalPrior(
                        mu_estimator=ShrunkMu(), covariance_estimator=DenoiseCovariance()
                    ),
                    portfolio_params=dict(name="Max Sharpe - ShrunkMu & DenoiseCovariance"),
                ),

                # 2. 最小条件风险价值模型
                # "MinCVaR": MeanRisk(
                #     risk_measure=RiskMeasure.CVAR,
                #     objective_function=ObjectiveFunction.MINIMIZE_RISK,
                #     portfolio_params=dict(name="Min CVaR")
                # ),
                # "MinCVaR_shrinkage": MeanRisk(
                #     risk_measure=RiskMeasure.CVAR,
                #     objective_function=ObjectiveFunction.MINIMIZE_RISK,
                #     prior_estimator=EmpiricalPrior(
                #         covariance_estimator=ShrunkCovariance(shrinkage=0.9)
                #     ),
                #     portfolio_params=dict(name="Min CVaR - ShrunkCovariance"),
                # ),

                # 3. 逆波动率模型（基准）
                "InverseVol": InverseVolatility(
                    portfolio_params=dict(name="Inverse Vol"),

                ),

                "Equal_Weight": EqualWeighted(
                    portfolio_params=dict(name="Equal Weight"),
                ),

                # "Risk_Parity":RiskBudgeting(
                #     risk_measure=RiskMeasure.VARIANCE,
                #     portfolio_params=dict(name="Risk Parity - Variance"),
                # ),

                # "Risk_Parity_Covariance_shrinkage":RiskBudgeting(
                #     risk_measure=RiskMeasure.VARIANCE,
                #     prior_estimator=EmpiricalPrior(
                #         covariance_estimator=ShrunkCovariance(shrinkage=0.9)
                #     ),
                #     portfolio_params=dict(name="Risk Parity - Covariance Shrinkage"),
                # ),

                # "NCO-1": NestedClustersOptimization(
                #     inner_estimator=MeanRisk(
                #         objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                #         risk_measure=RiskMeasure.VARIANCE,
                #     ),
                #     outer_estimator=RiskBudgeting(risk_measure=RiskMeasure.CVAR),
                #     n_jobs=-1,
                #     portfolio_params=dict(name="NCO-1"),
                # ),
                "NCO-1_shrinkage": NestedClustersOptimization(
                    inner_estimator=MeanRisk(
                        objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                        risk_measure=RiskMeasure.VARIANCE,
                        prior_estimator=EmpiricalPrior(
                            mu_estimator=ShrunkMu(), covariance_estimator=DenoiseCovariance()
                        ),
                    ),
                    outer_estimator=RiskBudgeting(risk_measure=RiskMeasure.CVAR),
                    n_jobs=-1,
                    portfolio_params=dict(name="NCO-1_shrinkage"),
                ),
                # "NCO-2": NestedClustersOptimization(
                #     inner_estimator=MeanRisk(
                #         objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                #         risk_measure=RiskMeasure.VARIANCE,
                #     ),
                #     outer_estimator=RiskBudgeting(risk_measure=RiskMeasure.CVAR),
                #     clustering_estimator=HierarchicalClustering(
                #         linkage_method=LinkageMethod.SINGLE,
                #     ),
                #     n_jobs=-1,
                #     portfolio_params=dict(name="NCO-2"),
                # ),
                "NCO-2_shrinkage": NestedClustersOptimization(
                    inner_estimator=MeanRisk(
                        objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                        risk_measure=RiskMeasure.VARIANCE,
                        prior_estimator=EmpiricalPrior(
                            mu_estimator=ShrunkMu(), covariance_estimator=DenoiseCovariance()
                        ),
                    ),
                    outer_estimator=RiskBudgeting(risk_measure=RiskMeasure.CVAR),
                    clustering_estimator=HierarchicalClustering(
                        linkage_method=LinkageMethod.SINGLE,
                    ),
                    n_jobs=-1,
                    portfolio_params=dict(name="NCO-2_shrinkage"),
                ),
                # "NCO-3": NestedClustersOptimization(
                #     inner_estimator=MeanRisk(
                #         objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                #         risk_measure=RiskMeasure.VARIANCE,
                #     ),
                #     outer_estimator=RiskBudgeting(risk_measure=RiskMeasure.CVAR),
                #     distance_estimator=KendallDistance(absolute=True),
                #     n_jobs=-1,
                #     portfolio_params=dict(name="NCO-3"),
                # ),
                "NCO-3_shrinkage": NestedClustersOptimization(
                    inner_estimator=MeanRisk(
                        objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                        risk_measure=RiskMeasure.VARIANCE,
                        prior_estimator=EmpiricalPrior(
                            mu_estimator=ShrunkMu(), covariance_estimator=DenoiseCovariance()
                        ),
                    ),
                    outer_estimator=RiskBudgeting(risk_measure=RiskMeasure.CVAR),
                    distance_estimator=KendallDistance(absolute=True),
                    n_jobs=-1,
                    portfolio_params=dict(name="NCO-3_shrinkage"),
                ),
                # "NCO-4": NestedClustersOptimization(
                #     inner_estimator=MeanRisk(
                #         objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                #         risk_measure=RiskMeasure.VARIANCE,
                #     ),
                #     outer_estimator=RiskBudgeting(risk_measure=RiskMeasure.CVAR),
                #     clustering_estimator=KMeans(n_init="auto"),
                #     n_jobs=-1,
                #     portfolio_params=dict(name="NCO-4"),
                # ),
                "NCO-4_shrinkage": NestedClustersOptimization(
                    inner_estimator=MeanRisk(
                        objective_function=ObjectiveFunction.MAXIMIZE_RATIO,
                        risk_measure=RiskMeasure.VARIANCE,
                        prior_estimator=EmpiricalPrior(
                            mu_estimator=ShrunkMu(), covariance_estimator=DenoiseCovariance()
                        ),
                    ),
                    outer_estimator=RiskBudgeting(risk_measure=RiskMeasure.CVAR),
                    clustering_estimator=KMeans(n_init="auto"),
                    n_jobs=-1,
                    portfolio_params=dict(name="NCO-4_shrinkage"),
                ),

                # 4. 均值-方差模型（效率前沿）
                # "MeanVar": MeanRisk(
                #     risk_measure=RiskMeasure.VARIANCE,
                #     efficient_frontier_size=30,
                #     portfolio_params=dict(name="Variance")
                # ),

                # 5. l1正则化模型
                "L1_Reg": MeanRisk(
                    risk_measure=RiskMeasure.VARIANCE,

                    l1_coef=0.001,

                    portfolio_params=dict(name="Mean-Variance", tag="L1 Regularization")
                ),

                # 6. l2正则化模型
                "L2_Reg": MeanRisk(
                    risk_measure=RiskMeasure.VARIANCE,

                    l1_coef=0,
                    l2_coef=0.001,

                    portfolio_params=dict(name="Mean-Variance", tag="L2 Regularization")
                )

            }

            # 存储不同模型的结果
            model_results = {}
            model_populations = []
            model_results_2 = {}
            # 训练并评估每个基础模型
            for model_name, model in models.items():
                print(f"训练模型: {model_name}")

                if model_name in ["MaxSharpe", "MinCVaR", "InverseVol", "L1_Reg", "L2_Reg", "Equal_Weight",
                                  "Risk_Parity", "Risk_Parity_Covariance_shrinkage", "MaxRETURN", "MaxSharpe_shrinkage",
                                  "MinCVaR_shrinkage"]:
                    try:
                        # 首先尝试使用原始参数
                        pred = cross_val_predict(
                            model,
                            X_test1,
                            cv=cv,
                            portfolio_params=dict(name=model_name)
                        )
                        print(f"模型 {model_name} 优化成功")
                        model_results[model_name] = pred
                        model_populations.append(pred)
                    except Exception as e:
                        print(f"模型 {model_name} 优化失败: {e}")
                        print(f"跳过模型 {model_name} 的优化")
                        continue

                elif model_name in ["NCO-1", "NCO-2", "NCO-3", "NCO-4", "NCO-1_shrinkage", "NCO-2_shrinkage",
                                    "NCO-3_shrinkage", "NCO-4_shrinkage"]:
                    try:
                        model.fit(X_train)
                        pred = model.predict(X_test2)
                        model_results[model_name] = pred
                        model_populations.append(pred)
                    except Exception as e:
                        print(f"模型 {model_name} 优化失败: {e}")
                        print(f"跳过模型 {model_name} 的优化")
                        continue

            # #参数网格搜索（仅对部分模型进行网格搜索以提高效率）
            # try:

            #     print("进行网格搜索优化参数...")
            #     model_nco = NestedClustersOptimization(
            #         inner_estimator=MeanRisk(), clustering_estimator=HierarchicalClustering()
            #     )
            #     grid_search_hrp = GridSearchCV(
            #         estimator=model_nco,
            #         cv=cv,
            #         n_jobs=-1,
            #         param_grid={
            #             "inner_estimator__risk_measure": [RiskMeasure.VARIANCE, RiskMeasure.CVAR],
            #             "outer_estimator": [
            #                 EqualWeighted(),
            #                 RiskBudgeting(risk_measure=RiskMeasure.CVAR),
            #             ],
            #             "clustering_estimator__linkage_method": [
            #                 LinkageMethod.SINGLE,
            #                 LinkageMethod.WARD,
            #             ],
            #             "distance_estimator": [PearsonDistance(), KendallDistance()],
            #         },
            #     )
            #     model_name="NCO-best"
            #     grid_search_hrp.fit(X_train)
            #     model_nco = grid_search_hrp.best_estimator_
            #     pred = cross_val_predict(
            #         model_nco,
            #         X_test,
            #         cv=cv,
            #         portfolio_params=dict(name="NCO-best"),
            #     )
            #     model_results[model_name] = pred
            #     model_populations.append(pred)

            # #     # 创建参考模型
            # #     ref_model = MeanRisk(
            # #         risk_measure=RiskMeasure.VARIANCE,
            # #         objective_function=ObjectiveFunction.MAXIMIZE_RETURN,
            # #         portfolio_params=dict(name="l1_l2_best")
            # #     )

            # #     # 定义网格搜索
            # #     grid_search = GridSearchCV(
            # #         estimator=ref_model,
            # #         cv=cv,
            # #         n_jobs=-1,
            # #         param_grid={
            # #             "l1_coef": [0.001, 0.01, 0.1],
            # #             "l2_coef": [0.001, 0.01, 0.1],
            # #         }
            # #     )

            # #     # 执行网格搜索
            # #     model_name="l1_l2_best"
            # #     grid_search.fit(X_train)
            # #     best_model = grid_search.best_estimator_
            # #     print(f"最佳模型参数: {grid_search.best_params_}")

            # #     pred = cross_val_predict(
            # #         best_model,
            # #         X_test,
            # #         cv=cv,
            # #         portfolio_params=dict(name=model_name)
            # #             )
            # #     model_results[model_name] = pred
            # #     model_populations.append(pred)

            # except Exception as e:
            #     print(f"网格搜索时出错: {e}")

            # 创建完整的投资组合种群
            population = Population(model_populations)

            # 保存结果
            results[group_name] = {
                "models": model_results,
                "population": population
            }

            # 创建可视化
            try:
                print("生成可视化结果...")

                pio.templates.default = "plotly"
                fig = population.plot_measures(
                    x=RiskMeasure.ANNUALIZED_STANDARD_DEVIATION,
                    y=PerfMeasure.ANNUALIZED_MEAN,
                    color_scale=RatioMeasure.ANNUALIZED_SHARPE_RATIO,
                    hover_measures=[
                        RiskMeasure.MAX_DRAWDOWN,
                        RatioMeasure.ANNUALIZED_SORTINO_RATIO
                    ],
                    title=f"因子组 {group_name} 的不同优化策略比较"
                )

                # 保存图表
                fig.write_html(
                    f'C:/Users/Administrator/PycharmProjects/experiment/optimization_results/{group_name}_{self.frequency}_{self.method}_optimization.html')

                # 保存权重
                for model_name, model_data in model_results.items():
                    weights = model_data.weights_per_observation
                    weights.to_csv(
                        f'C:/Users/Administrator/PycharmProjects/experiment/optimization_substr_weight/{group_name}_{model_name}_{self.frequency}_{self.method}_weights.csv',
                        encoding='utf-8-sig', index=False)
            except Exception as e:
                print(f"生成可视化时出错: {e}")

        # 保存总体结果
        self.optimization_results = results

        # 创建模型比较报告
        try:
            print("生成模型比较报告...")

            comparison_data = []
            # 创建一个空的DataFrame来存储所有return_df
            all_returns_df = pd.DataFrame()

            for group_name, group_results in results.items():
                for model_name, model_data in group_results["models"].items():
                    return_df = model_data.returns_df
                    column_name = f"{group_name}_{model_name}"
                    all_returns_df[column_name] = return_df
                    comparison_data.append({
                        "group": group_name,
                        "model": model_name,
                        "sharpe": model_data.annualized_sharpe_ratio,
                        "max_dd": model_data.max_drawdown,
                        "volatility": model_data.annualized_standard_deviation,
                        "return": model_data.annualized_mean,
                        "sortino": model_data.annualized_sortino_ratio,
                        "calmar": model_data.calmar_ratio
                    })

            if comparison_data:
                comparison_df = pd.DataFrame(comparison_data)
                comparison_df.to_csv(
                    f'C:/Users/Administrator/PycharmProjects/experiment/optimization_COMPARISON/model_comparison_{self.frequency}_{self.method}.csv',
                    encoding='utf-8-sig', index=False)

            all_returns_df.to_csv(
                f'C:/Users/Administrator/PycharmProjects/experiment/optimization_substr_return/all_returns_{self.frequency}_{self.method}.csv',
                encoding='utf-8-sig', index=True)

        except Exception as e:
            print(f"生成比较报告时出错: {e}")

        print("所有因子分组优化完成，结果已保存到 ./optimization_results/ 目录")
        return results

    def portfolio_optimization(self, df, pred_col='predicted_return', weight_bounds=(-0.4, 0.4), max_turnover=0.5,
                               max_cumulative_turnover=None, lookback_periods=None, target_return=None,
                               risk_constraint=None, cov_matrix=None, initial_weights=None):
        """
        使用cvxpy进行投资组合优化，在每个时间点基于预测收益分配权重

        参数:
        df (pd.DataFrame): 包含dt, symbol和预测列的数据框
        pred_col (str): 预测收益列名，默认'predicted_return'
        weight_bounds (tuple): 权重上下限，默认(0, 0.1)
        max_turnover (float): 每期最大换手率，默认0.5
        max_cumulative_turnover (float): 与过去N期最大累计换手率，默认None
        lookback_periods (int): 累计换手率的历史期数，默认None
        target_return (float): 目标收益率，默认None
        risk_constraint (float): 最大风险约束，默认None
        cov_matrix (dict): 每个时间点的协方差矩阵字典，默认None
        initial_weights (dict): 初始权重字典，默认为全0权重

        返回:
        pd.DataFrame: 包含优化后权重的数据框
        """
        import cvxpy as cp
        import pandas as pd
        import numpy as np

        # 确保日期格式正确
        df = df.copy()
        df['dt'] = pd.to_datetime(df['dt'])

        # 排序数据
        df = df.sort_values(['dt', 'symbol'])

        # 初始化权重字典和结果列
        all_weights = {}
        df['weight'] = 0.0

        # 获取所有唯一日期和品种
        all_dates = sorted(df['dt'].unique())
        all_symbols = sorted(df['symbol'].unique())
        n_symbols = len(all_symbols)

        # 修改点1: 初始化权重为0
        if initial_weights is None:
            prev_weights = {symbol: 0 for symbol in all_symbols}
        else:
            prev_weights = initial_weights

        # 存储历史权重
        weights_history = {symbol: [] for symbol in all_symbols}
        for symbol in all_symbols:
            weights_history[symbol].append(prev_weights.get(symbol, 0))

        # 对每个日期进行优化
        for date in all_dates:
            print(date)
            date_data = df[df['dt'] == date]

            # 获取当前日期的品种列表
            current_symbols = date_data['symbol'].values
            current_symbols_set = set(current_symbols)

            # 如果当前日期的品种较少，添加缺失品种
            missing_symbols = [s for s in all_symbols if s not in current_symbols_set]

            # 创建预测收益向量
            returns_dict = date_data.set_index('symbol')[pred_col].to_dict()

            # 修改点2: 对缺失的品种，设置预测收益为0
            for symbol in missing_symbols:
                returns_dict[symbol] = 0.0

            # 按所有品种排序的收益向量
            pred_returns = np.array([returns_dict.get(symbol, 0.0) for symbol in all_symbols])

            # 创建优化变量
            weights = cp.Variable(n_symbols)

            # 定义目标函数 - 最大化预期收益
            objective = cp.Maximize(pred_returns @ weights)

            # 定义约束条件
            constraints = []

            # 修改点3: 权重和为0（这可能会导致所有权重为0，请确认这是你想要的）

            constraints.append(cp.sum(weights) == 0)
            constraints.append(cp.sum(cp.abs(weights)) <= 1)
            # constraints.append(cp.sum(weights) <= 1)
            # 权重上下限

            constraints.append(weights >= weight_bounds[0])
            constraints.append(weights <= weight_bounds[1])

            # 换手率约束
            prev_weights_vector = np.array([prev_weights.get(symbol, 0) for symbol in all_symbols])
            if max_turnover is not None:
                turnover = cp.sum(cp.abs(weights - prev_weights_vector))
                constraints.append(turnover <= max_turnover)
            # if max_turnover is not None:
            #     # 对每个资产的权重变化添加限制
            #     for i in range(len(prev_weights_vector)):
            #         constraints.append(cp.abs(weights[i] - prev_weights_vector[i]) <= max_turnover)
            # 累计换手率约束
            # if max_cumulative_turnover is not None and lookback_periods is not None:
            #     for period in range(1, min(lookback_periods, len(weights_history[all_symbols[0]])) + 1):
            #         historical_weights = np.array([weights_history[symbol][-period] for symbol in all_symbols])
            #         cumulative_turnover = cp.sum(cp.abs(weights - historical_weights))
            #         constraints.append(cumulative_turnover <= max_cumulative_turnover)
            if max_cumulative_turnover is not None and lookback_periods is not None:
                maxturnover = 0
                for i, symbol in enumerate(all_symbols):
                    # 计算每个资产在lookback_periods内的历史累积turnover
                    historical_cumulative_turnover = 0
                    available_periods = min(lookback_periods, len(weights_history[symbol]))

                    # 计算历史累积turnover (已经发生的变化)
                    for period in range(1, available_periods):
                        current_weight = weights_history[symbol][-(period)]
                        previous_weight = weights_history[symbol][
                            -(period + 1)] if period + 1 <= available_periods else 0
                        historical_cumulative_turnover += abs(current_weight - previous_weight)

                    # 当前权重相对于最近一次权重的变化
                    current_turnover = cp.abs(weights[i] - weights_history[symbol][-1])

                    # 限制历史累积turnover加上当前turnover不超过最大值
                    maxturnover = maxturnover + historical_cumulative_turnover + current_turnover
                constraints.append(maxturnover <= max_cumulative_turnover)
            # 风险约束（如果提供协方差矩阵）
            if risk_constraint is not None and cov_matrix is not None and date in cov_matrix:
                date_cov = cov_matrix[date]
                # 确保符合当前品种顺序
                ordered_cov = np.zeros((n_symbols, n_symbols))

                # 这里需要根据实际情况调整协方差矩阵的处理
                for i, sym_i in enumerate(all_symbols):
                    for j, sym_j in enumerate(all_symbols):
                        if sym_i in date_cov and sym_j in date_cov[sym_i]:
                            ordered_cov[i, j] = date_cov[sym_i][sym_j]

                portfolio_risk = cp.quad_form(weights, ordered_cov)
                constraints.append(portfolio_risk <= risk_constraint)

            # 目标收益约束（如果指定）
            if target_return is not None:
                constraints.append(pred_returns @ weights >= target_return)

            # 创建和求解问题
            problem = cp.Problem(objective, constraints)
            try:
                problem.solve(solver=cp.ECOS)

                # 检查是否成功求解
                if problem.status in ["optimal", "optimal_inaccurate"]:
                    # 更新权重
                    new_weights = {symbol: float(weights.value[i]) for i, symbol in enumerate(all_symbols)}
                    all_weights[date] = new_weights

                    # 更新历史权重
                    for symbol in all_symbols:
                        weights_history[symbol].append(new_weights[symbol])

                    # 存储当前的权重作为下一期的前期权重
                    prev_weights = new_weights

                    # 将权重添加到数据框
                    for symbol, weight in new_weights.items():
                        idx = df[(df['dt'] == date) & (df['symbol'] == symbol)].index
                        if len(idx) > 0:
                            df.loc[idx, 'weight'] = weight
                else:
                    print(f"警告: 在 {date} 上的优化未能成功: {problem.status}")
                    # 如果优化失败，使用前一期权重
                    all_weights[date] = prev_weights
                    for symbol in all_symbols:
                        weights_history[symbol].append(prev_weights[symbol])

                    # 将前期权重添加到数据框
                    for symbol, weight in prev_weights.items():
                        idx = df[(df['dt'] == date) & (df['symbol'] == symbol)].index
                        if len(idx) > 0:
                            df.loc[idx, 'weight'] = weight
            except Exception as e:
                print(f"错误: 在 {date} 上的优化失败: {e}")
                # 如果出错，使用前一期权重
                all_weights[date] = prev_weights
                for symbol in all_symbols:
                    weights_history[symbol].append(prev_weights[symbol])

                # 将前期权重添加到数据框
                for symbol, weight in prev_weights.items():
                    idx = df[(df['dt'] == date) & (df['symbol'] == symbol)].index
                    if len(idx) > 0:
                        df.loc[idx, 'weight'] = weight

        # 计算每期的实际换手率
        # df['prev_weight'] = 0.0
        # for date_idx in range(1, len(all_dates)):
        #     prev_date = all_dates[date_idx - 1]
        #     curr_date = all_dates[date_idx]
        #
        #     prev_weights_dict = all_weights[prev_date]
        #
        #     for symbol, weight in prev_weights_dict.items():
        #         idx = df[(df['dt'] == curr_date) & (df['symbol'] == symbol)].index
        #         if len(idx) > 0:
        #             df.loc[idx, 'prev_weight'] = weight
        #
        # df['turnover'] = abs(df['weight'] - df['prev_weight'])

        return df


if __name__ == "__main__":
    # '日线','12小时','8小时','6小时','4小时','60分钟','30分钟','zscore','max_min','sum','zscore_clip','zscore_maxmin','rank','rank_balanced','rank_c'
    for time in ['2小时','1小时']:
        for m in ['zscore_maxmin']:
            for data in ['spot']:
                for yinzi in ['4h']:
                    for selec in ['fix']:
                        if selec == 'fix':
                            c = factor_to_strategy(fre=time, method=m, method2=m, d=data, yinzi=yinzi,
                                                   n_jobs=num_process,
                                                   n_jobs2=num_process_2)
                            c.cal_factor()
                            c.reverse_factor()
                            c.nor_factor()
                            c.cal_return(selec)
                            c.generate_simple_strategy('rolling', 4, 360, 7, selec)
                            c.optimize_factor_weights()
                        else:
                            c = factor_to_strategy(fre=time, method=m, method2=m, d=data, yinzi=yinzi,
                                                   n_jobs=num_process,
                                                   n_jobs2=num_process_2)
                            c.cal_factor()
                            c.reverse_factor()
                            c.nor_factor()
                            c.cal_return(selec)
                            c.evaluate_factor()
                            c.generate_simple_strategy('rolling', 4, 720, 720, selec)
                            # c.optimize_factor_weights()