from vk_api.keyboard import VkKeyboard, VkKeyboardButton, VkKeyboardColor


def menu():
    keyboard = VkKeyboard()
    keyboard.add_button(label='тест', color=VkKeyboardColor.POSITIVE, payload='101')
    return keyboard.get_keyboard()
