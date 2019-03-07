'''
1、统计前一天发布票据的数量
2、统计前一天发布票据的平均利率
3、
'''
from pymongo import MongoClient
import numpy as np
import configparser
import os
import datetime


curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "configData.ini")

class StatisticxData(object):

    def __init__(self, name, set_name):
        self.cf = configparser.ConfigParser()
        self.cf.read(cfgpath)
        self.client = MongoClient()
        self.db = self.client[self.get_database(name)]
        self.open_db_set = self.db[self.get_database(set_name)]

    def get_database(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    # def yesterday_count(self):
    #     '''
    #     获取前一个工作日发布票据的数量
    #     :return:
    #     '''
    #     count = self.open_db_set.count({"send_date" : self.get_time()})
    #     return count

    def get_time(self):
        now_time = datetime.datetime.now()
        yes_time = now_time + datetime.timedelta(days=-1)
        yes_time_nyr = yes_time.strftime('%Y-%m-%d')
        return  yes_time_nyr

    def yesterday_avg(self):
        '''
        获取前一个工作日发布票据利率的平均值
        :return: 
        '''
        get_info_list = []
        get_info = self.open_db_set.find({"send_date" : self.get_time()}, {"_id":0, "except_rate":1})
        for i in get_info:
            # print(i, type(i))
            get_info_list.append(i["except_rate"])

        return get_info_list



if __name__ == '__main__':
    a = StatisticxData("database", "database_set").yesterday_avg()
    print("昨日票据统计数量为", len(a))
    # b = list(a)
    for i in range(len(a)):
        a[i] = float(a[i])

    b = np.mean(a)
    print("平局利率为：%.2f" %b)