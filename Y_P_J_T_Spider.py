import requests
from lxml import etree


url = 'http://www.cpiaoju.com/Draft/detail/35125.html'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

# div class="container R_seecont R_borderG R_backg R_marginTop2 clearfix"

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
#
content = response.text[5110:-14899]


print("content类型", type(content), "content内容为：", content)
html = etree.HTML(content)

# print("_html对象：", html)

div_list = html.xpath("//div[@class='left R_seeLeft R_marginLeft1 R_marginTop50']//dl[8]//span/text()")

x = div_list[0].replace(' ', '')

y = x.replace('\r\n','')
print(y)
div_li = []
div_li.append(y)
print(type(y),"div_list内容为：", div_li)
#
# for li in li_list:
#     item = {}
#     item["href"] = li.xpath("./a/@href")[0] if len(li.xpath("./a/@href"))>0 else None
#     item["title"] = li.xpath("./a/text()")[0] if len(li.xpath("./a/text()"))>0 else None
#     print(item)

# content_list = []
# for div in div_list:
#     item = {}
#     item["title"] = div.xpath("//div[@class='left R_seeLeft R_marginLeft1 R_marginTop50']//dl")[8]
#     content_list.append(item)
#
# print(content_list)