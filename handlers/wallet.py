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

router = Router()
class SendMoneyStates(StatesGroup):
    waiting_for_recipient = State()
    waiting_for_amount = State()

@router.callback_query(lambda call: call.data == "wallet_number")
async def handle_wallet_number(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=f'Ваш номер кошелька: {user_id}'
    )
    await callback_query.answer()

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

@router.message(SendMoneyStates.waiting_for_amount)
async def process_amount(message: types.Message, state: FSMContext, db: AsyncDatabase):
    amount = float(message.text)
    sender_id = message.from_user.id
    data = await state.get_data()
    recipient_id = int(data['recipient'])

    balance = await db.get_user_balance(sender_id)
    if amount <= 0 or amount > balance:
        await bot.send_message(
            chat_id=message.chat.id,
            text='Неверная сумма или недостаточно средств на счете.'
        )
    else:
        await db.create_transaction(sender_id, recipient_id, amount)
        await db.update_balances(sender_id, recipient_id, amount)
        await bot.send_message(
            chat_id=message.chat.id,
            text='Транзакция выполнена успешно.'
        )
    await state.finish()