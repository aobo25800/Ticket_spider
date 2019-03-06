from pymongo import MongoClient
from bson.objectid import ObjectId
from time import sleep

client = MongoClient()

class GetData(object):
    _ticket_data = []

    def __new__(cls, db_name, set_name, *args):
        if cls._ticket_data:
            pass
        else:
            cls._ticket_data = cls.get_data(db_name, set_name)
            # print("2_ticket_data", type(_ticket_data[0]), _ticket_data[0])
        return cls._ticket_data

    @staticmethod
    def get_data(a, b):
        db = client[a]
        name = db[b]
        ticket_data = list(name.find())

        return ticket_data

class AddData(object):
    pass
    def __init__(self, new_data, alter_field):
        self.new_data = new_data
        self.alter_field = alter_field
    def judge_data(self):
        '''判断数据是否存在，存在pass，不存在写入'''
        print("ClearData", id(GetData(i, j)))
        if self.new_data in GetData(i, j):
            print('数据存在')

        else:
            print('数据不存在')
        pass

    def update_data(self):
        pass




if __name__ == '__main__':
    i = "YCKT_DATA"         # 数据库名称
    j = "ticket_INFO_YPJ"   # 数据表名称
    data = 'j'

    # print(ObjectId('5c78e7f386676643bccb22e6'))
    while True:
        AddData(data).judge_data()
        sleep(0.5)