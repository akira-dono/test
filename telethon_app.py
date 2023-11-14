from telethon import TelegramClient, events, types
from db import get_user_by_tg_id, get_text, get_user_ids
# from config import api_id, api_hash, chat_id #? Твои импорты из конфига
from bot import bot;
# from telethon.tl.functions.channels import JoinChannelRequest

client = TelegramClient('tg_session', api_id, api_hash, system_version='4.16.30-vxCUSTOM')

async def check_chat_type(chat_id):
    entity = await client.get_entity(chat_id)
    if isinstance(entity, types.User):
        print("Личный чат")
        return 0
    elif isinstance(entity, types.Chat):
        print("Группа")
        return 1
    elif isinstance(entity, types.Channel):
        print("Канал")
        return 2

@client.on(events.NewMessage)
async def my_event_handler(event):
    
    #! Скорее всего придется переписать
    ids = get_user_ids()
    for id in ids:
        await client.get_dialogs()
        event_msg = event.message
        text_msg = event_msg.message
        peer_id = event_msg.chat_id
        entity_type = await check_chat_type(peer_id)
        if entity_type == 2 and get_user_by_tg_id(id[0]) is not None:
            if get_text(id[0]) in text_msg:
                try:
                    await bot.send_message(id[0], text_msg)
                except ValueError as e:
                    print(e)

#! link = "https://t.me/test_128637518923"
#! entity = await client.get_entity(link)
#! await client(JoinChannelRequest(entity))

client.start()
client.run_until_disconnected()


