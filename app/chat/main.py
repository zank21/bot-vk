from vk_api.bot_longpoll import VkBotEventType
import vk_api
from vk_functions import get_random_number
from settings import token


def main(event: vk_api.bot_longpoll.VkBotMessageEvent, payload):
    values = {
        'user_id': event.obj['from_id'],
        'random_id': get_random_number(),
        'payload': 2,
    }

    if event.obj['text'] != '':
        values.update({'message': event.obj['text']})

    if 'attachments' in event.obj.keys():
        attachment_list = []
        for item in event.obj['attachments']:
            type_attachment = item['type']
            if type_attachment == 'sticker':
                sticker_id = item[type_attachment]['sticker_id']
                values.update({'sticker_id': sticker_id})
                break
            else:
                if 'access_key' in item[type_attachment]:
                    access_key = item[type_attachment]['access_key']
                    attachment = '{}{}_{}_{}'.format(type_attachment, item[type_attachment]['owner_id'],
                                                     item[type_attachment]['id'], access_key)
                else:
                    attachment = '{}{}_{}'.format(type_attachment, item[type_attachment]['owner_id'],
                                                  item[type_attachment]['id'])
                attachment_list.append(attachment)

        values.update({'attachment': ''.join(attachment_list)})

    vk_session = vk_api.VkApi(
        token=token)
    vk_session.method(method='messages.send', values=values)
