import requests
import json
import threading
from pymongo import MongoClient



client = MongoClient()
db = client.YCKT_DATA


class GetTicketInfo(object):

    def __init__(self, ticket_id_url, ticket_info_url, page):
        self.id_url = ticket_id_url
        self.info_url = ticket_info_url
        self.page = page
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
        self.timeout = 10

    def ticketIdList(self):
        billId = []
        for i in range(1, self.page):
            ticket_id_url = self.id_url % i
            response = requests.get(ticket_id_url, headers=self.header, timeout=self.timeout)
            result = json.loads(response.text)
            for j in range(len(result['content'])):
                if result["content"][j]['commoditySellStatus'] is True:
                    billId.append(result['content'][j]['id'])
                else:
                    continue
            # print("result结果为：", result)
        # print("billId结果为：", billId, '\n\t', "billId数量为：", len(billId))
        self.getInfo(billId)
        # return billId

    def getInfo(self, billIdList):
        ticketInfo = []
        for i in range(len(billIdList)):
            ticket_info_url = self.info_url % billIdList[i]
            response = requests.get(ticket_info_url, headers=self.header, timeout=self.timeout)
            self.result = response.text
            self.result = json.loads(self.result)
            ticketInfo.append(self.result)
        # print("ticketInfo信息是:", ticketInfo)

        self.writeMongodb(ticketInfo)
        # return ticketInfo

    def writeMongodb(self, ticketInfo):
        for i in range(len(ticketInfo)):
            ticket_DATA = dict(
                billType=ticketInfo[i]["billType"],
                endDate=ticketInfo[i]["endDate"],
                outTenPrice=ticketInfo[i]["outTenPrice"],
                billAmount=ticketInfo[i]["billAmount"],
                endDays=ticketInfo[i]["endDays"],
                endorseCount=ticketInfo[i]["endorseCount"],
                bankTypeName=ticketInfo[i]["bankTypeName"],
                annualizedRaise=ticketInfo[i]["annualizedRaise"],
                accepter=ticketInfo[i]["accepter"],
                belongEbankAccountName=ticketInfo[i]["belongEbankAccountName"],
                onsaleTime=ticketInfo[i]["onsaleTime"],
                billCode=ticketInfo[i]["billCode"]
            )

            ticket_INFO = db.ticket_INFO
            post_id = ticket_INFO.insert_one(ticket_DATA).inserted_id
            print("post id is ", post_id)

    def runAll(self):
        pass

if __name__ == '__main__':

    ticket_id_url = 'http://mall.yinchengku.com/mall/commodity/list?page=%d&perPage=10'
    ticket_info_url = 'http://mall.yinchengku.com/mall/commodity/get/%s'
    num = 258
    get_info = GetTicketInfo(ticket_id_url, ticket_info_url, page=num)
    # bill_id = get_info.ticketIdList(2)
    # bill_id = [39851]
    # bill_info = get_info.getInfo(bill_id)
    # print(bill_info)
