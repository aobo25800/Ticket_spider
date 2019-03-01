import requests
import re
import copy
from time import sleep
from pymongo import MongoClient
from lxml import etree


client = MongoClient()
db = client.YCKT_DATA

class SpiderYun(object):

    def __init__(self, num):
        self.num = num
        print("下一页的页面为", self.num)
        sleep(1)
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        self.url_all_ticket = 'http://www.cpiaoju.com/draft?&page=%s' % self.num
        self.url_base = 'http://www.cpiaoju.com'
        self.ticket_INFO = db.ticket_INFO_YPJ

    def _getTicketUrl(self):
        '''获取票据的链接'''
        detail_html = self._parseUrl(self.url_all_ticket)
        detail_html_elements = etree.HTML(detail_html)
        elements_list = detail_html_elements.xpath("//div[@class='R_borderG clearfix R_ulcont']//a/@href")
        # elements_title_list = detail_html_elements.xpath("//div[@class='R_borderG clearfix R_ulcont']//a/@href")
        # print("elements_title_list信息为", elements_title_list)
        # print("默认返回的URL路径信息：", elements_list, "\n\t\t长度为：%s", len(elements_list))
        elements_set = set(elements_list)
        # print("使用set去重结果：", elements_set, "\n\t\t长度为：%s", len(elements_set))
        elements_set_list = list(elements_set)
        # print("去重后的URL路径列表：", elements_set_list, "\n\t\t长度为：%s", len(elements_set_list))
        return elements_set_list

    def _parseUrl(self,url):
        '''发送请求，获取响应'''
        # print(url)
        response = requests.get(url, headers=self.headers,  timeout=20)
        return response.content

    def _configTicketUrl(self, url_list):
        '''配置票据的URL'''
        url_info = []
        for ticket_path in url_list:
            group_info_url = self.url_base + ticket_path
            url_info.append(group_info_url)
        # print("组装好的URL地址数量为：", len(url_info), "组装好的URL地址:", url_info)
        return url_info

    def _getTicketInfo(self, ticket_url):
        '''获取票据数据'''
        for parse_url in ticket_url:
            detail_html = self._parseUrl(parse_url)
            detail_html_elements = etree.HTML(detail_html)
            detail_data = detail_html_elements.xpath("//div[@class='left R_seeLeft R_marginLeft1 R_marginTop50']//dd//text()")
            detail_title_data = detail_html_elements.xpath("//div[@class='R_seulp1 R_fontSize3 R_marginBot']//text()")
            # print("detail_title_data信息为", detail_title_data, "类型", type(detail_title_data))
            detail_title_data = [x.strip() for x in detail_title_data if x.strip()!='']
            # print("mytest信息为", detail_title_data, "类型", type(detail_title_data))
            detail_data.extend(detail_title_data)
            # print("detail_data信息为", detail_data, "类型", type(detail_data))
            # print("detail_title_data信息为", detail_title_data, "类型", type(detail_title_data))
            self._trimTicketInfo(detail_data)


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
        try:
            for i in range(11):
                new_data_dict[title_list[i]] = re_data_list[i]
        except Exception as e:
            print(e)

        print("整理好的数据为：", new_data_dict)
        self._ticketSave(new_data_dict)

        # return new_data_list

    def _ticketSave(self, ticket_DATA):
        '''保存信息'''
        post_id = self.ticket_INFO.insert_one(ticket_DATA).inserted_id
        print("post id is ", post_id)


    def run(self):
        '''启动程序'''
        # while True:
        # 获取ticket路径信息
        ticket_path = self._getTicketUrl()
        # # 拼接票据URL
        url_list = self._configTicketUrl(ticket_path)
        # # 获取票据数据
        self._getTicketInfo(url_list)
        # data = ['电银', '是', '100万元', '2018-11-14', '2019-05-14', '76天 ', '国股', '\r\n                      3.21%', '993223.33元']
        # 整理数据并保存
        # self._trimTicketInfo(data)

if __name__ == '__main__':
    x = 1
    while x<= 41:
        SpiderYun(x).run()
        x += 1