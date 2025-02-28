#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
requests.packages.urllib3.disable_warnings()
import json
import time

# LINE Notify 訪問令牌
LINE_NOTIFY_TOKEN = 'dAFSmsbnBxpaUqbYTShnSWL8yZ7f5iIzpoTD3w57e2b'

# 帳號列表
accounts = [
    ("門號1", {'ck_encust': '3202821113257996', 'isEN': '27f628244f185ab824e2161621ed06b2dfb9432d'}),
    ("門號2", {'ck_encust': '3202821183400259', 'isEN': '443a082ada6cded408011323b35d65eb70011fbf'}),
    ("門號3", {'ck_encust': '3202831064445006', 'isEN': '4dc9781e02865227cc3e756c63c084db2ab6f2d9'}),
    ("門號4", {'ck_encust': '3202221133407108', 'isEN': '79214509e8c5748b2b31e2c917e3f021c7e6cba4'}),
    ("門號5", {'ck_encust': '3201541209015560', 'isEN': '49af10540904497c1a8b6d9bdb6219811554754f'}),
]

# 定義活動編號和禮品碼
m_promo_no = "M25030100017"
dt_promo_no_array = [
    "D25030100001"
]
gift_code_array = ["dumpling"]

def send_line_notify(message):
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"message": message}
    try:
        response = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)
        if response.status_code == 200:
            print("LINE Notify 發送成功")
        else:
            print(f"LINE Notify 發送失敗: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"LINE Notify 發送失敗: {e}")

def send_long_message(message):
    max_length = 1000
    while len(message) > 0:
        send_line_notify(message[:max_length])
        message = message[max_length:]
        time.sleep(1)  # 避免發送過快，被限制

def sign_in_account(account, m_promo_no, dt_promo_no, results):
    print("------------------------")
    t = time.localtime()
    time2 = time.strftime("%Y/%m/%d %H:%M:%S", t)
    print(time2)

    print("------------------------")
    print(f"帳號:{account[0]}")
    print(f"ID:{account[1]['ck_encust']}")

    headers = {
        'User-Agent': 'MOMOSHOP',
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'event.momoshop.com.tw',
        'Origin': 'https://www.momoshop.com.tw',
        'Referer': 'https://www.momoshop.com.tw/',
    }

    cookies = account[1]

    json_data_lottery = {
        "m_promo_no": m_promo_no,
        "dt_promo_no": dt_promo_no,
        'doAction': 'lottery',
    }    
    
    try:
        response = requests.post('https://event.momoshop.com.tw/promoMechReg.PROMO', cookies=cookies, headers=headers, json=json_data_lottery)
        print(response.text)
        results.append(f"帳號:{account[0]} 抽獎結果: {response.text}")
    except requests.exceptions.RequestException as e:
        error_message = f"帳號:{account[0]} 抽獎動作失敗: {e}"
        print(error_message)
        results.append(error_message)
    
    print("-----------------------")

# 自動簽到
results = []
for _ in range(1):  # 這裡的循環會讓簽到動作執行兩次
    for account in accounts:
        for dt_promo_no in dt_promo_no_array:
            sign_in_account(account, m_promo_no, dt_promo_no, results)

# 發送所有結果
all_results_message = "\n".join(results)
send_long_message(all_results_message)
