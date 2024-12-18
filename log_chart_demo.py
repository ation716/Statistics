from networkx.algorithms.bipartite.basic import color

from process.DrawChart import *
from process.GetData import *
from datetime import datetime

# 装饰了折线图、均值线和散点图
@PlotDecorators.line(label='xxx')
@PlotDecorators.avg_y(color='green')
@PlotDecorators.avg_x()
@PlotDecorators.scatter()
@PlotDecorators.observation()
def plot_data1(ax):
    # total_values, times = LogData().get_log_data()
    # plt_style = {
    #     'xlabel':'横轴',
    #     'ylabel':'纵轴',
    #     'title':'demo测试',
    #     'label_line':'test'
    # }
    return {'x': [1,2,3,4,5], 'y': [2, 4, 5, 4, 5]}

# 装饰了折线图、均值线和散点图
@PlotDecorators.line()
@PlotDecorators.scatter()
@PlotDecorators.observation()
@PlotDecorators.avg_y()
def plot_data2(ax):
    total_values, times = LogData().get_log_data()
    x = [datetime(2024, 11, 20, 14, 36, 20, 715000), datetime(2024, 11, 20, 14, 36, 20, 715000),
     datetime(2024, 11, 20, 14, 36, 28, 165000), datetime(2024, 11, 20, 14, 36, 28, 165000),
     datetime(2024, 11, 20, 14, 41, 23, 457000), datetime(2024, 11, 20, 14, 41, 23, 457000),
     datetime(2024, 11, 20, 14, 41, 36, 160000), datetime(2024, 11, 20, 14, 41, 36, 160000),
     datetime(2024, 11, 20, 14, 42, 1, 217000), datetime(2024, 11, 20, 14, 42, 1, 217000),
     datetime(2024, 11, 20, 14, 43, 2, 186000), datetime(2024, 11, 20, 14, 43, 2, 186000),
     datetime(2024, 11, 20, 14, 43, 27, 105000), datetime(2024, 11, 20, 14, 43, 27, 105000),
     datetime(2024, 11, 20, 14, 43, 34, 85000), datetime(2024, 11, 20, 14, 43, 34, 85000),
     datetime(2024, 11, 20, 14, 43, 37, 439000), datetime(2024, 11, 20, 14, 43, 37, 439000),
     datetime(2024, 11, 20, 14, 43, 42, 170000), datetime(2024, 11, 20, 14, 43, 42, 170000),
     datetime(2024, 11, 20, 14, 43, 46, 902000), datetime(2024, 11, 20, 14, 43, 46, 902000),
     datetime(2024, 11, 20, 14, 43, 50, 547000), datetime(2024, 11, 20, 14, 43, 50, 547000),
     datetime(2024, 11, 20, 14, 43, 54, 497000), datetime(2024, 11, 20, 14, 43, 54, 497000),
     datetime(2024, 11, 20, 14, 43, 58, 446000), datetime(2024, 11, 20, 14, 43, 58, 446000),
     datetime(2024, 11, 20, 14, 44, 2, 436000), datetime(2024, 11, 20, 14, 44, 2, 436000),
     datetime(2024, 11, 20, 14, 44, 6, 275000), datetime(2024, 11, 20, 14, 44, 6, 275000),
     datetime(2024, 11, 20, 14, 44, 26, 317000), datetime(2024, 11, 20, 14, 44, 26, 317000),
     datetime(2024, 11, 20, 14, 44, 37, 153000), datetime(2024, 11, 20, 14, 44, 37, 153000),
     datetime(2024, 11, 20, 15, 21, 43, 489000), datetime(2024, 11, 20, 15, 21, 43, 489000),
     datetime(2024, 11, 20, 15, 21, 47, 257000), datetime(2024, 11, 20, 15, 21, 47, 257000),
     datetime(2024, 11, 20, 15, 21, 51, 236000), datetime(2024, 11, 20, 15, 21, 51, 236000),
     datetime(2024, 11, 20, 15, 21, 58, 252000), datetime(2024, 11, 20, 15, 21, 58, 252000),
     datetime(2024, 11, 20, 15, 23, 24, 614000), datetime(2024, 11, 20, 15, 23, 24, 614000),
     datetime(2024, 11, 20, 15, 23, 28, 507000), datetime(2024, 11, 20, 15, 23, 28, 507000),
     datetime(2024, 11, 20, 15, 23, 33, 50000), datetime(2024, 11, 20, 15, 23, 33, 50000),
     datetime(2024, 11, 20, 15, 25, 10, 591000), datetime(2024, 11, 20, 15, 25, 10, 591000),
     datetime(2024, 11, 20, 15, 25, 22, 515000), datetime(2024, 11, 20, 15, 25, 22, 515000),
     datetime(2024, 11, 20, 15, 25, 34, 725000), datetime(2024, 11, 20, 15, 25, 34, 725000),
     datetime(2024, 11, 20, 15, 25, 59, 19000), datetime(2024, 11, 20, 15, 25, 59, 19000),
     datetime(2024, 11, 20, 15, 26, 23, 457000), datetime(2024, 11, 20, 15, 26, 23, 457000),
     datetime(2024, 11, 20, 15, 26, 33, 948000), datetime(2024, 11, 20, 15, 26, 33, 948000),
     datetime(2024, 11, 20, 15, 26, 42, 41000), datetime(2024, 11, 20, 15, 26, 42, 41000),
     datetime(2024, 11, 20, 15, 26, 48, 639000), datetime(2024, 11, 20, 15, 26, 48, 639000),
     datetime(2024, 11, 20, 15, 26, 52, 369000), datetime(2024, 11, 20, 15, 26, 52, 369000),
     datetime(2024, 11, 20, 15, 28, 24, 302000), datetime(2024, 11, 20, 15, 28, 24, 302000),
     datetime(2024, 11, 20, 15, 28, 28, 153000), datetime(2024, 11, 20, 15, 28, 28, 153000),
     datetime(2024, 11, 20, 15, 28, 31, 905000), datetime(2024, 11, 20, 15, 28, 31, 905000),
     datetime(2024, 11, 20, 15, 28, 36, 455000), datetime(2024, 11, 20, 15, 28, 36, 455000),
     datetime(2024, 11, 20, 15, 28, 47, 620000), datetime(2024, 11, 20, 15, 28, 47, 620000),
     datetime(2024, 11, 20, 15, 28, 52, 809000), datetime(2024, 11, 20, 15, 28, 52, 809000),
     datetime(2024, 11, 20, 15, 28, 56, 60000), datetime(2024, 11, 20, 15, 28, 56, 60000),
     datetime(2024, 11, 20, 15, 28, 59, 30000), datetime(2024, 11, 20, 15, 28, 59, 30000),
     datetime(2024, 11, 20, 15, 29, 10, 183000), datetime(2024, 11, 20, 15, 29, 10, 183000),
     datetime(2024, 11, 20, 15, 29, 14, 113000), datetime(2024, 11, 20, 15, 29, 14, 113000),
     datetime(2024, 11, 20, 15, 29, 17, 362000), datetime(2024, 11, 20, 15, 29, 17, 362000),
     datetime(2024, 11, 20, 15, 29, 26, 58000), datetime(2024, 11, 20, 15, 29, 26, 58000)]
    y=list(range(92))
    return {'x': x, 'y': y}

if __name__ == '__main__':
    # 调用自动绘图函数
    PlotDecorators.create_plots(
        (plot_data1),
        # (plot_data2)
    )

