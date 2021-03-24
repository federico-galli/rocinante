#!/usr/bin/env python

from telethon import TelegramClient, events
import json
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

from fortunate import Fortunate

# sample json config file
# {
#     "name" : "mysession",
#     "api_id" : "apiid",
#     "api_hash" : "apihash",
#     "forward_from_channel" : -1001234567,
#     "forward_to_channel" : "somechannell"
# }

with open('config.json') as json_file:
    config=json.load(json_file)
from_channel=config["forward_from_channel"]
to_channel=config["forward_to_channel"]


# initialize the telegram client with configs from config.json
client = TelegramClient(config["name"], config["api_id"], config["api_hash"])
# this will let telethon know the identities ids
dialogs = client.get_dialogs()

# tell fortunes on "givemeacookie" message - this is an easter egg
@client.on(events.NewMessage)
async def tellFortunes(event):
    if 'givemeacookie' in event.raw_text.lower():
        fortunegenerator=Fortunate('/usr/share/games/fortune')
        try:
            await event.reply(fortunegenerator())
        except:
            await event.reply(fortunegenerator())

# read new messages from chat and forward to another
@client.on(events.NewMessage(chats=from_channel, pattern=r'(?i).*(buy|ta+rge+t)'))
async def newMessageListener(event):
    print('regex matched', event.message.raw_text)
    await client.forward_messages(to_channel, event.message)
    
@client.on(events.MessageEdited(chats=from_channel,pattern=r'(?i).*(buy|ta+rge+t)'))
async def editTestListener(event):
    print('Message', event.id, 'changed at', event.date)
    await client.forward_messages(to_channel, event.message)

# print all dialogs ids for debug
async def main():
    async for dialog in client.iter_dialogs():
         print(dialog.name, 'has ID', dialog.id)

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()