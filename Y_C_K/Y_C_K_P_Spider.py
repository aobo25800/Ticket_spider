import requests
import json
import xlwt
from pymongo import MongoClient


client = MongoClient()
db = client.YCKT_DATA


class GetTicketInfo(object):

    def __init__(self, ticket_id_url, ticket_info_url):
        self.id_url = ticket_id_url
        self.info_url = ticket_info_url
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
        self.timeout = 10




    def ticketIdList(self, num):
        self.billId = []
        # for i in range(1, 7):
        #     # 获取票号ID——url
        #     ticket_id_url = 'http://mall.yinchengku.com/mall/commodity/list?page=%d&perPage=10' % i
        #     # print(url)
        #     self.response = requests.get(ticket_id_url, timeout = 5)
        #     self.result = self.response.text
        #     self.result = json.loads(self.result)
        #     for j in range(len(self.result['content'])):
        #         self.billId.append(self.result['content'][j]['id'])
        # print(self.billId, len(self.billId))
        for i in range(1, num):
            ticket_id_url = self.id_url % i
            response = requests.get(ticket_id_url, headers=self.header, timeout=self.timeout)
            result = json.loads(response.text)
            for j in range(len(result['content'])):
                if result["content"][j]['commoditySellStatus'] is True:
                    self.billId.append(result['content'][j]['id'])
                else:
                    continue
        print("result结果为：", result)
        print("billId结果为：", self.billId, '\n', "billId数量为：", len(self.billId))
        return self.billId

    def getInfo(self, billIdList):
        ticketInfo = []
        for i in range(len(billIdList)):
            ticket_info_url = self.info_url % billIdList[i]
            response = requests.get(ticket_info_url, headers=self.header, timeout=self.timeout)
            self.result = response.text
            self.result = json.loads(self.result)
            ticketInfo.append(self.result)
        # print("ticketInfo信息是:", ticketInfo)
        return ticketInfo

    def writeExcel(self, ticketInfo):

        workbook = xlwt.Workbook(encoding='ascii')
        worksheet = workbook.add_sheet('Ticket_info')
        # billType
        # billAmount---票据金额
        # bankTypeName---承兑行类型
        # accepter----承兑人全称
        # endDate
        # endDays---剩余天数
        # annualizedRaise---年化利率
        # outTenPrice---每十万扣款
        # endorseCount---背书次数
        # discrepancy

        for i in range(len(ticketInfo)):
            a = ticketInfo[i]["billType"]
            b = ticketInfo[i]["billAmount"]
            c = ticketInfo[i]["bankTypeName"]
            d = ticketInfo[i]["accepter"]
            e = ticketInfo[i]["endDate"]
            f = ticketInfo[i]["endDays"]
            g = ticketInfo[i]["annualizedRaise"]
            h = ticketInfo[i]["outTenPrice"]
            j = ticketInfo[i]["endorseCount"]
            k = ticketInfo[i]["discrepancy"]
            # print(type(b))
            data = list("abcdefghjk")
            print(data)
            for j in range(10):
                for x in data:
                    worksheet.write(i, j, label=x)


        workbook.save('spider_ticket_info.xls')

    def writeMongodb(self, ticketInfo):
        for i in range(len(ticketInfo)):
            ticket_DATA = dict(
                billType=ticketInfo[i]["billType"],
                billAmount=ticketInfo[i]["billAmount"],
                bankTypeName=ticketInfo[i]["bankTypeName"],
                accepter=ticketInfo[i]["accepter"],
                endDate=ticketInfo[i]["endDate"],
                endDays=ticketInfo[i]["endDays"],
                annualizedRaise=ticketInfo[i]["annualizedRaise"],
                outTenPrice=ticketInfo[i]["outTenPrice"],
                endorseCount=ticketInfo[i]["endorseCount"],
                discrepancy=ticketInfo[i]["discrepancy"]
            )
            ticket_INFO = db.ticket_INFO
            post_id = ticket_INFO.insert_one(ticket_DATA).inserted_id
            print("post id is ", post_id)


if __name__ == '__main__':

    ticket_id_url = 'http://mall.yinchengku.com/mall/commodity/list?page=%d&perPage=10'
    ticket_info_url = 'http://mall.yinchengku.com/mall/commodity/get/%s'
    get_info = GetTicketInfo(ticket_id_url, ticket_info_url)
    bill_id = get_info.ticketIdList(7)
    bill_info = get_info.getInfo(bill_id)
    get_info.writeMongodb(bill_info)
    # print(bill_id)
    # print(bill_info)