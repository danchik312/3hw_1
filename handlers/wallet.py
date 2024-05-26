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
from keyboards.like_dislike import like_dislike_keyboard, history_keyboard
from keyboards.profile import my_profile_keyboard
from keyboards.start import start_menu_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot

router = Router()
class SendMoneyStates(StatesGroup):
    waiting_for_recipient = State()
    waiting_for_amount = State()

@router.callback_query(lambda call: call.data == "wallet_number")
async def show_wallet_number(call: types.CallbackQuery,
                             state: FSMContext,
                             db=AsyncDatabase()):
    user = await db.execute_query(
        query="SELECT ID FROM telegram_users WHERE TELEGRAM_ID = ?",
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    if user:
        user_id = user['ID']
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'Ваш номер кошелька: {user_id}'
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Пользователь не найден.'
        )

    await call.answer()


@router.callback_query(lambda call: call.data == "send_money")
async def handle_send_money(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(SendMoneyStates.waiting_for_amount)
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Введите номер кошелька получателя:'
    )
    await callback_query.answer()

@router.message(SendMoneyStates.waiting_for_recipient)
async def process_recipient(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['recipient'] = message.text
    await SendMoneyStates.waiting_for_amount.set()
    await bot.send_message(
        chat_id=message.chat.id,
        text='Введите сумму для отправки:'
    )


@router.callback_query(lambda call: call.data == "send_money")
async def start_send_money(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите номер кошелька получателя:")
    await SendMoneyStates.waiting_for_recipient.set()


@router.message(SendMoneyStates.waiting_for_recipient)
async def handle_send_money_recipient(message: types.Message, state: FSMContext):
    recipient_wallet = message.text.strip()

    recipient = await db.execute_query(
        query="SELECT TELEGRAM_ID FROM telegram_users WHERE ID = ?",
        params=(recipient_wallet,),
        fetch='one'
    )

    if recipient:
        await state.update_data(recipient_id=recipient['TELEGRAM_ID'])
        await message.answer("Введите сумму для отправки:")
        await SendMoneyStates.waiting_for_amount.set()
    else:
        await message.answer("Пользователь с таким номером кошелька не найден.")


@router.message(SendMoneyStates.waiting_for_amount)
async def handle_send_money_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if 'recipient_id' not in data:
        await message.answer("ой что то не так")
        return

    try:
        amount = int(message.text)
        if amount <= 0:
            await message.answer("Пожалуйста, введите сумму больше нуля.")
            return

        recipient_id = data['recipient_id']
        await perform_send_money(message.from_user.id, recipient_id, amount, db)

        await message.answer("Деньги успешно отправлены!")
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите числовую сумму.")


async def perform_send_money(sender_id, recipient_id, amount, db):
    await db.execute_query(
        query="UPDATE telegram_users SET BALANCE = BALANCE - ? WHERE TELEGRAM_ID = ?",
        params=(amount, sender_id),
        fetch='none'
    )

    await db.execute_query(
        query="UPDATE telegram_users SET BALANCE = BALANCE + ? WHERE TELEGRAM_ID = ?",
        params=(amount, recipient_id),
        fetch='none'
    )