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
count = 0
while (count < 18):
    time.sleep(300)
    KR = price_monitor(KR_tesla, 8)
    US = price_monitor(US_tesla, 5)
    CN = price_monitor(CN_tesla, 6)

    for list in [KR, US, CN]:
        if list == KR:
            KR_message = "Korea" + " 종류: " + str(list[0]) + ", 가격(KRW) :"
            for i in range(len(list[1])):
                KR_message = KR_message + " " + str(list[1][i])
            if list[0] != 2:
                bot.sendMessage(mc, '한국 모델변경\n' + KR_message)
                count += 1
            if list[1][0] != 92390000 or list[1][1] != 84990000:
                bot.sendMessage(mc, '한국 가격변경\n' + KR_message)
                count += 1
        elif list == US:
            US_message = "USA" + " 종류: " + str(list[0]) + ", 가격(USD) :"
            for i in range(len(list[1])):
                US_message = US_message + " " + str(list[1][i])
            if list[0] != 2:
                bot.sendMessage(mc, '미국 모델변경\n' + US_message)
                count += 1
            if list[1][0] != 67990 or list[1][1] != 62990:
                bot.sendMessage(mc, '미국 가격변경\n' + US_message)
                count += 1
        elif list == CN:
            CN_message = "China" + " 종류: " + str(list[0]) + ", 가격(CNY) :"
            for i in range(len(list[1])):
                CN_message = CN_message + " " + str(list[1][i])
            if list[0] != 3:
                bot.sendMessage(mc, '중국 모델변경\n' + CN_message)
                count += 1
            if list[1][0] != 375900 or list[1][1] != 417900 or list[1][2] != 316900:
                bot.sendMessage(mc, '중국 가격변경\n' + CN_message)
                count += 1
    
    now = datetime.now()
    current_time = now.strftime("%H")
    min = now.strftime("%M")
    if current_time == "22" and 43<= int(min) <= 48:
        bot.sendMessage(mc, KR_message)
        bot.sendMessage(mc, US_message)
        bot.sendMessage(mc, CN_message)

# print(KR_message)
# print(US_message)
# print(CN_message)


# bot.sendMessage(mc,KR_message)
# bot.sendMessage(mc,US_message)
# bot.sendMessage(mc,CN_message)
