from DrawChart import *
from GetData import *


# 装饰了折线图、均值线和散点图
@PlotDecorators.line
@PlotDecorators.avg_y
@PlotDecorators.scatter
def plot_data1(ax):
    total_values, times = LogData().get_log_data()
    return {'x': times, 'y': total_values}

# 装饰了折线图、均值线和散点图
@PlotDecorators.line
@PlotDecorators.avg_y
@PlotDecorators.scatter
def plot_data2(ax):
    total_values, times = LogData().get_log_data()
    return {'x': times, 'y': total_values}

if __name__ == '__main__':
    # 调用自动绘图函数
    PlotDecorators.create_plots(
        (plot_data1),
        (plot_data2)
    )
