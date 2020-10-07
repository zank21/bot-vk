import vk_api
from settings import token
from vk_functions import get_random_number
import keybord_pattern

vk_session = vk_api.VkApi(
    token=token)
vk_session.method(method='messages.send', values={
    'user_id': '395807460',
    'message': '11',
    'random_id': get_random_number(),
    # 'keyboard': keybord_pattern.menu(),
    'payload' : '2'
})
