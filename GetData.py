from datetime import datetime
import os
import re

from pandas import pivot

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