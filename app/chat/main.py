from vk_api.bot_longpoll import VkBotEventType
import vk_api
from vk_functions import get_random_number
from settings import token, group_id
import requests
import error_num


def main(event: vk_api.bot_longpoll.VkBotMessageEvent, payload):
    user_id = event.obj['from_id']
    values = {
        'user_id': user_id,
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

            if type_attachment == 'photo':
                if 'access_key' in item[type_attachment]:
                    for size in item[type_attachment]['sizes']:
                        if size['type'] == 'w':
                            file = requests.get(size['url']).content
                            break

                    vk_session = vk_api.VkApi(
                        token=token)
                    upload_server = vk_session.method(method='photos.getMessagesUploadServer', values={
                        'peer_id': user_id
                    })['upload_url']
                    response = requests.post(url=upload_server, files={'photo': file})
                    data = response.json()
                    title = '{}{}_{}'.format('audio_message', event.obj['from_id'],
                                             event.obj['conversation_message_id'])

                    doc = vk_session.method(method='photos.saveMessagesPhoto', values={
                        'photo': data['photo'],
                        'server': data['server'],
                        'hash': data['hash']
                    })
                    type_attachment = doc['type']
                    attachment = '{}{}_{}'.format(type_attachment, doc[type_attachment]['owner_id'],
                                                  doc[type_attachment]['id'])
                    attachment_list.append(attachment)
                    continue
                else:
                    attachment = '{}{}_{}'.format(type_attachment, item[type_attachment]['owner_id'],
                                                  item[type_attachment]['id'])
                    attachment_list.append(attachment)
                    continue
            if type_attachment == 'video' or type_attachment == 'audio':
                if 'access_key' in item[type_attachment]:
                    file = requests.get(item[type_attachment]['url']).content
                    vk_session = vk_api.VkApi(
                        token=token)
                    upload_server = vk_session.method(method='docs.getMessagesUploadServer', values={
                        'type': type_attachment,
                        'peer_id': user_id,
                        'group_id': group_id
                    })['upload_url']
                    response = requests.post(url=upload_server, files={'file': file})
                    data = response.json()
                    data = str(data['file'])
                    title = '{}{}_{}'.format('audio_message', event.obj['from_id'],
                                             event.obj['conversation_message_id'])

                    doc = vk_session.method(method='docs.save', values={
                        'file': data,
                        'title': title
                    })
                    type_attachment = doc['type']
                    attachment = '{}{}_{}'.format(type_attachment, doc[type_attachment]['owner_id'],
                                                  doc[type_attachment]['id'])
                    attachment_list.append(attachment)
                    continue
                else:
                    attachment = '{}{}_{}'.format(type_attachment, item[type_attachment]['owner_id'],
                                                  item[type_attachment]['id'])
                    attachment_list.append(attachment)
                    continue
            if type_attachment == 'doc':
                if item[type_attachment]['title'] == 'audio_msg.opus':
                    file = requests.get(item[type_attachment]['url']).content
                    vk_session = vk_api.VkApi(
                        token=token)
                    upload_server = vk_session.method(method='docs.getMessagesUploadServer', values={
                        'type': 'audio_message',
                        'peer_id': user_id,
                        'group_id': group_id
                    })['upload_url']
                    response = requests.post(url=upload_server, files={'file': file})
                    data = response.json()
                    data = str(data['file'])
                    title = '{}{}_{}'.format('audio_message', event.obj['from_id'],
                                             event.obj['conversation_message_id'])

                    doc = vk_session.method(method='docs.save', values={
                        'file': data,
                        'title': title
                    })
                    type_attachment = doc['type']
                    attachment = '{}{}_{}'.format(type_attachment, doc[type_attachment]['owner_id'],
                                                  doc[type_attachment]['id'])
                else:
                    error_num.error_doc(event, payload)
                    attachment = ''
                attachment_list.append(attachment)
                continue

        values.update({'attachment': ''.join(attachment_list)})

    vk_session = vk_api.VkApi(
        token=token)
    vk_session.method(method='messages.send', values=values)
