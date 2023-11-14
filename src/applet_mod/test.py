# encoding=utf8
import ssl
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url ='https://wx.abchina.com/MiniProNew/billquery/getNormalBillList'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
}
data = {
    'data':{
        "cardNo": "6282699504599221",
        "token": "90f505181c1c49e098648b19e7127cf0",
        "pageNo": 5
    }

}

res = requests.get(url,headers=headers,json=data,verify=False)

print(res.text)