import matplotlib.pyplot as plt
import numpy as np
from functools import wraps
from datetime import datetime
import matplotlib.dates as mdates
import os
import re

# 创建一个包含装饰器画图表的类
class PlotDecorators:
    @staticmethod
    def line(func):
        """
        画折线
        """
        @wraps(func)
        def wrapper(ax, *args, **kwargs):
            data = func(ax, *args, **kwargs)  # 调用原函数
            if (data.get('x') is None) or (data.get('y') is None):
                raise Exception('画折线时，x / y不能为空')
            x = data.get('x')
            y = data.get('y')
            ax.plot(x, y, label='Line Plot')  # 绘制折线图
            return data  # 返回数据
        return wrapper

    @staticmethod
    def avg_y(func):
        """
        画均值线 - 画横线，即y轴值的均值
        """
        @wraps(func)
        def wrapper(ax, *args, **kwargs):
            data = func(ax, *args, **kwargs)  # 调用原函数
            if data.get('y') is None:
                raise Exception('画y均值线时,y不能为空')
            x = data.get('x')
            y = data.get('y')
            if x is None:
                x=[0,1]
            avg_y = np.mean(y)
            # 绘制平均线
            ax.hlines(y=avg_y, xmin=x[0], xmax=x[-1], color='red', linestyle='--', label='Average Line')
            return data  # 返回数据
        return wrapper

    @staticmethod
    def avg_x(func):
        """
        画均值线  - 画竖线，即x轴值的均值
        """

        @wraps(func)
        def wrapper(ax, *args, **kwargs):
            data = func(ax, *args, **kwargs)  # 调用原函数
            if data.get('x') is None:
                raise Exception('画x均值线时,x不能为空')
            x = data.get('x')
            y = data.get('y')
            if y is None:
                y = [0, 1]
            if isinstance(x[0], datetime):
                # 将 datetime 对象转换为时间戳（秒数）
                timestamps = np.array([dt.timestamp() for dt in x])
                # 计算时间戳的平均值
                avg_timestamp = np.mean(timestamps)

                # 将平均时间戳转换回 datetime
                avg_x = datetime.fromtimestamp(avg_timestamp)
            else:
                avg_x = np.mean(x)
            # 绘制平均线
            ax.vlines(x=avg_x, ymin=y[0], ymax=y[-1], color='red', linestyle='--', label='Average Line')
            return data  # 返回数据

        return wrapper

    @staticmethod
    def scatter(func):
        @wraps(func)
        def wrapper(ax, *args, **kwargs):
            data = func(ax, *args, **kwargs)  # 调用原函数
            if (data.get('x') is None) or (data.get('y') is None):
                raise Exception('画折线时，x / y不能为空')
            x = data.get('x')
            y = data.get('y')
            ax.scatter(x, y, s=4, color='blue', label='Scatter Plot')
            return data  # 返回数据
        return wrapper

    # 自动绘制函数
    @staticmethod
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
        for i, plot_func in enumerate(plot_funcs_and_data):
            ax = axes[i]
            plot_func(ax)  # 执行装饰器修饰后的函数
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

