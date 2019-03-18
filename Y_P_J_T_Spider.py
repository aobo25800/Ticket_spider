import requests
import re
import copy
import time
from time import sleep
from pymongo import MongoClient
from lxml import etree
import clear_data


# client = MongoClient()
# db = client.YCKT_DATA

class SpiderYun(object):

    def __init__(self, num):
        self.num = num
        print("下一页的页面为", self.num)
        sleep(1)
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        self.url_all_ticket = 'http://www.cpiaoju.com/draft?&page=%s' % self.num
        self.url_base = 'http://www.cpiaoju.com'
        # self.ticket_INFO = db.ticket_INFO_YPJ

    def _getTicketUrl(self):
        '''获取票据的链接'''
        detail_html = self._parseUrl(self.url_all_ticket)
        detail_html_elements = etree.HTML(detail_html)
        elements_list = detail_html_elements.xpath("//div[@class='R_borderG clearfix R_ulcont']//a/@href")
        elements_set = set(elements_list)
        elements_set_list = list(elements_set)
        return elements_set_list

    def _parseUrl(self,url):
        '''发送请求，获取响应'''
        response = requests.get(url, headers=self.headers,  timeout=20)
        return response.content

    def _configTicketUrl(self, url_list):
        '''配置票据的URL'''
        url_info = []
        for ticket_path in url_list:
            group_info_url = self.url_base + ticket_path
            url_info.append(group_info_url)
        return url_info

    def _getTicketInfo(self, ticket_url):
        '''获取票据数据'''
        for parse_url in ticket_url:
            detail_html = self._parseUrl(parse_url)
            detail_html_elements = etree.HTML(detail_html)
            detail_title_data = detail_html_elements.xpath("//div[@class='R_seulp1 R_fontSize3 R_marginBot']//text()")
            detail_title_data = [x.strip() for x in detail_title_data if x.strip()!='']

            list_data = []
            for i in range(1, 10):
                html_data = detail_html_elements.xpath("/html/body/div[4]/div[2]/dl[%d]//text()" % i)
                detail_data = [x.strip() for x in html_data if x.strip() != '']

                if "电商" in detail_data or '议价' in detail_data:
                    continue
                else:
                    list_data.append(detail_data)

            list_data_info = []
            for i in list_data:
                list_data_info.append(i[1])

            if list_data:
                list_data_info.extend(detail_title_data)
                if len(list_data_info) == 11:
                    self._trimTicketInfo(list_data_info)
            else:
                continue

    def _trimTicketInfo(self, data):

        '''整理数据, 返回新列表'''
        re_data_list = copy.deepcopy(data)
        for r in data:
            a = r.strip()
            if a[:1].isdigit():
                # print(a)
                b = re.search('[0-9.-]*', a).group()
                re_data_list[re_data_list.index(r)] = b
            elif a[-1:].isdigit():
                b = re.findall('[0-9.-]*', a)
                for x in b:
                    if x != '':
                        re_data_list[re_data_list.index(r)] = str(x)
                    else:
                        continue
            else:
                continue
        # print("re匹配过的数据", re_data_list)
        new_data_dict = {}
        title_list = [
        "bill_type", # 票据类型
        "transferability", # 是否可转让
        "bill_sum", # 票据金额
        "start_time", # 出票日期
        "end_time", # 汇票到期日
        "remain_day", # 剩余天数
        "bank_type", # 承兑银行类型
        "except_rate", # 期望利率
        "except_sum" ,# 期望金额
        "accept_bank", # 承兑银行
        "send_date" # 发布时间
        ]
        print("基本值", re_data_list)

        for i in range(11):
            new_data_dict[title_list[i]] = re_data_list[i]


        print("整理好的数据为：", new_data_dict)

        clear_data.AddData(database_name='YCKT_DATA', database_set='ticket_INFO_YPJ', new_data=new_data_dict, alter_field='remain_day').judge_data()



    def run(self):
        '''启动程序'''
        # 获取ticket路径信息
        ticket_path = self._getTicketUrl()
        # 拼接票据URL
        url_list = self._configTicketUrl(ticket_path)
        # 获取票据数据
        self._getTicketInfo(url_list)
        # data = ['电银', '是', '100万元', '2018-11-14', '2019-05-14', '76天 ', '国股', '\r\n                      3.21%', '993223.33元']
        # 整理数据并保存
        # self._trimTicketInfo(data)

if __name__ == '__main__':
    start_time = time.time()
    x = 1
    while x<= 88:
        SpiderYun(x).run()
        x += 1
    print("爬取结束，用时：", time.time() - start_time)
    # 72页爬取结束，用时： 155.73225140571594
    # 88页爬取结束，用时： 202.82258200645447