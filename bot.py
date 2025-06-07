from web3 import Web3
import time
import requests

# RPC لشبكة BNB
bsc_rpc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc_rpc))

# عنوان عقد الزوج CTC/USDT على PancakeSwap V3
pair_address = Web3.to_checksum_address('0xaF3662d3809a590902Ed8a0127bbd244874fA659')

# ABI لعقد الزوج (getReserves فقط)
pair_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "getReserves",
        "outputs": [
            {"name": "_reserve0", "type": "uint112"},
            {"name": "_reserve1", "type": "uint112"},
            {"name": "_blockTimestampLast", "type": "uint32"},
        ],
        "type": "function",
    }
]

pair = web3.eth.contract(address=pair_address, abi=pair_abi)

# بيانات Telegram
TELE_TOKEN = '7728299479:AAEDJsYEdPe3YKABXD2AqqLKZRQbhDj-P9sا'  # استبدل هذا بالتوكن الخاص ببوتك
CHAT_ID = '6444681745ا'     # استبدل هذا بالـ chat id الخاص بك

def send_telegram(msg):
    url = f'https://api.telegram.org/bot{TELE_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': msg}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("خطأ أثناء إرسال الرسالة:", e)

last_r0, last_r1 = None, None

def check_liquidity():
    global last_r0, last_r1
    reserves = pair.functions.getReserves().call()
    r0, r1 = reserves[0], reserves[1]

    if last_r0 is not None and (r0 != last_r0 or r1 != last_r1):
        msg = (
            "🔔 تم تغيير السيولة لزوج CTC/USDT\n"
            f"🟢 Reserve0 (CTC): {r0}\n"
            f"💰 Reserve1 (USDT): {r1}"
        )
        print(msg)
        send_telegram(msg)

    last_r0, last_r1 = r0, r1

print("✅ بدء مراقبة السيولة...")
while True:
    try:
        check_liquidity()
    except Exception as e:
        print("خطأ:", e)
    time.sleep(10)