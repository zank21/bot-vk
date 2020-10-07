from vk_api.bot_longpoll import VkBotEventType
import vk_api
import app.bot.main
import app.chat.main
from settings import token, group_id
import error_num

URL = {
    '': error_num.error_url,
    '1': app.bot.main.main,
    '2': app.chat.main.main

}


def process(event: vk_api.bot_longpoll.VkBotMessageEvent):
    if 'payload' in event.obj.keys():
        payload = str(event.obj['payload'])
    else:
        vk_session = vk_api.VkApi(
            token=token)
        history = vk_session.method(method='messages.getHistory', values={
            'peer_id': event.obj['from_id'],
            'extended': 1,
            'count': 50
        })
        payload = '0'
        for message in history['items']:
            if message['from_id'] == -1 * group_id:
                payload = message['payload']
                break

    payload = payload.split('0')
    command = URL[payload[0]]
    command(event, payload)
