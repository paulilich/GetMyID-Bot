from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from db.db import Users
from logs.record_log import log_error
from utils.translation import translate
from bot_tools.keyboard import keyboard_main, keyboard_choice_language

db = Users()
router = Router()

db.init_db()

# All possible button labels (all languages) so handlers work after language change
MY_ID_BUTTONS = {"🆔 My ID", "🆔 Mi ID", "🆔 Менің ID", "🆔 Мой ID"}
ABOUT_BUTTONS = {"ℹ️ About this bot", "ℹ️ Sobre este bot", "ℹ️ Бот туралы", "ℹ️ О боте"}

CHANGE_LANG_BUTTONS = {
    "🌐 Change language",
    "🌐 Cambiar idioma",
    "🌐 Тілді өзгерту",
    "🌐 Сменить язык",
}


LANG_CHOICES = {
    "🇺🇸 English": "en-US",
    "🇪🇸 España": "es-ES",
    "🇷🇺 Русский": "ru-RU",
    "🇰🇿 Қазақ": "kk-KZ",
}


@router.message(CommandStart())
async def main(message: Message):
    user_id = message.from_user.id
    name = message.from_user.first_name or "friend"

    db.add_user(user_id)

    if db.get_language(user_id) is None:
        await message.answer(
            f"👋 Hi, <b>{name}</b>! I’m a bot that shows IDs of users, chats, channels and groups.\n\n"
            f"Choose the bot interface language 👇",
            reply_markup=keyboard_choice_language(),
            parse_mode="HTML",
        )
    else:
        answer = translate(user_id, "welcome_msg_")
        answer = answer.replace("name", name).replace("user_id", str(user_id))
        await message.answer(
            answer,
            reply_markup=keyboard_main(user_id),
            parse_mode="HTML",
        )


@router.message(F.text.in_(ABOUT_BUTTONS))
async def about_handler(message: Message):
    user_id = message.from_user.id
    answer = translate(user_id, "about_thisBot_")
    await message.answer(
        text=answer,
        disable_web_page_preview=True,
    )


@router.message(F.text.in_(MY_ID_BUTTONS))
async def my_id_handler(message: Message):
    user_id = message.from_user.id
    answer = translate(user_id, "your_id_")
    await message.answer(
        f"{answer}`{user_id}`",
        parse_mode="Markdown",
    )


@router.message(F.text.in_(CHANGE_LANG_BUTTONS))
async def change_language_handler(message: Message):
    await message.answer(
        "Choice your language 👇",
        reply_markup=keyboard_choice_language(),
    )


@router.message(F.users_shared)
async def user_id_handler(message: Message):
    # language of the person who pressed the button
    requester_id = message.from_user.id
    shared_user_id = message.users_shared.users[0].user_id

    answer = translate(requester_id, "user_id_")
    await message.answer(
        f"{answer}`{shared_user_id}`",
        parse_mode="Markdown",
    )


@router.message(F.chat_shared)
async def chat_id_handler(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat_shared.chat_id

    answer = translate(user_id, "chat_id_")
    await message.answer(
        f"{answer}`{chat_id}`",
        parse_mode="Markdown",
    )


@router.message(F.sticker)
async def handle_sticker(message: Message):
    user_id = message.from_user.id
    sticker_id = message.sticker.file_id

    db.add_user(user_id)

    try:
        await message.answer(
            text=(
                f"😊 *Thanks for the sticker!* 😊\n\n"
                f"🆔 *Your unique ID:* `{user_id}`\n\n"
                f"📌 *Sticker ID:* `{sticker_id}`\n\n"
                f"🤖 *I don’t know how to react to it yet, but I’ll learn soon!*"
            ),
            parse_mode="Markdown",
        )
    except Exception as e:
        log_error(f"Ошибка при отправке сообщения юзеру: {user_id}\n{e}")


@router.message(F.text)
async def text_input(message: Message):
    user_id = message.from_user.id
    text = message.text

    if text in LANG_CHOICES:
        lang = LANG_CHOICES[text]
        db.set_language(user_id, lang)

        confirm = translate(user_id, "language_set_")
        await message.answer(
            confirm,
            reply_markup=keyboard_main(user_id),
        )
        return

    answer = translate(user_id, "unknown_text_")
    await message.answer(
        answer,
        reply_markup=keyboard_main(user_id) if db.get_language(user_id) else keyboard_choice_language(),
    )
