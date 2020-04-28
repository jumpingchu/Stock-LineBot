import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from datetime import date


def get_data(url, columns):
    """
    取得資料並存成表格
    回傳一個 pandas dataframe
    """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html5lib')

    trs = soup.find('tbody').find_all('tr')
    data = []
    for tr in trs:
        data.append(tr.text.split())

    df = pd.DataFrame(data[1:], columns=columns)

    # 篩選:未截止 & 報酬率>10%
    df = df[df['備註'] != '已截止']
    df = df[df['總合格件/中籤率(%)'] != '已截止']
    df = df[df['報酬率(%)'].astype(float) > 10]

    # 新增欄位: 轉帳金額
    df['轉帳金額'] = df['承銷價'].astype(float) * df['申購張數'].astype(int) * 1000 + 70

    # 新增欄位: 預約轉帳日
    two_days = datetime.timedelta(2)
    df['抽籤日期'] = pd.to_datetime(df['抽籤日期'], format='%Y/%m/%d')
    df['預約轉帳日'] = df['抽籤日期'] - two_days
    df['預約轉帳日'] = df['預約轉帳日'].astype(str)
    df_simple = df[['股票代號', '名稱', '報酬率(%)', '轉帳金額', '預約轉帳日']]
    return df_simple


def to_jsonfile(data):
    with open('stock_public.json', 'w', encoding='utf-8') as file:
        data.to_json(file, force_ascii=False)


# 資料來源
url = 'https://histock.tw/stock/public.aspx'

# 整理欄位標題
columns = ['抽籤日期', '股票代號', '名稱', '發行市場', '申購期間', '撥券日期', '承銷張數',
           '承銷價', '市價', '獲利', '報酬率(%)', '申購張數', '總合格件/中籤率(%)', '備註']


def main():
    df = get_data(url, columns)
    df.index += 1   # 讓使用者看到 1,2,3,4...而不是0,1,2,3...
    to_jsonfile(df)
    print(df[['股票代號', '名稱', '報酬率(%)']])

    switch = True
    stock_list = []

    # 迴圈輸入想要抽的股票編號
    while switch:
        try:
            stock = int(input('輸入編號: '))
            if stock >= 0:
                stock_list.append(stock)
            else:
                stock_list.pop(abs(stock))
        except ValueError:
            switch = False

    total = 0
    content = ''
    for ind in stock_list:
        num = df.loc[ind].values[0]
        name = df.loc[ind].values[1]
        date = df.loc[ind].values[4]
        price = df.loc[ind].values[3]
        total += price
        content += '\n申購 {num}{name}:\n請設定 【{date}】 轉帳 【{price}】 元'.format(
            **locals())
        print('\n申購 {num}{name}:\n請設定 【{date}】 轉帳 【{price}】 元'.format(**locals()))

    if len(stock_list) > 1:
        content += '\n總金額: ' + str(total)
        print('\n總金額: ' + str(total))

    # 存檔做當日紀錄
    today = datetime.datetime.now()
    year, month, day = str(today.year), str(today.month), str(today.day)
    today_str = '{year}-{month}-{day}'.format(**locals())
    with open(today_str + '.txt', 'w+', encoding='utf-8') as f:
        f.write(content)


if __name__ == "__main__":
    main()
