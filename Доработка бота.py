from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button1 = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Купить')
kb.insert(button)
kb.insert(button1)
kb.insert(button2)

inline_kb = InlineKeyboardMarkup(resize_keyboard=True)
inline_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button1 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.add(inline_button)
inline_kb.add(inline_button1)


kb_buy = InlineKeyboardMarkup(resize_keyboard=True)
but_b = InlineKeyboardButton(text='Дренирующий напиток FITODRAIN цитрус мята Драйн Drain',
                                  callback_data="product_buying")
but_b2 = InlineKeyboardButton(text='Коллаген животный пептидный порошок с витамином С',
                                   callback_data="product_buying")
but_b3 = InlineKeyboardButton(text='Магний Б6 Mg B6', callback_data="product_buying")
but_b4 = InlineKeyboardButton(text='Омега 3', callback_data="product_buying")
kb_buy.insert(but_b)
kb_buy.insert(but_b2)
kb_buy.insert(but_b3)
kb_buy.insert(but_b4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Формула Миффлина-Сан Жеора – это одна из самых последних формул расчета калорий для '
                         'оптимального похудения или сохранения нормального веса. Она была выведена в 2005 году '
                         'и стала заменять классическую формулу Харриса-Бенедикта.')


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    with open("Фитодрайн.png", "rb") as img:
        await message.answer_photo(img,
                                   "Название: Фитодрайн | Описание: Дренирующий напиток FITODRAIN цитрус мята Драйн Drain | Цена: 1 035 ₽.")
    with open("Коллаген.png", "rb") as img:
        await message.answer_photo(img, "Название: Коллаген |"
                                        " Описание: Коллаген животный пептидный порошок с витамином С | Цена: 784 ₽.")
    with open("Магний Б-6.png", "rb") as img:
        await message.answer_photo(img, "Название: Магний Б6 Mg B6 |"
                                        " Описание:  антидепрессант; для сердца; улучшение работы головного мозга | Цена: 362 ₽.")
    with open("Омега 3.png", "rb") as img:
        await message.answer_photo(img, "Название: Омега 3 |"
                                        " Описание:  для сердца; сосуды; для спортсменов | Цена: 541 ₽.")


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result_prog = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'Ваша норма калорий {result_prog} день')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)