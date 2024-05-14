from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def reference_menu_keyboard():
    link_button = InlineKeyboardButton(
        text="Link 🔗",
        callback_data=f"reference_link"
    )
    balance_button = InlineKeyboardButton(
        text="Balance 🤑",
        callback_data="reference_balance"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [link_button],
            [balance_button],
        ]
    )
    return markup