from process.DrawChart import *
from process.GetData import *


# 装饰了折线图、均值线和散点图
@PlotDecorators.line
@PlotDecorators.avg_y
@PlotDecorators.scatter
@PlotDecorators.observation
def plot_data1(ax):
    total_values, times = LogData().get_log_data()
    return {'x': [1,2,3,4,5], 'y': [2, 4, 5, 4, 5]}

# 装饰了折线图、均值线和散点图
@PlotDecorators.line
@PlotDecorators.avg_y
@PlotDecorators.scatter
# @PlotDecorators.observation
def plot_data2(ax):
    total_values, times = LogData().get_log_data()
    return {'x': times, 'y': total_values}

if __name__ == '__main__':
    # 调用自动绘图函数
    PlotDecorators.create_plots(
        # (plot_data1),
        (plot_data2)
    )

