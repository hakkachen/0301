import aiohttp
import asyncio
import json
import time
import nest_asyncio



# Telegram Bot 設定
TELEGRAM_BOT_TOKEN = "7795529893:AAHMUzaZHj4rVrG4rVF2fmdp6Hmln9wkQqU"
TELEGRAM_CHAT_ID = "2060001903"

# 帳號列表，包含門號與 cookies
accounts = [
    ("門號1", {'ck_encust': '3202821113257996', 'isEN': '27f628244f185ab824e2161621ed06b2dfb9432d'}),
    ("門號2", {'ck_encust': '3202821183400259', 'isEN': '443a082ada6cded408011323b35d65eb70011fbf'}),
    ("門號3", {'ck_encust': '3202831064445006', 'isEN': '4dc9781e02865227cc3e756c63c084db2ab6f2d9'}),
    ("門號4", {'ck_encust': '3202221133407108', 'isEN': '79214509e8c5748b2b31e2c917e3f021c7e6cba4'}),
    ("門號5", {'ck_encust': '3201541209015560', 'isEN': '49af10540904497c1a8b6d9bdb6219811554754f'}),
]

m_promo_no = "M26010100179"
dt_promo_no_array = ["D26010100001"]
gift_code_array = ["gift001"]

# 定義發送 Telegram 消息的函式
async def send_telegram_message(session, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"  # 使用 HTML 格式以支持換行
    }
    async with session.post(url, json=data) as response:
        return await response.text()

# 定義註冊函式，用來向指定的 URL 發送請求
async def sign_in_account(session, account, m_promo_no, dt_promo_no, gift_code):
    headers = {
        'User-Agent': 'MOMOSHOP',
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'event.momoshop.com.tw',
        'Origin': 'https://www.momoshop.com.tw',
        'Referer': 'https://www.momoshop.com.tw/',
    }

    # 使用指定帳號的 cookies
    cookies = account[1]

    # 請求的 JSON 資料
    data = {
        "m_promo_no": m_promo_no,
        "dt_promo_no": dt_promo_no,
        "gift_code": gift_code,
        "doAction": "reg"
    }

    # 發送 POST 請求並返回響應
    async with session.post('https://event.momoshop.com.tw/promoMechReg.PROMO', headers=headers, json=data, cookies=cookies) as response:
        return await response.text()

# 定義帶有延遲的執行函式，每個帳號最多執行 50 次
async def execute_with_delay(account, m_promo_no, dt_promo_no_array, gift_code_array, max_attempts=1):
    attempt_count = 0  # 記錄已執行的次數
    async with aiohttp.ClientSession() as session:
        while attempt_count < max_attempts:  # 當次數少於 max_attempts 時，繼續執行
            for dt_promo_no, gift_code in zip(dt_promo_no_array, gift_code_array):
                result = await sign_in_account(session, account, m_promo_no, dt_promo_no, gift_code)
                # 格式化結果訊息
                message = f"<b>{account[0]}</b> 回傳值: {result}"
                print(message)
                # 發送結果到 Telegram
                await send_telegram_message(session, message)
                attempt_count += 1  # 增加已執行次數
                if attempt_count >= max_attempts:  # 若達到最大執行次數，結束迴圈
                    return
                await asyncio.sleep(0)  # 延遲下一次請求

# 主函式，用於啟動多個帳號的註冊程序
async def main():
    start_time = time.time()
    # 為每個帳號創建一個執行任務
    tasks = [execute_with_delay(account, m_promo_no, dt_promo_no_array, gift_code_array) for account in accounts]
    await asyncio.gather(*tasks)  # 並行執行所有任務
    end_time = time.time()
    total_time = end_time - start_time
    # 發送總執行時間到 Telegram
    time_message = f"Total execution time: {total_time:.2f} seconds"
    print(time_message)
    async with aiohttp.ClientSession() as session:
        await send_telegram_message(session, time_message)

if __name__ == "__main__":
    asyncio.run(main())
