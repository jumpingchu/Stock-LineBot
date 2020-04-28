from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage

import requests
from bs4 import BeautifulSoup
import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def get_page(url):
    resp = requests.get(url)
    resp.encoding == 'utf-8'
    soup = BeautifulSoup(resp.text, 'html5lib')
    return soup

def date_cal(time):
    weekno = time.weekday() + 1
    if weekno == 1: #抽籤日為周一: 扣4天=轉帳日 
        time_transfer = time - (datetime.timedelta(4))
    else: #抽籤日為二到五: 扣2天=轉帳日
        time_transfer = time - (datetime.timedelta(2))
    return time_transfer

def get_data(event):
    url = 'https://histock.tw/stock/public.aspx'
    soup = get_page(url)
    trs = soup.find_all('tr')
    dict_stock = []
    text = ''
    for tr in trs:
        if tr.find('a'):
            try:
                roi = float(tr.select('td')[9].text.strip()) 
            except:
                break #排除負數
            
            # 篩選: 報酬率>10% & 尚未抽籤
            time_str = tr.select('td')[0].text.strip()
            time = datetime.datetime.strptime(time_str, '%Y/%m/%d')
            if roi > 10.0 and time > datetime.datetime.today():
                name = tr.select('td')[1].text.split()
                price = tr.select('td')[6].text
                num = tr.select('td')[10].text
                time_transfer = date_cal(time) # 處理周末
                if len(tr.select('td')[-1].text.split()) == 0: # 處理偶發的例外
                    end = '無'
                else: 
                    end = tr.select('td')[-1].text.split()[0]
                dict_stock.append({
                    '抽籤日': '{}/{}/{}'.format(time.year, time.month, time.day),
                    '預約轉帳日': '{}/{}/{}'.format(time_transfer.year, time_transfer.month, time_transfer.day),
                    '股票代號': name[0],
                    '股票名稱': name[1],
                    '總金額': int(float(price) * int(num) * 1000 + 70),
                    '報酬率': str(roi) + '%',
                    '備註': end
                })
            
    if len(dict_stock) != 0:
        for data in dict_stock:
            text += '【' + data['股票代號'] + ' ' + data['股票名稱'] + '】\n'
            text += '・抽籤日: ' + data['抽籤日'] + '\n'
            text += '・狀態: ' + str(data['備註']) + '\n'
            text += '・報酬率: ' + data['報酬率'] + '\n'
            text += '・金額: ' + str(data['總金額']) + '\n'
            text += '・轉帳日: ' + data['預約轉帳日'] + '\n\n'
    else:
        text += '目前沒有值得抽的股票唷~'
    try:
        message = TextSendMessage(
            text=text.rstrip()
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))

def other(event):
    try:
        message = TextSendMessage(
            text='抱歉! 我不太懂您的意思'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('錯誤!'))
        