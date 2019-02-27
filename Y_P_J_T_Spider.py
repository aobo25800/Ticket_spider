import requests
import re
import copy
from lxml import etree


# url = 'http://www.cpiaoju.com/Draft/detail/35125.html'
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
#
# # div class="container R_seecont R_borderG R_backg R_marginTop2 clearfix"
#
# response = requests.get(url, headers=headers)
# response.encoding = 'utf-8'
# #
# content = response.text[5110:-14899]
#
#
# print("content类型", type(content), "content内容为：", content)
# html = etree.HTML(content)
#
# # print("_html对象：", html)
#
# div_list = html.xpath("//div[@class='left R_seeLeft R_marginLeft1 R_marginTop50']//dl[8]//span/text()")
# div_list1 = html.xpath("//div[@class='R_seulp1 R_fontSize3 R_marginBot']//text()")
#
# x = div_list[0].replace(' ', '')
#
# y = x.replace('\r\n','')
# print(y)
# div_li = []
# div_li.append(y)
# print(type(y),"div_list内容为：", div_li)
#
# print(div_list1)




class SpiderYun(object):

    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        self.url_all_ticket = 'http://www.cpiaoju.com/Draft'
        self.url_base = 'http://www.cpiaoju.com'


    def _getTicketUrl(self):
        '''获取票据的链接'''
        detail_html = self._parseUrl(self.url_all_ticket)
        detail_html_elements = etree.HTML(detail_html)
        elements_list = detail_html_elements.xpath("//div[@class='R_borderG clearfix R_ulcont']//a/@href")
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
            print(detail_data)
            return detail_data

    def _trimTicketInfo(self, data):

        '''整理数据, 返回新列表'''
        re_data_list = copy.deepcopy(data)
        for r in data:
            try:
                data_re = re.search('\d+\W\d+\W\d+', r).group()
                data_re_a = re.search(r'\d+.\d+', r).group()
                data_re_b = re.search('\d+', r).group()
                if data_re:
                    print(data_re)
                    re_data_list[re_data_list.index(r)] = data_re
                elif data_re_a:
                    print(data_re_a)
                    re_data_list[re_data_list.index(r)] = data_re_a
                elif data_re_b:
                    print(data_re_b)
                    re_data_list[re_data_list.index(r)] = data_re_b
                else:
                    pass

            except Exception as e:
                print(e)
        print("re匹配过的数据", re_data_list)
        new_data_list = []
        for i in data:
            data_str = i.strip()
            # print(data_str)
            # if data_str == '':
            #     continue
            # else:
            new_data_list.append(data_str)
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
        "except_sum" # 期望金额
        ]
        for i in range(9):
            new_data_dict[title_list[i]] = new_data_list[i]


        print("整理好的数据为：", new_data_dict)
        # return new_data_list

    def _ticketSave(self):
        '''保存信息'''
        pass

    def run(self):
        '''启动程序'''
        # 获取ticket路径信息
        # ticket_path = self._getTicketUrl()
        # 拼接票据URL
        # url_list = self._configTicketUrl(ticket_path)
        # 获取票据数据
        # data = self._getTicketInfo(url_list)
        data = ['电银', '是', '100万元', '2018-11-14', '2019-05-14', '76天 ', '国股', '\r\n                      3.21%', '993223.33元']
        # 整理数据并返回
        self._trimTicketInfo(data)

if __name__ == '__main__':
    SpiderYun().run()