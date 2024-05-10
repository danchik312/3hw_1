from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

async def show_profile_keyboard():
    profile_button = InlineKeyboardButton(
        text="Show profile😎",
        callback_data="Show_profile"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [profile_button],
        ]
    )
    return markup