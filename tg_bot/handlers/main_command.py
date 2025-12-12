from aiogram import types
from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import CHANNEL, INVITE_LINK
from database.db_services import UserService
from locales.texts import TEXTS
from tg_bot.keyboards.admin_keyboard import report_keyboard

main_command_router = Router()

@main_command_router.message(CommandStart())
async def start_handler(message: types.Message, command: CommandStart):
    start_param = command.args
    '''language = message.from_user.language_code
    if language not in TEXTS:
        language = "en"
    '''
    language = 'ru'
    texts = TEXTS[language]

    admins = await message.bot.get_chat_administrators(chat_id=f"{CHANNEL}")
    admin_ids = [adm.user.id for adm in admins]
    if message.from_user.id in admin_ids:
        await message.answer("Нажмите кнопку, чтобы получить отчет:", reply_markup=report_keyboard())
        return

    if not start_param:
        start_param='native_user'

        '''await message.answer(
            f"{texts['start_with_param']} {start_param}\n"
            f"{texts['subscribe_text']}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=texts['subscribe_button'], url=f"{INVITE_LINK}")]
                ]
            )
        )'''

    # else:
        # start_param='native_user'
    await message.answer(
        f"{texts['start_no_param']}\n"
        f"{texts['subscribe_text'].format(link=INVITE_LINK)}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=texts['subscribe_button'], url=f"{INVITE_LINK}")]
            ]
        )
    )

    user = await UserService.create_user(
        tg_id=message.from_user.id,
        name=message.from_user.full_name,
        source=start_param
    )


