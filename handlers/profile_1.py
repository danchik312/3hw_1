# from aiogram import types
# from handlers import dp
# from keyboards.show_profile import show_profile_keyboard
# from database.database import execute_select_query
#
# @dp.message_handler(commands=("profile"))
# async def show_profile_command(message: types.Message):
#     keyboard = await show_profile_keyboard()
#     await message.answer("Хотите взглянуть на свой профиль?", reply_markup=keyboard)
#
# @dp.callback_query_handler(text="show_profile")
# async def show_profile(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     profile = execute_select_query("SELECT * FROM profiles WHERE TELEGRAM_ID=?", (user_id,))
#
#     if profile:
#         profile_text = f"Ваш профиль:\nНикнейм: {profile['NICKNAME']}\nБиография: {profile['BIO']}"
#     else:
#         profile_text = "Профиль не найден."
#
#     await callback_query.message.answer(profile_text)
