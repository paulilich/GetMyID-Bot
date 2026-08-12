from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonRequestUsers,
    KeyboardButtonRequestChat,
    ReplyKeyboardRemove,
)

from utils.translation import translate


def keyboard_main(user_id):
    """Главная клавиатура (aiogram 3.x)."""
    my_id = KeyboardButton(text=translate(user_id, "btn_myID_"))

    btn_user_id = KeyboardButton(
        text=translate(user_id, "btn_userID_"),
        request_users=KeyboardButtonRequestUsers(
            request_id=1,
            user_is_bot=False,
            max_quantity=1,
        ),
    )

    btn_channel_id = KeyboardButton(
        text=translate(user_id, "btn_channelID_"),
        request_chat=KeyboardButtonRequestChat(
            request_id=2,
            chat_is_channel=True,
        ),
    )

    btn_group_id = KeyboardButton(
        text=translate(user_id, "btn_groupID_"),
        request_chat=KeyboardButtonRequestChat(
            request_id=3,
            chat_is_channel=False,
        ),
    )

    btn_change_language = KeyboardButton(text=translate(user_id, "change_language_"))
    btn_about_this_bot = KeyboardButton(text=translate(user_id, "btn_about_thisBot_"))

    return ReplyKeyboardMarkup(
        keyboard=[
            [my_id, btn_user_id],
            [btn_channel_id, btn_group_id],
            [btn_change_language, btn_about_this_bot],
        ],
        resize_keyboard=True,
    )


def keyboard_choice_language():
    btn_en = KeyboardButton(text="🇺🇸 English")
    btn_sp = KeyboardButton(text="🇪🇸 España")
    btn_kz = KeyboardButton(text="🇰🇿 Қазақ")
    btn_ru = KeyboardButton(text="🇷🇺 Русский")

    return ReplyKeyboardMarkup(
        keyboard=[
            [btn_en, btn_sp],
            [btn_kz, btn_ru],
        ],
        resize_keyboard=True,
    )


def remove_keyboard():
    return ReplyKeyboardRemove()
