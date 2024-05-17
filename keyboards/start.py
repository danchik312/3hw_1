from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def start_menu_keyboard():
    registration_button = InlineKeyboardButton(
        text="Registration 🤑🔥",
        callback_data="registration"
    )
    my_profile_button = InlineKeyboardButton(
        text="My Profile 😎",
        callback_data="my_profile"
    )
    profiles_button = InlineKeyboardButton(
        text="View Profiles 🧲",
        callback_data="view_profiles"
    )
    reference_button = InlineKeyboardButton(
        text="Reference Menu 💵",
        callback_data="reference_menu"
    )
    like_history_button = InlineKeyboardButton(
        text="Liked Profiles 😍",
        callback_data="history"
    )
    wallet_number_button = InlineKeyboardButton(
        text="Ur Wallet Number💳",
        callback_data="wallet_number"
    )
    send_money_button = InlineKeyboardButton(
        text="Send money🦅",
        callback_data="send_money"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [registration_button],
            [my_profile_button],
            [profiles_button],
            [reference_button],
            [like_history_button],
            [wallet_number_button],
            [send_money_button],
        ]
    )
    return markup