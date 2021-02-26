from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext

from loader_model import dp
from aiogram import types

# from states import Test
#
#
# @dp.message_handler(Command("test"))
# async def enter_test(message: types.Message):
#     await message.answer("Test has begun. \nQuestion 1:")
#     await Test.Q1.set()
#
#
# @dp.message_handler(state=Test.Q1)
# async def answer_q1(message: types.Message, state: FSMContext):
#     answer = message.text
#     await state.update_data(answer1=answer)
#     await message.answer("Question 2:")
#     await Test.next()  # .previous()
#
#
# @dp.message_handler(state=Test.Q2)
# async def answer_q1(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     answer1 = data.get("answer1")
#     answer2 = message.text
#
#     await message.answer("Thanks.")
#     await message.answer(f"Results: {answer1, answer2}")

# we can go state.reset_data() - удаляем данные
