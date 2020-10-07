from vk_api.bot_longpoll import VkBotEventType
import vk_api


def main(event: vk_api.bot_longpoll.VkBotMessageEvent, payload):
    print(payload)
    print('good')
