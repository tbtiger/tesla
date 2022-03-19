import requests
from bs4 import BeautifulSoup
import re
import telepot
from datetime import datetime
import time


def price_monitor(url, unit):
    price = []
    req = requests.get(url)  # "https://www.tesla.com/ko_KR/modely/design?redirect=no#overview")
    # req.text
    soup = BeautifulSoup(req.content, "html.parser")
    # print(soup)
    tesla = str(soup.body.script)
    tesla = tesla.replace("\\", "&")
    tesla = tesla.replace("\"", "&")
    scriptParse_iter = re.finditer("base_plus_trim&&,&&value&&:", tesla)
    num = 0
    for scriptParse in scriptParse_iter:
        # print(scriptParse)
        # print(scriptParse.group())
        # print(scriptParse.end())
        # end = scriptParse.end()
        # print(tesla[scriptParse.end():scriptParse.end()+8])
        # print(int(tesla[scriptParse.end():scriptParse.end()+8]))
        price.append(int(tesla[scriptParse.end():scriptParse.end() + unit]))
        num = num + 1
    # print(num)
    # print(price)
    return num, price


KR_tesla = "https://www.tesla.com/ko_KR/modely/design?redirect=no#overview"
US_tesla = "https://www.tesla.com/modely/design?redirect=no#overview"
CN_tesla = "https://www.tesla.cn/modely/design?redirect=no#overview"

# print(KR)
# print(US)
# print(CN)
token = '5168734909:AAHNEAc-pRfsv4jVetzQ_t369WqO6ZY_Mqc'
mc = '2109879317'
bot = telepot.Bot(token)
count_KR_model = 0
count_KR_price = 0
count_US_model = 0
count_US_price = 0
count_CN_model = 0
count_CN_price = 0
while (True):
    time.sleep(60)
    KR = price_monitor(KR_tesla, 8)
    US = price_monitor(US_tesla, 5)
    CN = price_monitor(CN_tesla, 6)

    for list in [KR, US, CN]:
        if list == KR:
            KR_message = "Korea" + " Model Y 종류: " + str(list[0]) + ", 가격(KRW) :"
            for i in range(len(list[1])):
                KR_message = KR_message + " " + str(list[1][i])
            if list[0] != 2 and count_KR_model <5:
                bot.sendMessage(mc, '한국 모델변경\n' + KR_message)
                count_KR_model += 1
            if (list[1][0] != 92390000 or list[1][1] != 84990000) and count_KR_price <5:
                bot.sendMessage(mc, '한국 가격변경\n' + KR_message)
                count_KR_price += 1
        elif list == US:
            US_message = "USA" + " Model Y 종류: " + str(list[0]) + ", 가격(USD) :"
            for i in range(len(list[1])):
                US_message = US_message + " " + str(list[1][i])
            if list[0] != 2 and count_US_model <5:
                bot.sendMessage(mc, '미국 모델변경\n' + US_message)
                count_US_model += 1
            if (list[1][0] != 67990 or list[1][1] != 62990) and count_US_price <5 :
                bot.sendMessage(mc, '미국 가격변경\n' + US_message)
                count_US_price += 1
        elif list == CN:
            CN_message = "China" + " Model Y 종류: " + str(list[0]) + ", 가격(CNY) :"
            for i in range(len(list[1])):
                CN_message = CN_message + " " + str(list[1][i])
            if list[0] != 3 and count_CN_model <5:
                bot.sendMessage(mc, '중국 모델변경\n' + CN_message)
                count_CN_model += 1
            if (list[1][0] != 375900 or list[1][1] != 417900 or list[1][2] != 316900) and count_CN_price <5:
                bot.sendMessage(mc, '중국 가격변경\n' + CN_message)
                count_CN_price += 1

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    min = now.strftime("%M")
    if int(min) == 10:
        bot.sendMessage(mc, "Model Y monitoring WORKS FINE")
        bot.sendMessage(mc, KR_message)

# print(KR_message)
# print(US_message)
# print(CN_message)


# bot.sendMessage(mc,KR_message)
# bot.sendMessage(mc,US_message)
# bot.sendMessage(mc,CN_message)
