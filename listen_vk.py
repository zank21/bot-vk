import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import handler_event
from settings import token, group_id

vk_session = vk_api.VkApi(
    token=token)
vk = vk_session.get_api()

longpoll = VkBotLongPoll(vk_session, group_id)


def listen():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            handler_event.process(event)


if __name__ == '__main__':
    listen()
