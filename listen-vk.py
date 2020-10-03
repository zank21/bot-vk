import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import command_enum
from vk_functions import get_random_id

vk_session = vk_api.VkApi(
    token='c1fa29197260f82e5c97fb4c597aee8091c6c1e36dabaf2c58b38298d780a18d63dc69bd734d2b50f17e4')
vk = vk_session.get_api()

longpoll = VkBotLongPoll(vk_session, '192848017')


def proccess_query(event):
    for command in command_enum.COMAND_ENUM:
        if event.obj.text == command:
            response = command_enum.COMAND_ENUM[command]
            vk_session.method('messages.send', values={
                'user_id': event.obj['from_id'],
                'message': response,
                'random_id': get_random_id()
            })


def listen():
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            proccess_query(event)


if __name__ == '__main__':
    listen()
