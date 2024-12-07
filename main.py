import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils import executor

API_TOKEN = 'YOUR_BOT_TOKEN'

# Создаем бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Начальный язык — русский
current_language = 'ru'


# Функция для получения цитаты с Forismatic API
def get_quote(language):
    url = "http://api.forismatic.com/api/1.0/"
    params = {
        "method": "getQuote",  # Метод для получения цитаты
        "format": "json",  # Формат ответа JSON
        "lang": language,  # Язык ответа (ru/en)
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        quote_data = response.json()
        return quote_data.get("quoteText", "Цитата не найдена."), quote_data.get("quoteAuthor", "Неизвестный автор")
    else:
        return "Ошибка при запросе цитаты.", ""


# Функция для создания inline клавиатуры
def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)

    # Кнопки: Новая цитата и Переключить язык
    button_new_quote = InlineKeyboardButton(text="Новая цитата", callback_data="new_quote")
    button_switch_language = InlineKeyboardButton(text="Переключить язык", callback_data="switch_language")

    keyboard.add(button_new_quote, button_switch_language)

    return keyboard


# Хэндлер для команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Отправляем приветственное сообщение с кнопками
    quote_text, author = get_quote(current_language)
    await message.answer(f"<b>Цитата:</b> {quote_text}\n<b>Автор:</b> {author}", parse_mode=ParseMode.HTML,
                         reply_markup=get_inline_keyboard())


# Хэндлер для кнопок
@dp.callback_query_handler(lambda c: c.data == 'new_quote' or c.data == 'switch_language')
async def handle_button_click(callback_query: types.CallbackQuery):
    global current_language

    if callback_query.data == 'new_quote':
        # Получаем новую цитату
        quote_text, author = get_quote(current_language)
        await bot.send_message(callback_query.from_user.id, f"<b>Цитата:</b> {quote_text}\n<b>Автор:</b> {author}",
                               parse_mode=ParseMode.HTML)

    elif callback_query.data == 'switch_language':
        # Переключаем язык
        current_language = 'en' if current_language == 'ru' else 'ru'
        language = 'Русский' if current_language == 'ru' else 'English'
        await bot.send_message(callback_query.from_user.id, f"Язык переключен на {language}.",
                               reply_markup=get_inline_keyboard())

    # Удаляем кнопку, чтобы избежать повторных нажатий на одну и ту же
    await callback_query.answer()


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
