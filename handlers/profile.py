import random
import re
import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from config import bot, ADMIN_ID, MEDIA_PATH
from const import PROFILE_TEXT
from database import sql_queries
from database.a_db import AsyncDatabase
from keyboards.like_dislike import like_dislike_keyboard
from keyboards.profile import my_profile_keyboard
from keyboards.start import start_menu_keyboard
from config import dp



router = Router()


@router.callback_query(lambda call: call.data == "my_profile")
async def random_profiles_call(call: types.CallbackQuery,
                               db=AsyncDatabase()):
    profile = await db.execute_query(
        query=sql_queries.SELECT_PROFILE_QUERY,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    print(profile)
    if profile:
        photo = types.FSInputFile(profile["PHOTO"])
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=PROFILE_TEXT.format(
                nickname=profile['NICKNAME'],
                bio=profile['BIO'],
            ),
            reply_markup=await my_profile_keyboard()
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="U have not registered ‼️"
        )


async def delete_profile(user_id):

    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM profiles WHERE TELEGRAM_ID = ?", (user_id,))
    connection.commit()
    print(f"Profile of user {user_id} has been deleted.")


@router.callback_query(lambda call: call.data == 'delete_profile')
async def process_delete_profile(callback_query: types.CallbackQuery):
    await delete_profile(callback_query.from_user.id)
    await callback_query.answer("Профиль удален", show_alert=True)


