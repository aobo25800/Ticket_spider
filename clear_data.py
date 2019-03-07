import copy
from pymongo import MongoClient
from bson.objectid import ObjectId

from time import sleep

client = MongoClient()

class GetData(object):
    _ticket_data = []

    def __new__(cls, db_name, set_name, remain_day="remain_day", *args):
        if cls._ticket_data:
            pass
        else:
            cls._ticket_data = cls.get_data(db_name, set_name)
            for i in range(len(cls._ticket_data)):
                cls._ticket_data[i].pop(remain_day)
                cls._ticket_data[i].pop("_id")
            print("2_ticket_data", type(cls._ticket_data[0]), cls._ticket_data)
        return cls._ticket_data

    @staticmethod
    def get_data(a, b):
        db = client[a]
        name = db[b]
        ticket_data = list(name.find())

        return ticket_data

class AddData(object):
    '''
    通过除【remain_day（剩余天数），_id】字段之外的全部字段来判断数据库是否存在此数据，
    如果存在修改remain_day字段，不存在新建保存到数据库
    '''
    def __init__(self, database_name, database_set, new_data, alter_field):
        '''
        
        :param database_name: 数据库名称 
        :param database_set: 数据表名称
        :param new_data: 准备写入的数据
        :param alter_field: 要修改的字段
        '''
        self.database_name = database_name
        self.database_set = database_set
        self.new_data = new_data
        self.alter_field = alter_field

    def judge_data(self):
        '''判断数据是否存在，存在pass，不存在写入'''
        i = copy.deepcopy(self.new_data)

        i.pop(self.alter_field)
        # print("删除hou", i)
        print("ClearData", id(GetData(self.database_name, self.database_set)))

        if i in GetData(self.database_name, self.database_set):
            print('数据存在')
            print("传入的数据是：", self.new_data)

            self.update_data(i)

        else:
            print('数据不存在')
            self.seva_data()
        pass

    def update_data(self, ID):
        db = client[self.database_name]
        db_set = db[self.database_set]
        # myquery修改之前的数据
        my_query = {}
        my_query["remain_day"] = list(db_set.find(ID))[0]["remain_day"]
        print("修改之前的数据", my_query)

        new_values = {}
        new_values["$set"] = {"remain_day": self.new_data["remain_day"]}
        print("新数据为", new_values)
        db_set.update_one(my_query, new_values)

        after_query = db_set.find(ID)
        print("修改之后的数据", after_query[0])

    def seva_data(self):
        db = client[self.database_name]
        db_set = db[self.database_set]
        db_set.insert_one(self.new_data)




if __name__ == '__main__':
    database_name  = "YCKT_DATA"         # 数据库名称
    database_set = "ticket_INFO_YPJ"   # 数据表名称
    data = {
        "bill_type" : "电银",
        "transferability" : "是",
        "bank_type" : "其他",
        "except_sum" : "860416.67",
        "except_rate" : "15.00",
        "end_time" : "2020-01-30",
        "bill_sum" : "100",
        "send_date" : "2019-03-01",
        "accept_bank" : "西双版纳国际旅游度假区开发有限",
        "remain_day" : "8890",
        "start_time" : "2019-01-30"
        }
    remain_day = "remain_day"

    # i = data.pop(remain_day)
    # print(data)
    # print(ObjectId('5c78e7f386676643bccb22e6'))
    # while True:
    AddData(database_name, database_set, data, remain_day).judge_data()
    sleep(0.5)