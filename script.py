#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
requests.packages.urllib3.disable_warnings()
import json
import time

pNo1 = "U120250301"
line_notify_token = 'P2r0eM5lqbShPP9Nnzps3L4IGF5GddodiTseFbKVBkv'
line_notify_api = 'https://notify-api.line.me/api/notify'

accounts = [
    ("門號1", {'ck_encust': '3202821113257996', 'isEN': '27f628244f185ab824e2161621ed06b2dfb9432d'}),
    ("門號2", {'ck_encust': '3202821183400259', 'isEN': '443a082ada6cded408011323b35d65eb70011fbf'}),
    ("門號3", {'ck_encust': '3202831064445006', 'isEN': '4dc9781e02865227cc3e756c63c084db2ab6f2d9'}),
    ("門號4", {'ck_encust': '3202221133407108', 'isEN': '79214509e8c5748b2b31e2c917e3f021c7e6cba4'}),
    ("門號5", {'ck_encust': '3201541209015560', 'isEN': '49af10540904497c1a8b6d9bdb6219811554754f'}),
]

def line_notify(message):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + line_notify_token
    }
    payload = {'message': message}
    response = requests.post(line_notify_api, headers=headers, data=payload)
    return response.status_code

def sign_in_account(account, pNo):
    print("------------------------")
    t = time.localtime()
    time2 = time.strftime("%Y/%m/%d %H:%M:%S", t)
    print(time2)

    print("------------------------")
    print(f"帳號:{account[0]}")
    print(f"ID:{pNo}")

    headers = {
        'user-agent': 'MOMOSHOP',
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'event.momoshop.com.tw',
        'Origin': 'https://www.momoshop.com.tw',
        'Referer': 'https://www.momoshop.com.tw/',
    }

    cookies = requests.utils.cookiejar_from_dict(account[1])
    data = {"pNo": pNo, "doAction": "taskFinished"}
    r = requests.post('https://event.momoshop.com.tw/punch.PROMO', headers=headers, data=json.dumps(data), cookies=cookies)
    task_finished_response = r.text

    data = {"pNo": pNo, "doAction": "reg"}
    r = requests.post('https://event.momoshop.com.tw/punch.PROMO', headers=headers, data=json.dumps(data), cookies=cookies)
    reg_response = r.text

    data = {"pNo": pNo, "doAction": "sel"}
    r = requests.post('https://event.momoshop.com.tw/punch.PROMO', headers=headers, data=json.dumps(data), cookies=cookies)
    sel_response = r.text

    print("-----------------------")
    
    return f"帳號: {account[0]}\nID: {pNo}\nTask Finished Response: {task_finished_response}\nReg Response: {reg_response}\nSel Response: {sel_response}\nTime: {time2}\n"

def send_long_message(message, chunk_size=1000):
    for i in range(0, len(message), chunk_size):
        line_notify(message[i:i+chunk_size])

def main():
    message = ""
    for account in accounts:
        message += sign_in_account(account, pNo1) + "\n"
    
    send_long_message(message)

if __name__ == "__main__":
    main()
