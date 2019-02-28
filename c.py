# a = ['\r\n         ', '\r\n         ', '葫芦岛银行股份有限公司沈阳北顺城支行', '\r\n         ', '发布日期：2019-02-28 ', '\r\n      ']
# # for i in a:
#     # a = i.strip("\r\n")
#     #
#     # if a == "":
#     #     a.remove(i)
# # print(a[2])
# s=[x.strip() for x in a]
# print(s)
# s=[x.strip() for x in a if x.strip()!='']
# print(s)

import re

a = '发布日期：2019-02-28 '
b = re.search('[0-9.-]*', a).group()
print(b)