import time
import os
import requests
from substrateinterface import SubstrateInterface


# Moonbeam
# address = '0x0198d3053a69c3f977bb1943bc95a0ffa7777474'
# Moonriver
address = '0x55d1f6118db6fe98868eeb27002d3d8a054316f0'
rank = []


def connect():
    ws_provider = SubstrateInterface(
        url="wss://moonriver.api.onfinality.io/public-ws",
    )
    return ws_provider


def get_stakers(ws_provider):
    candidate_pool_info = ws_provider.query(
        module='ParachainStaking',
        storage_function='CandidatePool',
        params=[]
    )
    candidate_pool_info_sorted = sorted(candidate_pool_info, key=lambda item: item.get("amount"), reverse=True)
    return candidate_pool_info_sorted


def get_rank(candidate_pool_info_sorted):
    c = 0
    for i in candidate_pool_info_sorted:
        c = c + 1
        # Print all Collators
        # print(str(i) + " Current Rank: " + str(c))
        if i["owner"] == address:
            # print("Your position is: " + str(c))
            return c


def telegram_bot_sendtext(bot_message):
    bot_token = os.environ['KEY']
    bot_chatID = os.environ['CHAT']
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


try:
    while True:
        conn = connect()
        stakers = get_stakers(conn)
        rank.insert(0, get_rank(stakers))
        if len(rank) > 2:
            rank.pop(2)
            if rank[0] < rank[1]:
                telegram_bot_sendtext("✅ \n Chill, moonriver Rank changed! \n Old rank: " + str(rank[1]) + " New rank: " + str(rank[0]))
            if rank[0] > rank[1]:
                telegram_bot_sendtext("🆘 \n Alarm, moonriver Rank changed! \n Old rank: " + str(rank[1]) + " New rank: " + str(rank[0]))
        print(rank)
        time.sleep(900)
except:
    print("Whoops")
    pass
