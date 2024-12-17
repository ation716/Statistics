from nt import times

import matplotlib.pyplot as plt
import numpy as np
from functools import wraps
from datetime import datetime
import matplotlib.dates as mdates
import os
import re

from pandas import pivot


# 创建一个包含装饰器画图表的类
class PlotDecorators:
    @staticmethod
    def line(func):
        @wraps(func)
        def wrapper(ax, *args, **kwargs):
            data = func(ax, *args, **kwargs)  # 调用原函数
            x = data.get('x')
            y = data.get('y')
            ax.plot(x, y, label='Line Plot')  # 绘制折线图
        return wrapper

    @staticmethod
    def avg(func):
        def wrapper(ax, *args, **kwargs):
            data = func(ax, *args, **kwargs)  # 调用原函数
            x = data.get('x')
            y = data.get('y')
            avg_y = np.mean(y)
            # 绘制平均线
            ax.hlines(y=avg_y, xmin=x[0], xmax=x[-1], color='red', linestyle='--', label='Average Line')
        return wrapper

    @staticmethod
    def scatter(func):
        @wraps(func)
        def wrapper(ax, *args, **kwargs):
            data = func(ax, *args, **kwargs)  # 调用原函数
            x = data.get('x')
            y = data.get('y')
            ax.scatter(x, y, s= 4, color='blue', label='Scatter Plot')
        return wrapper

    # 自动绘制函数
    def create_plots(*plot_funcs_and_data):
        # 计算需要的图形数量
        num_plots = len(plot_funcs_and_data)

        # 动态计算子图布局
        cols = 2  # 假设每行两个子图
        rows = (num_plots + 1) // cols  # 计算行数，向上取整

        # 创建图形对象
        fig, axes = plt.subplots(rows, cols, figsize=(12, rows * 6))

        # 展开axes二维数组，方便循环
        axes = axes.flatten()

        # 绘制每个图形
        for i, (plot_func, data) in enumerate(plot_funcs_and_data):
            ax = axes[i]
            plot_func(ax)
            # 设置标题和标签
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_title(f'Data Set {i + 1}')
            ax.legend()
            # 在每个子图上旋转X轴标签
            ax.tick_params(axis='x', rotation=45)

        # 如果子图不满，则隐藏多余的子图
        for i in range(num_plots, len(axes)):
            axes[i].axis('off')

        # 自动调整布局
        plt.tight_layout()
        plt.show()


# 创建一个从日志中获取数据的类
class LogData:
    def get_log_data(self):
        """
        获取普通的log中数据
        :return:
        """
        # 定义日志文件的目录路径
        # directory_path = r'C:\.SeerRobotics\rdscore\diagnosis\log'
        directory_path = r'D:\log'

        # 给定的时间范围，格式为：'YYYY-MM-DD HH:MM:SS'
        start_time_str = '2024-11-20 14:15:41'
        end_time_str = '2024-11-20 14:39:00'

        # 将字符串时间转换为 datetime 对象
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

        # 正则表达式，用于提取时间和 total 值
        log_pattern = r'\[(\d{6} \d{6}\.\d{3})\].*\[TCost\].*Total\|(\d,+)'

        # 存储数据：时间和对应的 total 值
        times = []
        total_values = []

        # 获取目录下所有的日志文件
        file_paths = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if
                      filename.endswith('.log')]

        # 逐个处理文件
        for file_path in file_paths:
            # 从文件名中提取时间，假设文件名格式为 rdscore_YYYY-MM-DD_HH-MM-SS.MS.log
            filename = os.path.basename(file_path)
            time_str = filename.split('_')[1] + ' ' + filename.split('_')[2].split('.')[0].replace('-', ':')  # 提取时间部分
            file_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

            # 检查文件时间是否在指定的时间范围内
            if start_time <= file_time <= end_time:
                with open(file_path, 'r', errors='ignore') as file:
                    for line in file:
                        # 使用正则表达式查找匹配的时间和 total 值
                        match = re.search(log_pattern, line)
                        if match:
                            # 提取时间和 total 值
                            timestamp_str = match.group(1)
                            total_value_str = match.group(2)
                            timestamp = datetime.strptime(timestamp_str, '%y%m%d %H%M%S.%f')
                            total_value = int(total_value_str.replace(",", ""))  # 去除逗号并转换为整数
                            times.append(timestamp)
                            total_values.append(total_value)
                            # 将数据添加到列表中
                            if total_value < 1000:
                                times.append(timestamp)
                                total_values.append(total_value)
        return total_values,times
    def get_rhcr_log_data(self):
        """
        获取rhcr中日志的数据
        :return:
        """
        pass


# 示例1：装饰了折线图和均值线
# @PlotDecorators.line
@PlotDecorators.avg
@PlotDecorators.scatter
def plot_data1(ax):
    total_values, times = LogData().get_log_data()
    return {'x':times,'y':total_values}

# 示例2：装饰了散点图
@PlotDecorators.line
@PlotDecorators.avg
def plot_data2(x, y, ax):
    pass  # 实际绘图由装饰器处理

# 示例3：装饰了折线图和散点图
# @PlotDecorators.line
@PlotDecorators.avg
# @PlotDecorators.scatter
def plot_data3(x, y, ax):
    pass  # 实际绘图由装饰器处理

# 示例3：装饰了折线图和散点图
@PlotDecorators.line
@PlotDecorators.avg
def plot_data4(x, y, ax):

    pass  # 实际绘图由装饰器处理

# 示例3：装饰了折线图和散点图
@PlotDecorators.line
@PlotDecorators.avg
def plot_data5(x, y, ax):
    pass  # 实际绘图由装饰器处理

# 示例3：装饰了折线图和散点图
@PlotDecorators.line
@PlotDecorators.avg
def plot_data6(x, y, ax):
    pass  # 实际绘图由装饰器处理

if __name__ == '__main__':
    # total_values, times = LogData().get_log_data()
    PlotDecorators.create_plots(
        (plot_data1,None)
    )