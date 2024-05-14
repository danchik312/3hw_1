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
    referral_list_button = InlineKeyboardButton(
        text="Referral List🤗",
        callback_data="referral_list"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [link_button],
            [balance_button],
            [referral_list_button],
        ]
    )
    return markup