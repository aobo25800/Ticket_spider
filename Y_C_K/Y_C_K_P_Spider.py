import time
import requests
import json
import threading
from queue import Queue
from pymongo import MongoClient



client = MongoClient()
db = client.YCKT_DATA


class GetTicketInfo(object):

    def __init__(self):
        self.q_bill_all_url = Queue()
        self.q_ticket_id = Queue()
        self.q_ticket_info = Queue()
        self.q_save_data = Queue()

        self.ticket_id_url = 'http://mall.yinchengku.com/mall/commodity/list?page={}&perPage=10'
        self.ticket_info_url = 'http://mall.yinchengku.com/mall/commodity/get/{}'
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
        self.timeout = 10

    def get_url_list(self):
        '''拼接票据列表页的URL'''
        for i in range(1, 11):
            self.q_ticket_id.put(self.ticket_id_url.format(i))

    def ticketIdList(self):
        '''从页面获取所有票据的ID'''
        while True:
            url = self.q_ticket_id.get()
            response = requests.get(url, headers=self.header, timeout=self.timeout)
            result = json.loads(response.text)
            # print(result)
            billId = []
            for j in range(len(result['content'])):
                billId.append(result['content'][j]['id'])
            # print(billId)
            self.q_bill_all_url.put(billId)
            self.q_ticket_id.task_done()
                # self.getInfo(billId)

    def get_info_url(self):
        '''根据票据ID拼接票据详情页的URL'''
        while True:
            one_id = self.q_bill_all_url.get()

            for i in one_id:
                ticket_info = self.ticket_info_url.format(i)
                self.q_ticket_info.put(ticket_info)
            self.q_bill_all_url.task_done()

    def get_ticket_data(self):
        while True:
            info_url = self.q_ticket_info.get()
            response = requests.get(info_url, headers=self.header, timeout=self.timeout)
            save_data = json.loads(response.text)
            self.q_save_data.put(save_data)
            self.q_ticket_info.task_done()

    def save_db(self):
        while True:
            ticketInfo = self.q_save_data.get()
            ticket_DATA = dict(
                billType=ticketInfo["billType"],
                # endDate=ticketInfo["endDate"],
                endDate=time.strftime("%Y-%m-%d", time.localtime(int(ticketInfo["endDate"])/1000)),

                outTenPrice=ticketInfo["outTenPrice"],
                billAmount=ticketInfo["billAmount"],
                endDays=ticketInfo["endDays"],
                endorseCount=ticketInfo["endorseCount"],
                bankTypeName=ticketInfo["bankTypeName"],
                annualizedRaise=ticketInfo["annualizedRaise"],
                accepter=ticketInfo["accepter"],
                belongEbankAccountName=ticketInfo["belongEbankAccountName"],
                # onsaleTime=ticketInfo["onsaleTime"],
                onsaleTime=time.strftime("%Y-%m-%d", time.localtime(int(ticketInfo["onsaleTime"])/1000)),
                billCode=ticketInfo["billCode"]
            )
            if ticketInfo['annualizedRaise'] > 8 and ticketInfo['annualizedRaise'] < 2.5:
                continue
            else:
                ticket_INFO = db.ticket_INFO
                post_id = ticket_INFO.insert_one(ticket_DATA).inserted_id
                print("post id is ", post_id)
            self.q_save_data.task_done()

    def runAll(self):
        start = time.time()
        thread_list = []

        t_url = threading.Thread(target=self.get_url_list)
        thread_list.append(t_url)

        for i in range(3):
            th_bill_id = threading.Thread(target=self.ticketIdList)
            thread_list.append(th_bill_id)

        th_parse = threading.Thread(target=self.get_info_url)
        thread_list.append(th_parse)

        for i in range(3):
            th_ticket_info = threading.Thread(target=self.get_ticket_data)
            thread_list.append(th_ticket_info)

        th_save_data = threading.Thread(target=self.save_db)
        thread_list.append(th_save_data)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.q_bill_all_url, self.q_ticket_id, self.q_ticket_info]:
            q.join()
        print("时间为：", time.time() - start)




if __name__ == '__main__':
    start = time.time()
    GetTicketInfo().runAll()
    print("耗时为1", time.time() - start)
