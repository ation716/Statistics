from turtledemo.penrose import start

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime,timedelta

from scipy.ndimage import label
from sklearn.preprocessing import StandardScaler
from functools import wraps
from sklearn.linear_model import LinearRegression
from scipy.interpolate import CubicSpline


def data_deduplication(x, y):
    # 使用 zip 创建一对一的 (x, y) 对，并转换为字典去重
    xy_pairs = list(zip(x, y))

    # 通过 dict 去重（会保留第一个出现的元素）
    unique_xy_pairs = dict()  # 创建一个空字典来保存唯一的 (x, y) 对
    for xi, yi in xy_pairs:
        if xi not in unique_xy_pairs:
            unique_xy_pairs[xi] = yi

    # 解压唯一的 (x, y) 对
    x = list(unique_xy_pairs.keys())
    y = list(unique_xy_pairs.values())
    return x, y

# 创建一个包含装饰器画图表的类
class PlotDecorators:

    @staticmethod
    def line(label='',color='blue',linestyle='-',zorder=2):
        """
        画折线
        """
        def decorator(func):
            @wraps(func)
            def wrapper(ax, *args, **kwargs):
                data = func(ax, *args, **kwargs)  # 调用原函数
                if (data.get('x') is None) or (data.get('y') is None):
                    raise Exception('画折线时，x / y不能为空')
                x = data.get('x')
                y = data.get('y')
                ax.plot(x, y, color=color, label=label,linestyle=linestyle,zorder=zorder)  # 绘制折线图
                return data  # 返回数据
            return wrapper
        return decorator

    @staticmethod
    def avg_y(label='',color='red',linestyle='--',zorder=2):
        """
        画均值线 - 画横线，即y轴值的均值
        """
        def decorator(func):
            @wraps(func)
            def wrapper(ax, *args, **kwargs):
                data = func(ax, *args, **kwargs)  # 调用原函数
                if data.get('y') is None:
                    raise Exception('画y均值线时,y不能为空')
                x = data.get('x')
                y = data.get('y')
                if x is None:
                    x=[0,1]
                if isinstance(y[0], datetime):
                    # 将 datetime 对象转换为时间戳（秒数）
                    timestamps = np.array([dt.timestamp() for dt in y])
                    # 计算时间戳的平均值
                    avg_timestamp = np.mean(timestamps)

                    # 将平均时间戳转换回 datetime
                    avg_y = datetime.fromtimestamp(avg_timestamp)
                else:
                    avg_y = np.mean(y)
                x.sort()
                # 绘制平均线
                ax.hlines(y=avg_y, xmin=x[0], xmax=x[-1], color=color, linestyle=linestyle, label=label,zorder=zorder)
                return data  # 返回数据
            return wrapper
        return decorator

    @staticmethod
    def avg_x(label='',color='red',linestyle='--',zorder=2):
        """
        画均值线  - 画竖线，即x轴值的均值
        """
        def decorator(func):
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
                y.sort()
                # 绘制平均线
                ax.vlines(x=avg_x, ymin=y[0], ymax=y[-1], color=color, linestyle=linestyle, label=label,zorder=zorder)
                return data  # 返回数据
            return wrapper
        return decorator

    @staticmethod
    def scatter(label='',color='green',zorder=10,s=4,alpha=0.5,edgecolors=None):
        """
        画散点图
        """
        def decorator(func):
            @wraps(func)
            def wrapper(ax, *args, **kwargs):
                data = func(ax, *args, **kwargs)  # 调用原函数
                if (data.get('x') is None) or (data.get('y') is None):
                    raise Exception('画折线时，x / y不能为空')
                x = data.get('x')
                y = data.get('y')
                ax.scatter(x, y, s=s, color=color, label=label,zorder=zorder,alpha=alpha,edgecolors=edgecolors)
                return data  # 返回数据
            return wrapper
        return decorator

    @staticmethod
    def least_square_method(label='',color='purple',linestyle='-',zorder=5):
        """
        线性最小二乘法 - 画趋势图
        """
        def decorator(func):
            @wraps(func)
            def wrapper(ax, *args, **kwargs):
                data = func(ax, *args, **kwargs)  # 调用原函数
                if (data.get('x') is None) or (data.get('y') is None):
                    raise Exception('画图时（线性最小二乘法），x / y不能为空')
                x = np.array(data.get('x'))
                y = np.array(data.get('y'))

                # 处理 x 为 datetime 类型的情况
                if len(x) > 0 and isinstance(x[0], datetime):
                    # 将 datetime 转换为秒数（相对于第一个时间点）
                    x_numeric = np.array([(dt - x[0]).total_seconds() for dt in x]).reshape(-1, 1)
                else:
                    # 如果 x 不是 datetime 类型，按常规方式使用数值类型
                    x_numeric = x.reshape(-1, 1)

                # 处理 y 为 datetime 类型的情况
                if len(y) > 0 and isinstance(y[0], datetime):
                    # 将 datetime 转换为秒数（相对于第一个时间点）
                    y_numeric = np.array([(dt - y[0]).total_seconds() for dt in y]).reshape(-1, 1)
                else:
                    # 如果 y 不是 datetime 类型，按常规方式使用数值类型
                    y_numeric = y.reshape(-1, 1)

                # 使用 scikit-learn 进行线性回归拟合
                model = LinearRegression()
                model.fit(x_numeric, y_numeric)  # 使用 x 和 y 的数值进行回归拟合

                # 获取拟合结果
                m = model.coef_[0][0]  # 斜率
                b = model.intercept_[0]  # 截距

                # 用模型预测 y 值
                y_fit = model.predict(x_numeric)

                # 绘制拟合曲线
                if len(x) > 0 and isinstance(x[0], datetime):  # 如果 x 是 datetime 类型，需将拟合的时间戳转换为 datetime
                    # 将拟合曲线的时间戳转换回 datetime 类型
                    x_fitted = np.array([x[0] + timedelta(seconds=ts) for ts in x_numeric.flatten()])
                    if len(y) > 0 and isinstance(y[0], datetime):  # y 也为 datetime 类型
                        # 将拟合的 y 值（秒数）转换回 datetime 类型
                        y_fitted_datetime = np.array([y[0] + timedelta(seconds=ts) for ts in y_fit.flatten()])
                        ax.plot(x_fitted, y_fitted_datetime, color=color, label=label,
                                zorder=zorder, linestyle=linestyle)
                    else:
                        ax.plot(x_fitted, y_fit.flatten(), color=color, label=label,
                                zorder=zorder, linestyle=linestyle)
                # 如果 y 是 datetime 类型，绘制拟合曲线时将 y_fit 转换回 datetime
                elif  len(y) > 0 and isinstance(y[0], datetime):
                    # 将拟合的 y 值（秒数）转换回 datetime 类型
                    y_fitted_datetime = np.array([y[0] + timedelta(seconds=ts) for ts in y_fit.flatten()])
                    ax.plot(x, y_fitted_datetime, color=color, label=label, zorder=zorder,linestyle=linestyle)
                else:
                    ax.plot(x, y_fit.flatten(), color=color, label=label, zorder=zorder,linestyle=linestyle)
                return data  # 返回数据
            return wrapper
        return decorator

    @staticmethod
    def transect(label='', color='orange', linestyle='-', zorder=5):
        """
        三次样条插值 - 画趋势图
        """

        def decorator(func):
            @wraps(func)
            def wrapper(ax, *args, **kwargs):
                # 调用原函数获取数据
                data = func(ax, *args, **kwargs)

                # 数据检查
                x = data.get('x')
                y = data.get('y')
                if x is None or y is None:
                    raise Exception('画图时（三次样条插值），x、y不能为空')

                x = np.array(x)
                y = np.array(y)
                x,y = data_deduplication(x,y)

                # 判断是否为datetime类型
                x_is_datetime = isinstance(x[0], datetime)
                y_is_datetime = isinstance(y[0], datetime)

                # 如果x和y都是datetime类型，则进行统一处理
                if x_is_datetime and y_is_datetime:
                    # 将x和y都转换为秒数，避免微秒精度问题
                    x_numeric = np.array([(dt - x[0]).total_seconds() for dt in x])
                    y_numeric = np.array([(dt - y[0]).total_seconds() for dt in y])
                elif x_is_datetime:
                    x_numeric = np.array([(dt - x[0]).total_seconds() for dt in x])
                    y_numeric = y
                elif y_is_datetime:
                    x_numeric = x
                    y_numeric = np.array([(dt - y[0]).total_seconds() for dt in y])
                else:
                    # x和y都不是datetime类型
                    x_numeric = x
                    y_numeric = y

                # 使用 CubicSpline 进行三次样条插值
                cs = CubicSpline(x_numeric, y_numeric)

                # 生成插值点（更密集的 x 点）
                num_points = len(x) * 10  # 根据实际情况，可以调整密度
                x_new = np.linspace(x_numeric[0], x_numeric[-1], num_points)
                y_new = cs(x_new)

                # 绘制结果
                if x_is_datetime and y_is_datetime:
                    # 如果x和y都为datetime类型，生成新的datetime对象
                    x_fitted = np.array([x[0] + timedelta(seconds=ts) for ts in x_new.flatten()])
                    y_fitted = np.array([y[0] + timedelta(seconds=ts) for ts in y_new.flatten()])
                    ax.plot(x_fitted, y_fitted, color=color, label=label, zorder=zorder, linestyle=linestyle)
                elif x_is_datetime:
                    # 只有x为datetime类型，y为数值类型
                    x_fitted = np.array([x[0] + timedelta(seconds=ts) for ts in x_new.flatten()])
                    ax.plot(x_fitted, y_new, color=color, label=label, zorder=zorder, linestyle=linestyle)
                elif y_is_datetime:
                    # 只有y为datetime类型，x为数值类型
                    y_fitted = np.array([y[0] + timedelta(seconds=ts) for ts in y_new.flatten()])
                    ax.plot(x_new, y_fitted, color=color, label=label, zorder=zorder, linestyle=linestyle)
                else:
                    # x和y都为数值类型
                    ax.plot(x_new, y_new, color=color, label=label, zorder=zorder, linestyle=linestyle)
                return data  # 返回数据

            return wrapper

        return decorator

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
            data = plot_func(ax)  # 执行装饰器修饰后的函数
            if (data is not None):
                plt_style = data.get('plt_style','')
                # 设置标题和标签
                if plt_style is None or (plt_style == ''):
                    ax.set_xlabel('横轴')
                    ax.set_ylabel('纵轴')
                    ax.set_title('title')
                else:
                    ax.set_xlabel(plt_style.get('xlabel','横轴'))
                    ax.set_ylabel(plt_style.get('ylabel','纵轴'))
                    ax.set_title(plt_style.get('title','title'))
            ax.legend()
            # 在每个子图上旋转X轴标签
            ax.tick_params(axis='x', rotation=45)

        # 如果子图不满，则隐藏多余的子图
        for i in range(num_plots, len(axes)):
            axes[i].axis('off')

        # 设置matplotlib的字体，以支持中文
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        # 自动调整布局
        plt.tight_layout()
        plt.show()

