import requests
import json
import _thread
import time
import threading
import random
from pymongo import MongoClient




client = MongoClient()
db = client.YCKT_DATA


class GetTicketInfo(object):

    def __init__(self, ):
        # threading.Thread.__init__(self)
        print("线程号：")
        print(threading.currentThread())
        print(threading.currentThread().ident)

    def ticketIdList(self):
        billId = []
        for i in range(5):
            a = random.randint(0, 100)
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
    #     self.writeMongodb(ticketInfo)
    #
    #
    # def writeMongodb(self, ticketInfo):
    #     for i in range(len(ticketInfo)):
    #         ticket_DATA = dict(
    #             billType=ticketInfo[i]["billType"],
    #             endDate=ticketInfo[i]["endDate"],
    #             outTenPrice=ticketInfo[i]["outTenPrice"],
    #             billAmount=ticketInfo[i]["billAmount"],
    #             endDays=ticketInfo[i]["endDays"],
    #             endorseCount=ticketInfo[i]["endorseCount"],
    #             bankTypeName=ticketInfo[i]["bankTypeName"],
    #             annualizedRaise=ticketInfo[i]["annualizedRaise"],
    #             accepter=ticketInfo[i]["accepter"],
    #             belongEbankAccountName=ticketInfo[i]["belongEbankAccountName"],
    #             onsaleTime=ticketInfo[i]["onsaleTime"],
    #             billCode=ticketInfo[i]["billCode"]
    #         )
    #
    #         ticket_INFO = db.ticket_INFO
    #         post_id = ticket_INFO.insert_one(ticket_DATA).inserted_id
    #         print("post id is ", post_id)

    def runAll(self):
        pass



if __name__ == '__main__':
    GetTicketInfo().runAll()