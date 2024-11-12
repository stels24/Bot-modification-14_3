from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio



api = "7063587812:AAFWVFYy-SsfAHsJNCg9Edqnn1C0IvB2uhQ"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


KeyBoard = ReplyKeyboardMarkup(resize_keyboard=True)
KBbutt_1 = KeyboardButton(text='Информация')
KBbutt_2 = KeyboardButton(text='Рассчитать')
KBbutt_3 = KeyboardButton(text="Купить")
KeyBoard.add(KBbutt_1)
KeyBoard.add(KBbutt_2)
KeyBoard.add(KBbutt_3)


INKboard_1 = InlineKeyboardMarkup()
INKbutt_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
INKbutt_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
INKboard_1.add(INKbutt_1)
INKboard_1.add(INKbutt_2)


INKboard_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product4", callback_data="product_buying")]
    ])
# kb.insert kb.row


product = [1, 2, 3, 4]


@dp.message_handler(text='Рассчитать')
async def main_menu(mess):
    await mess.answer(text='Выберите опцию:', reply_markup=INKboard_1)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(text='10 х вес(кг) + 6,25 x рост(см) – 5 х возраст(г) + 5')
    await call.answer()


@dp.message_handler(text='Информация')
async def info(mess):
    await mess.answer('Формула Миффлина-Сан Жеора – это одна из самых последних формул расчета калорий для '
                         'оптимального похудения или сохранения нормального веса.')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(mess, state):
    await state.update_data(age=mess.text)
    await mess.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(mess, state):
    await state.update_data(growth=mess.text)
    await mess.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(mess, state):
    await state.update_data(weight=mess.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await mess.answer(f'Ваши калории {calories}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def consol_command(messe):
    await messe.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=KeyBoard)


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for num in product:
        with open(f"Коллаген.png", 'rb') as img:
            await message.answer_photo(img, f"Название:Product{num} | Описание: {num} | Цена {num * 100}")
    await message.answer("Выберите продукт для покупки:", reply_markup=INKboard_2)



@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно преобрели продукт!")
    await call.answer()


@dp.message_handler()
async def other_message(mess):
    await mess.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
