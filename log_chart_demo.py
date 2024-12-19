from networkx.algorithms.bipartite.basic import color

from process.DrawChart import *
from process.GetData import *
from datetime import datetime

# 装饰了折线图、均值线和散点图
@PlotDecorators.line(label='111')
@PlotDecorators.avg_y(color='green')
@PlotDecorators.avg_x()
@PlotDecorators.scatter()
@PlotDecorators.least_square_method()
@PlotDecorators.transect()
def plot_data1(ax):
    plt_style = {
        'xlabel':'横轴',
        'ylabel':'纵轴',
        'title':'demo测试'
    }
    return {'x': [1,2,3,4,5], 'y': [2, 4, 5, 4, 5],'plt_style':plt_style}

# 装饰了折线图、均值线和散点图
@PlotDecorators.line(label='222')
@PlotDecorators.avg_y(color='green')
@PlotDecorators.avg_x()
@PlotDecorators.scatter()
@PlotDecorators.least_square_method()
@PlotDecorators.transect()
def plot_data2(ax):
    total_values, times = LogData().get_log_data()
    return {'x': times, 'y': total_values}

@PlotDecorators.line(label='333')
@PlotDecorators.avg_y(color='green')
@PlotDecorators.avg_x()
@PlotDecorators.scatter()
@PlotDecorators.least_square_method()
@PlotDecorators.transect()
def plot_data3(ax):
    x = [datetime(2024, 1, 1, 12, 0),
         datetime(2024, 1, 1, 12, 10),
         datetime(2024, 1, 1, 12, 20)]
    y = [100, 150, 120]

    return {'x': x, 'y': y}

@PlotDecorators.line(label='333')
@PlotDecorators.avg_y(color='green')
@PlotDecorators.avg_x()
@PlotDecorators.scatter()
@PlotDecorators.least_square_method()
@PlotDecorators.transect()
def plot_data4(ax):
    x = [datetime(2024, 1, 1, 12, 0),
         datetime(2024, 1, 1, 12, 10),
         datetime(2024, 1, 1, 12, 20)]
    y = [datetime(2024, 1, 1, 12, 0),
         datetime(2024, 1, 1, 12, 10),
         datetime(2024, 1, 1, 12, 20)]

    return {'x': x, 'y': y}
if __name__ == '__main__':
    # 调用自动绘图函数
    PlotDecorators.create_plots(
        (plot_data1),
        # (plot_data2),
        (plot_data3),
        (plot_data4)
    )


