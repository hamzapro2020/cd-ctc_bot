import time
from web3 import Web3
from telegram import Bot

# إعداد الاتصال بـ BSC
bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

# إعدادات التليغرام
TELE_TOKEN = "7728299479:AAEDJsYEdPe3YKABXD2AqqLKZRQbhDj-P9s"
CHAT_ID = "6444681745"
bot = Bot(token=TELE_TOKEN)

# عنوان العقد
token_address = Web3.to_checksum_address("0x612a8770649aff0c9838c4fbd5e5e546c4dd3d7c")

# عنوان السيولة، نحتاج عنوان زوج Pair على PancakeSwap (يمكنني مساعدتك بالحصول عليه لو أردت)
pair_address = Web3.to_checksum_address("عنوان_زوج_السيولة")

# ABI بسيط للاستعلام عن الرصيد
abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]'
contract = web3.eth.contract(address=token_address, abi=abi)

last_liquidity = 0

while True:
    try:
        # الحصول على رصيد السيولة من العقد
        liquidity = contract.functions.balanceOf(pair_address).call()

        if liquidity != last_liquidity:
            msg = f"📈 تغيّرت السيولة! السيولة الآن: {liquidity / 1e18:.4f} CTC"
            bot.send_message(chat_id=CHAT_ID, text=msg)
            last_liquidity = liquidity

        time.sleep(30)

    except Exception as e:
        print(f"❌ خطأ: {e}")
        time.sleep(10)