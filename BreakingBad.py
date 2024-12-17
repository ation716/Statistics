"""统计信息的库
"""
# matplotlib https://matplotlib.org/stable/users/explain/
try:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import AutoLocator, AutoMinorLocator
    import numpy as np
    import sqlite3
    import json
    # import re
    import time
    from datetime import datetime, timedelta
    import config as cg
    import functools

except Exception as e:
    print(e)

# 设置matplotlib的字体，以支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号



class Haisenberg:
    """画图"""
    decorated_fun=[] # to count axes
    is_combined=False
    relation_map={}
    fig,axes=None,None

    @classmethod
    def join_decorated_fun(cls,fun_name):
        """Join decorated functions and set up axes if needed"""
        for funs in cls.decorated_fun:
            for fun in funs:
                if fun == fun_name:
                    return
        else:
            cls.decorated_fun.append([fun_name])
        if not cls.is_combined:
            cls.fig, cls.axes = plt.subplots(1,1,
                                             figsize=( 5, 10))  # todo adaptive size
            cls.axes = [cls.axes]

    @classmethod
    def update_fig(cls,axes_num):
        """"""
        cls.fig,cls.axes =plt.subplots(axes_num//2+1,2,
                                             figsize=( 5*(axes_num//2+1), 10))

    @classmethod
    def get_axes(cls,name):
        """"""
        for i in range(len(cls.decorated_fun)):
            print(cls.decorated_fun)
            for j in range(len(cls.decorated_fun[i])):
                if cls.decorated_fun[i][j]==name:
                    print(i,name)
                    if j>1:
                        return cls.axes[i].twinx()
                    else:
                        print(len(cls.axes))
                        return cls.axes[i]
        return


    @staticmethod
    def mark_twins(label=""):
        """ mark twin axes """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                data = func(*args, **kwargs)
                if not Haisenberg.relation_map.get(label):
                    Haisenberg.relation_map[label]=func.__name__
                    Haisenberg.decorated_fun.append([func.__name__])
                else:
                    for funs in Haisenberg.decorated_fun:
                        for fun in funs:
                            if fun==Haisenberg.relation_map.get(label):
                                funs.append(func.__name__)

                return data
            return wrapper
        return decorator



    @staticmethod
    def broken_line(**param):
        """ plot data as a line graph """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                data = func(*args, **kwargs)
                Haisenberg.join_decorated_fun(func.__name__)
                if data is not None:
                    axes_c=Haisenberg.get_axes(func.__name__)
                    if param.get('param_dict'):
                        axes_c.plot(data,label=param.get('label'),**(param.get('param_dict')))
                    else:
                        axes_c.plot(data, label=param.get('label'))
                    axes_c.set_title(param.get('title'))
                    if kwargs.get('label') is not None:
                        axes_c.legend(loc='upper right')
                return data
            return wrapper
        return decorator

    @staticmethod
    def scatter(func):
        """
        装饰器：将数据画成散点图
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if data is not None:
                x = np.arange(len(data))
                plt.scatter(x, data, label="Scatter Plot")
            return data
        Haisenberg.decorated_fun.append(func.__name__)
        return wrapper

    @staticmethod
    def bar(func):
        """
        装饰器：将数据画成柱状图
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if data is not None:
                x = np.arange(len(data))
                plt.bar(x, data, label="Bar Chart")
            return data
        Haisenberg.decorated_fun.append(func.__name__)
        return wrapper

    @staticmethod
    def means(tilte="title", label="mean line"):
        """
        装饰器：在图上绘制均线
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                data = func(*args, **kwargs)
                Haisenberg.join_decorated_fun(func.__name__)
                if data is not None:
                    index = Haisenberg.decorated_fun.index(func.__name__)
                    mean_line = [np.mean(data)] * len(data)
                    Haisenberg.axes[index].plot(mean_line, label=label,linestyle='--',color='red')
                    Haisenberg.axes[index].set_title(tilte)
            return wrapper
        return decorator

    @staticmethod
    def show_plot():
        """
        显示图表并清空，避免多次绘制时图形堆叠
        """
        plt.show()
        pass




class Goodman:
    """数据库读取"""

    def __init__(self,db_path):
        self.db_path=db_path
    def __del__(self):
        pass

    @property
    def conn(self):
        return sqlite3.connect(self.db_path)

    def query_data(self, table="Order",filter=None):
        """
        执行查询操作，返回筛选后的数据，使用事务机制避免阻塞。
        :param query: SQL查询语句
        :param params: SQL查询语句的参数（默认空元组）
        :return: 返回查询结果的列表
        """
        cursor = self.conn.cursor()
        try:
            self.conn.isolation_level = 'EXCLUSIVE'
            cursor.execute("BEGIN EXCLUSIVE;")
            sql=self.translate_to_sql(table,filter)
            cursor.execute(sql)
            data = cursor.fetchall()
            self.conn.commit()
            return data
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Error occurred: {e}")
            return []
        finally:
            self.conn.close()

    def translate_to_sql(self,table="Order",filter=None):
        """"""
        if isinstance(filter,str):
            return filter
        sql_query = f"select * from {repr(table)}"
        where = ""
        if filter:
            where += " where"
            first_flag = True
            for i, j in filter.items():
                if first_flag:
                    first_flag = False
                else:
                    where += " and"
                if i == "terminate_time" or i == "create_time" or i == "receive_time":
                    if not j:
                        where += f" {i} between 0 and {int(time.time())}"
                    else:
                        if isinstance(j[0], str):
                            if j[0].find(":"):  # 时间格式未作清晰的检查, 注意数据库时间是北京时间+8
                                j0_s ,j1_s,*_= self.times_convert(j)
                                receive_inter = f" {i} between {j0_s} and {j1_s}"
                                where += receive_inter
                            else:
                                raise Exception(f"time format is not standard, {j}")
                        else:
                            where += f" {i} between {j[0]} and {j[1]}"
                else:
                    if isinstance(j, str) or isinstance(j,int) or isinstance(j,float):
                        where += f" {i}={repr(j)}"
                    else:
                        where += f" {i} in {repr(j)}"
        sql_query += where
        return sql_query

    @staticmethod
    def times_convert(times,_format='%Y-%m-%d %H:%M:%S'):
        """"""
        if isinstance(times, str):
            return (datetime.strptime(times, _format) + timedelta(hours=8 - cg.utc_time)).timestamp()
        else:
            return [(datetime.strptime(time, _format) + timedelta(hours=8 - cg.utc_time)).timestamp() for time in times]

    # more explicit data





#
# # 修改 query_order1 函数，接受动态查询结果
# def query_order1(rows):
#     # 假设你从 SQLite 数据库查询得到以下结果
#     return rows
#
#
# # 提取字段值（横纵坐标数据）
# def extract_fields(rows):
#     create_time_data = [row["create_time"] for row in rows]
#     execution_time_data = [row["execution_time_cost"] for row in rows]
#
#     # 如果时间是 Unix 时间戳 (整数)，则转换为 datetime 对象
#     create_time_data = [
#         datetime.fromtimestamp(time) if isinstance(time, int) else datetime.strptime(time, "%Y-%m-%d %H:%M:%S") for time
#         in create_time_data]
#
#     return create_time_data, execution_time_data
#
#
# # 将提取的字段传入绘图函数
# def plot_order_data(order_path, filter_conditions):
#     # 从 Goodman 查询数据
#     rows = Goodman.query_orders(order_path, filter_conditions)
#
#     # 调用 query_order1 处理查询结果
#     rows = query_order1(rows)
#
#     # 提取字段
#     create_time_data, execution_time_data = extract_fields(rows)
#
#     # 返回执行时间数据
#     return create_time_data, execution_time_data
#
#
# # 装饰器应用于散点图函数
# # @Haisenberg.scatter()
# def plot_scatter_data(create_time_data, execution_time_data):
#     return execution_time_data


class LittlePink():
    """日志读取"""

    def __init__(self):
        pass

    def __del__(self):
        pass


    # import matplotlib.pyplot as plt
    #
    # # 创建一个图形和子图
    # fig, axes = plt.subplots(1, 1)
    #
    # # 动态添加一个新的子图
    # new_axes = fig.add_subplot(2, 2, 4)  # 在 2x2 网格的第 4 个位置添加新子图
    #
    # # 绘制一些数据
    # axes.plot([1, 2, 3], [1, 2, 3])
    # new_axes.plot([1, 2, 3], [3, 2, 1])
    #
    # plt.show()

if __name__ == '__main__':
    # test_GoodMan
    # soul=Goodman(r'D:\workshop\new_bug\2412\无锡RDSCore-Debug-20241205132243-20241205140044\db\orders.sqlite')
    # # data=soul.query_data()
    #
    # # print(soul.times_convert(("2412-12-08 10:10:10","2412-12-08 10:10:10")))
    # data=soul.query_data(filter={"type":0,"create_time":("2024-08-21 00:00:00","2024-08-26 00:00:00")})
    # print('bingo')
    # pass

    @Haisenberg.means()
    @Haisenberg.broken_line(title="tes",label="label",param_dict={'marker':'x'})
    def get_data1():
        soul = Goodman(r'db\orders.sqlite') # 随便抓的一个数据库，241205之前都有数据
        data = soul.query_data(filter={"type": 0, "create_time": ("2024-08-21 00:00:00", "2024-08-26 00:00:00")})


        return
    #
    #
    # # @Haisenberg.means("4")
    # @Haisenberg.broken_line(title="tes2")
    # def get_data2():
    #     return np.random.rand(20)*20
    #
    #
    #
    # get_data1()
    # # get_data2()
    # print(Haisenberg.decorated_fun)
    # Haisenberg.show_plot()
