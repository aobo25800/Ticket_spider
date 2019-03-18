import queue
import threading
import random
from pymongo import MongoClient




client = MongoClient()
db = client.YCKT_DATA


class GetTicketInfo(object):

    def __init__(self, page):
        self.page = page
        print("线程号：")
        print(threading.currentThread())
        print(threading.currentThread().ident)

    def ticketIdList(self):
        billId = []
        for i in range(5):
            a = self.page
            billId.append(a)

        self.getInfo(billId)
        # return billId

    def getInfo(self, billIdList):
        ticketInfo = []
        for i in billIdList:
            url = "www.baidu.com %d" %i
            ticketInfo.append(url)
        print(ticketInfo)
        print(threading.current_thread())

    def runAll(self):
        pass



if __name__ == '__main__':
    GetTicketInfo().runAll()