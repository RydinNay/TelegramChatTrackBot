from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def report_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Получить отчет", callback_data="get_report")]
    ])
    return kb
