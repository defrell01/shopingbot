import config
import json
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class ClientState(StatesGroup):
    NONE = State()
    START_ORDER = State()
    BOOK_SEARCH = State()
    BOOK_INFO = State()
    OTHER_BOOK_INFO = State()
    PROCESS_CART = State()
    PROCCESS_ORDER = State()

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start_process(message: types.Message, state: FSMContext) -> None:
    msg = 'Привет! Для поиска интересующей тебя книги используй команду /search'
    cart = []
    search_btn = KeyboardButton('/search')

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(search_btn)

    await message.answer(msg, reply_markup=markup)
    await state.set_state(ClientState.START_ORDER)
    await state.update_data(cart)

@dp.message_handler(state=ClientState.START_ORDER, commands=['search'])
async def start_search(message: types.Message, state: FSMContext):
    msg = 'Введите название книги или имя автора.'
    await message.answer(msg)
    await state.set_state(ClientState.BOOK_SEARCH)

@dp.message_handler(state=ClientState.BOOK_SEARCH)
async def find_book(message: types.Message, state: FSMContext):
    user_msg = message.text

    f = open('mock.json', encoding='utf-8')

    data = json.load(f)

    if user_msg == data['title']:
        
        vars = data['variants']

        msg = f'Найдено {vars} вариантов книги, используйте кнопки, чтобы посмотреть подробнее'

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        
        for i in range(len(vars)):
            
            book_btn = KeyboardButton(f'Книга {i+1} 📖')
            markup.row(book_btn)

        await message.answer('Используйте кнопки, чтобы изучить варианты', reply_markup=markup)
        await state.set_state(ClientState.BOOK_INFO)


    else:

        msg = f'Книга не найдена'

        continue_btn = KeyboardButton('Продолжить поиск 🔎') 
        
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(continue_btn)

        await message.answer(msg, reply_markup=markup)

@dp.message_handler(state=ClientState.BOOK_INFO)
async def book_info(message: types.Message, state: FSMContext):
    
    user_msg = message.text
    
    # if (user_msg == '/start') or (user_msg == 'назад':
    #     await state.reset_state(with_data=False)

    # elif user_msg == 'Добавить в корзину 🛒' :
    #     await state.set_state(ClientState.PROCESS_CART)
    
    # else:

    book_number = user_msg.split(' ')[1]

    f = open('mock.json', encoding='utf-8')
    data = json.load(f)
    vars = data['variants']

    continue_btn = KeyboardButton('Посмотреть другие 🔎') 
    cart_btn = KeyboardButton('Добавить в корзину 🛒')
    back_btn = KeyboardButton('Назад')

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(continue_btn, cart_btn, back_btn)


    await state.update_data(current=book_number)
    await message.answer(f'Книга {data["title"]}, вариант {book_number}, {vars[int(book_number)-1]["price"]} руб.', reply_markup=markup)
    await state.set_state(ClientState.OTHER_BOOK_INFO)
    
# @dp.message_handler(state=ClientState.OTHER_BOOK_INFO)
# async def others_info(message: types.Message, state: FSMContext):
#     f = open('mock.json', encoding='utf-8')
#     data = json.load(f)
#     vars = data['variants']

#     msg = f'Найдено {vars} вариантов книги, используйте кнопки, чтобы посмотреть подробнее'

#     markup = ReplyKeyboardMarkup(resize_keyboard=True)
        
#     for i in range(len(vars)):
            
#         book_btn = KeyboardButton(f'Книга {i+1} 📖')
#         markup.row(book_btn)

#     await message.answer('Используйте кнопки, чтобы изучить варианты', reply_markup=markup)
#     await state.set_state(ClientState.BOOK_INFO)

@dp.message_handler(state=ClientState.OTHER_BOOK_INFO)
@dp.message_handler(lambda message: message.text and 'корзину' in message.text.lower())
async def add_to_cart(message: types.Message, state: FSMContext):
    await state.get_data(current)
    await message.answer('test')
    




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)