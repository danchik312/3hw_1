import sqlite3
import random
from aiogram import Router, types
from aiogram.filters import Command

from config import bot, ADMIN_ID, MEDIA_PATH
from const import START_MENU_TEXT
from database import sql_queries
from database.a_db import AsyncDatabase
from keyboards.start import start_menu_keyboard
from aiogram.utils.deep_linking import create_start_link
# from scraper.news_scraper import NewsScraper


router = Router()


@router.message(Command("start"))
async def start_menu(message: types.Message,
                     db=AsyncDatabase()):
    print(message)
    command = message.text
    token = command.split()
    print(token)
    if len(token) > 1:
        await process_reference_link(token[1],
                                     message)

    await db.execute_query(
        query=sql_queries.INSERT_USER_QUERY,
        params=(
            None,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            None,
            0
        ),
        fetch='none'
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello {message.from_user.first_name}"
    )

    animation_file = types.FSInputFile(MEDIA_PATH + "bot-ani.gif")
    await bot.send_animation(
        chat_id=message.chat.id,
        animation=animation_file,
        caption=START_MENU_TEXT.format(
            user=message.from_user.first_name
        ),
        reply_markup=await start_menu_keyboard()
    )
async def process_reference_link(token, message, db=AsyncDatabase()):
    link = await create_start_link(bot=bot, payload=token)
    owner = await db.execute_query(
        query=sql_queries.SELECT_USER_BY_LINK_QUERY,
        params=(
            link,
        ),
        fetch='one'
    )

    if owner['TELEGRAM_ID'] == message.from_user.id:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="U can not use ur own link"
        )
        return
    try:
        await db.execute_query(
            query=sql_queries.INSERT_REFERENCE_USER_QUERY,
            params=(
                None,
                owner['TELEGRAM_ID'],
                message.from_user.id
            ),
            fetch='none'
        )
        await db.execute_query(
            query=sql_queries.UPDATE_USER_BALANCE_QUERY,
            params=(
                owner['TELEGRAM_ID'],
            ),
            fetch='none'
        )
        await bot.send_message(
            chat_id=owner['TELEGRAM_ID'],
            text='U got new reference user\n'
                 'Congrats 🤑🍾'
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='U have used this link ‼️'
        )


@router.message(lambda message: message.text == "SasaiKudasai")
async def admin_start_menu(message: types.Message,
                           db=AsyncDatabase()):
    if int(ADMIN_ID) == message.from_user.id:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Приветствую вас, мой хозяин"
        )
        users_info = await db.execute_query(query=sql_queries.SELECT_USER, fetch='all')
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'Список пользователей:\n{users_info}'
    )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ты не мой хозяин"
        )
# @router.callback_query(lambda call: call.data == "news")
# async def handle_news_button(callback_query: types.CallbackQuery):
#     scraper = NewsScraper()
#     news_data = await scraper.scrape_data()
#     await scraper.save_to_database(news_data)
#     await callback_query.answer()
