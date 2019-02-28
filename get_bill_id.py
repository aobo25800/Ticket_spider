import json
import requests

url = 'https://www.pengpengpiao.com/ppp/bills/filterbill'

json_data = {
	"acceptor": "",
	"acceptorType": "",
	"amountType": "",
	"billType": "",
	"maturityType": "",
	"number": 107,      # 票据总数量
	"starter": 40,      # 票据开始数量
	"userId": "da154db0-e7fd-436b-bcbf-"

}


response = requests.post(url, json=json_data)
data = response.text

data_dict = json.loads(data)

# print("data类型", type(data_dict), data_dict)

data_list = []
date_list = []
for i in range(len(data_dict["list"])):
    i_dict = {}
    i_dict["billiId"] = data_dict["list"][i]["billId"]
    i_dict["status"] = "已签收"
    data_list.append(i_dict)
    date_list.append(data_dict["list"][i]["releaseDate"])


data_list = str(data_list).replace("'", '"')
print(data_list, '\n', date_list, len(date_list))