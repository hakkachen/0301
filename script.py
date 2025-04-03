#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
import time
from itertools import product

# Telegram Bot 設定
TELEGRAM_BOT_TOKEN = "7795529893:AAHMUzaZHj4rVrG4rVF2fmdp6Hmln9wkQqU"
TELEGRAM_CHAT_ID = "2060001903"  # 你的 Chat ID

# 帳號列表
accounts = [
    ("門號1", {'ck_encust': '3202821113257996', 'isEN': '27f628244f185ab824e2161621ed06b2dfb9432d'}),
    ("門號2", {'ck_encust': '3202821183400259', 'isEN': '443a082ada6cded408011323b35d65eb70011fbf'}),
    ("門號3", {'ck_encust': '3202831064445006', 'isEN': '4dc9781e02865227cc3e756c63c084db2ab6f2d9'}),
    ("門號4", {'ck_encust': '3202221133407108', 'isEN': '79214509e8c5748b2b31e2c917e3f021c7e6cba4'}),
    ("門號5", {'ck_encust': '3201541209015560', 'isEN': '49af10540904497c1a8b6d9bdb6219811554754f'}),
]

# 活動編號與禮品碼
m_promo_no = "M25040100022"
dt_promo_no_array = ["D25040100001"]
gift_code_array = ["rice"]

def send_telegram_message(message):
    """發送訊息到 Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Telegram 訊息發送成功")
        else:
            print(f"Telegram 訊息發送失敗: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Telegram 發送失敗: {e}")

def send_long_message(message, chunk_size=4096):
    """避免訊息過長，Telegram 單則訊息最多 4096 字"""
    for i in range(0, len(message), chunk_size):
        send_telegram_message(message[i:i+chunk_size])

def sign_in_account(account, m_promo_no, dt_promo_no, gift_code, results):
    """執行 momo 抽獎動作"""
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
        "gift_code": gift_code,
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

def main():
    # 確保 gift_code_array 不為空
    if not gift_code_array:
        gift_code_array.append("default_code")  # 預設禮品碼

    # 開始執行 momo 抽獎
    results = []
    for account, dt_promo_no, gift_code in product(accounts, dt_promo_no_array, gift_code_array):
        sign_in_account(account, m_promo_no, dt_promo_no, gift_code, results)

    # 傳送抽獎結果
    all_results_message = "\n".join(results)
    send_long_message(all_results_message)

if __name__ == "__main__":
    main()
