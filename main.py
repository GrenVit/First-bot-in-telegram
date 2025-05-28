from aiogram.types import (ContentType, ReplyKeyboardMarkup, KeyboardButton,
                            KeyboardButtonPollType, Message, InlineKeyboardButton,
                            InlineKeyboardMarkup, BotCommand, CallbackQuery, FSInputFile, KeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import CommandStart
from aiogram.filters import Command 
from config_reader import config
from aiogram.fsm.context import FSMContext
import logging
import asyncio
import os

# Включаем логирование и сохраняем логи в файл
logging.basicConfig(
    filename='/Users/user/Проекты/venv_Telegram/FirstTelegramBot/bot.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
storage = MemoryStorage()
dp = Dispatcher()
users = {} 
# Список с ID администраторов бота. !!!Замените на ваш!!!
admin_ids: list[int] = [1234567890, 987654321]

# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/groups', description='Наш телеграмм канал'),
        BotCommand(command='/start', description='Запустить бота')           
    ]
    await bot.set_my_commands(main_menu_commands) 
# Регистрируем асинхронную функцию в диспетчере,
# которая будет выполняться на старте бота,
dp.startup.register(set_main_menu)

#Создаем инлайн-кнопки (кнопки которые под сообщением)
inline_button_1 = InlineKeyboardButton(text='💵 Цены ', callback_data='show_prices')
inline_button_2 = InlineKeyboardButton(text='📍 Наши локации ', callback_data='show_address')
inline_button_3 = InlineKeyboardButton(text='🎾 Расписание ', callback_data='schedule')
inline_button_4 = InlineKeyboardButton(text='📞 Контакты тренеров', callback_data='contact')  #'https://t.me/DeeWithNoDegree'})
inline_button_5 = InlineKeyboardButton(text='❣️ Правила абонемента',callback_data='abonement')
inline_button_6 = InlineKeyboardButton(text='💯 Акции', callback_data='action_button')

keyboard = InlineKeyboardMarkup(inline_keyboard=[[inline_button_6], [inline_button_1], [inline_button_2],
                                                [inline_button_3], [inline_button_4],
                                                [inline_button_5]])

# Необходимые кнопки для работы в боте
back_button = InlineKeyboardButton(text='⬅ Назад', callback_data='back_to_menu')
back_button_1 = InlineKeyboardButton(text='📍 Наличная ул 44к6', callback_data='location_vaska')
back_button_2 = InlineKeyboardButton(text='📍 ВМФ (Средний проспект 87 В.О.)', callback_data='location_dynamit')
Kuznetsova_button = InlineKeyboardButton(text='Кузнецова Елизавета', callback_data='Kuznetsova')
Ivanova_button = InlineKeyboardButton(text='Грега Дарья', callback_data='Ivanova')
Savin_button = InlineKeyboardButton(text='Савин Роман', callback_data='Savin')
back_button_contact = InlineKeyboardButton(text='⬅ Назад', callback_data='back_button_contact')
vaska_button_location = InlineKeyboardButton(text='📍 Наличная', callback_data='vaska_button_location')
dynamit_button_location = InlineKeyboardButton(text='📍 ВМФ', callback_data='dynamit_button_location')
dinamo_button_location = InlineKeyboardButton(text='📍 Динамо', callback_data='dinamo_button_location')
back_button_show_address = InlineKeyboardButton(text='⬅ Назад', callback_data='show_address')
price_button_vaska = InlineKeyboardButton(text='📍 Наличная', callback_data='price_button_vaska')
price_button_dynamit = InlineKeyboardButton(text='📍 ВМФ', callback_data='price_button_dynamit')
price_button_Dinamo = InlineKeyboardButton(text='📍 Динамо', callback_data='price_button_dinamo')
back_button_show_price = InlineKeyboardButton(text='⬅ Назад', callback_data='show_prices')
button_VMF_schedule =  InlineKeyboardButton(text='📍 ВМФ', callback_data='button_VMF_schedule')
button_Dinamo_schedule =  InlineKeyboardButton(text='📍 Динамо', callback_data='button_Dinamo_schedule')
button_Nalichnay_schedule =  InlineKeyboardButton(text='📍 Наличная', callback_data='button_Nalichnay_schedule')
back_button_show_schedule = InlineKeyboardButton(text='⬅ Назад', callback_data='schedule')                                               

# Сохрянем послднее id сообщение
last_message_id = None

# # Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command("start"))
async def process_start_command(message: types.Message):
    global last_message_id
    logging.info(f"Received /start command from {message.from_user.id}")
 # Если есть предыдущее сообщение, удаляем его
    if last_message_id is not None:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)
        except Exception as e:
            logging.error(f"Error deleting message {last_message_id}: {e}") 

# Отправляем новое сообщение и сохраняем его ID
    new_message = await message.answer(text=f'Привет, {message.from_user.first_name}!😊\nЯ - <b>Твити</b>, твой теннисный помощник клуба <b>Game Set Match</b> 🎾\n\n'
        'Тут ты можешь узнать о наших <u>тренировках</u>, <u>ценах</u> и <u>локациях</u> ☺️\n'
        'А если ты не нашел ответ на интересующий тебя вопрос, то ты можешь обратиться к нашим <u>тренерам</u> 💌\n'
        'Нажми интересующее тебе кнопку',
        reply_markup=keyboard, parse_mode='HTML') # Запуск инлайн кнопок
    last_message_id = new_message.message_id

    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'id устройства': message.from_user.id,
            'Имя': message.from_user.first_name,
            'Фамилия': message.from_user.last_name,
            'Логин в телеграмме': message.from_user.username,
            'Текст сообщения':message.text
        }
    logging.info(f"Added new user: {users[message.from_user.id]}")

@dp.message(Command("groups"))
async def process_group_command(message: types.Message):
    logging.info(f"Received /groups command from {message.from_user.id}")
    await message.answer(text='Наш телеграмм канал https://t.me/tennisclub_gsm')
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'id устройства': message.from_user.id,
            'Имя': message.from_user.first_name,
            'Фамилия': message.from_user.last_name,
            'Логин в телеграмме': message.from_user.username,
            'Текст сообщения':message.text
        }
       # logging.info(f"Added new user: {users[message.from_user.id]}")
        logging.info(f"Added new user: {users[message.from_user.id]}" )

@dp.callback_query(F.data == 'action_button')
async def process_action_button(callblack: CallbackQuery):
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])   
    await callblack.message.edit_text(text='<b>АКЦИИ</b>\n\n'
                                            '1. При покупке абонемента другом\n'
                                            '+1 бесплатная тренировка ТЕБЕ\n\n'
                                            '2. Акция «День в день»\n'
                                            'При продлении абонемента в день последней тренировки -\n'
                                            '10% на покупку нового\n\n'
                                            '3. Абонемент «СЕМЕЙНЫЙ»\n'
                                            'для каждого следующего члена семьи -10% на покупку\n'
                                            'НОВОГО АБОНЕМЕНТА\n\n'
                                            '4. «Праздничный Happy Birthday»\n'
                                            'за 3 дня до и 3 после вашего дня рождения - скидка 10%\n'
                                            'на новый абонемент\n', reply_markup=back_keyboard, parse_mode='HTML')
    await callblack.answer() #Убирает часики с кнопки

@dp.callback_query(F.data == 'show_prices')
async def process_show_price_one_press(callblack: CallbackQuery):
    # Создаем клавиатуру только с кнопкой "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[price_button_dynamit],[price_button_Dinamo],[price_button_vaska],[back_button]]) 
# Редактируем сообщение, заменяя старую клавиатуру на новую
    await callblack.message.edit_text(text='Выбери нужный адрес для получения подробной информации по <u>ценам</u>\n'
    '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard, parse_mode='HTML')
    await callblack.answer() #Убирает часики с кнопки

@dp.callback_query(F.data == 'price_button_vaska')
async def process_show_price_vaska(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)#Убирает часики с кнопки
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_show_price]])
    await callback_query.message.edit_text(text='Вы выбрали <b>Наличная</b>\n\nЦены на\n'
                                            'ГРУППОВЫЕ ТРЕНИРОВКИ\n'
                                            'НА НАЛИЧНОЙ 44\n\n'
                                            'РАЗОВОЕ ПОСЕЩЕНИЕ\n'
                                            '1,5 часа\n'
                                            '2600р\n\n'
                                            '4 раза в месяц\n'
                                            '(Тренировки 1 раз в неделю)\n'
                                            '1,5 часа\n'
                                            '9500р\n\n'
                                            '8 раз в месяц\n'
                                            '(Тренировки 2 раза в неделю)\n'
                                            '1,5 часа\n'
                                            '17000р\n'
                                            '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard, parse_mode='HTML')
    await callback_query.answer() #Убирает часики с кнопки

@dp.callback_query(F.data == 'price_button_dynamit')
async def process_show_price_dynamit(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)#Убирает часики с кнопки
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_show_price]])   
    await callback_query.message.edit_text(text='Вы выбрали <b>ВМФ</b>\n\nЦены на \n'
                                            'ГРУППОВЫЕ ТРЕНИРОВКИ\n'
                                            'На ВМФ (Средний проспект 87 В.О.)\n\n'
                                            'РАЗОВОЕ ПОСЕЩЕНИЕ\n'
                                            '1,5 Часа\n'
                                            '2600р\n\n'
                                            '4 раза в месяц\n'
                                            '(Тренировки 1 раз в неделю)\n'
                                            '1,5 Часа\n'
                                            '9500р\n\n'
                                            '8 раз в месяц\n'
                                            '(Тренировки 2 раза в неделю)\n'
                                            '1,5 Часа\n'
                                            '17000р\n'
                                            '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard, parse_mode='HTML')
    await callback_query.answer() #Убирает часики с кнопки

@dp.callback_query(F.data == 'price_button_dinamo')
async def process_show_price_dynamit(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)#Убирает часики с кнопки
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_show_price]])   
    await callback_query.message.edit_text(text='Вы выбрали <b>Динамо</b>\n\nЦены на\n'
                                            'ГРУППОВЫЕ ТРЕНИРОВКИ\n'
                                            'На Динамо \n\n'
                                            'РАЗОВОЕ ПОСЕЩЕНИЕ\n'
                                            '1,0 час (Утро)\n'
                                            '2300р с человека\n\n'
                                            '1.0 час (День)\n'
                                            '2500р с человека\n\n'
                                            '1,5 часа (Утро)\n'
                                            '3200р с человека\n\n'
                                            '1.5 часа (День)\n'
                                            '3500р с человека\n'
                                            '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard, parse_mode='HTML')
    await callback_query.answer() #Убирает часики с кнопки

# Возврат в главное меню
@dp.callback_query(F.data == 'back_to_menu')
async def process_back_to_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id) #Убирает часики с кнопки
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=f'Привет, {callback_query.from_user.first_name}!😊\nЯ - <b>Твити</b>, твой теннисный помощник клуба <b>Game Set Match</b> 🎾\n\n'
        'Тут ты можешь узнать о наших <u>тренировках</u>, <u>ценах</u> и <u>локациях</u> ☺️\n'
        'А если ты не нашел ответ на интересующий тебя вопрос, то ты можешь обратиться к нашим <u>тренерам</u> 💌\n'
        'Нажми интересующее тебе кнопку',
                                reply_markup=keyboard,
                                parse_mode='HTML')


# Здесь заполняется информация по кнопке Локации
@dp.callback_query(F.data == 'schedule')
async def process_schedule_press(callblack: CallbackQuery):
    # Создаем клавиатуру только с кнопкой "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_VMF_schedule],[button_Dinamo_schedule],[button_Nalichnay_schedule],[back_button]])  
    await callblack.message.edit_text(text='Выбери нужный <u>адрес</u> для детальной информации.\n'
    '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard, parse_mode='HTML')
    await callblack.answer() #Убирает часики с кнопки

@dp.callback_query(F.data == 'button_VMF_schedule')
async def process_show_price_vaska(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)#Убирает часики с кнопки
   
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_show_schedule]])
    
    await callback_query.message.edit_text(text='Вы выбрали <b>ВМФ</b>\n\n'
                        "<u>ПОНЕДЕЛЬНИК</u> (Продолжающие, NTRP 2.0-3.5)\n"
                        "20:00-21:30\n\n"
                        "<u>ПОНЕДЕЛЬНИК</u> (Средние, NTRP 3.5-4.5)\n"
                        "20:00-21:30\n\n"
                        "<u>ВТОРНИК</u> (Продолжающие, NTRP 2.0-3.5)\n"
                        "20:00-21:30\n\n"
                        "<u>СРЕДА</u> (Средние, NTRP 3.5-4.5)\n"
                        "20:00-21:30\n\n"
                        "<u>ЧЕТВЕРГ</u> (Продолжающие, NTRP 2.0-3.5)\n"
                        "20:00-21:30\n\n"
                        "<u>ПЯТНИЦА</u> (Начинающие, NTRP 0-2.5)\n"
                        "20:00-21:30\n\n"
                        '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard, parse_mode='HTML')
    await callback_query.answer() #Убирает часики с кнопки

@dp.callback_query(F.data == 'button_Dinamo_schedule')
async def process_show_price_vaska(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)#Убирает часики с кнопки
   
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_show_schedule]])
    
    await callback_query.message.edit_text(text='Вы выбрали <b>Динамо</b>\n\n'
                        "<u>ПОНЕДЕЛЬНИК</u> (Средние, NTRP 3.5-4.5)\n"
                        "08:00-09:00 Утро (Грунт/Хард)\n"
                        "14:00-15:00 День (Грунт/Хард)\n\n"
                        "<u>СРЕДА</u> (Начинающие, NTRP 0-2.0)\n"
                        "08:00-09:00 Утро (Грунт/Хард)\n"
                        "14:00-15:00 День (Грунт/Хард)\n\n"
                        "<u>ПЯТНИЦА</u> (Продолжающие, NTRP 2.0-3.5)\n"
                        "08:00-09:00 Утро (Грунт/Хард)\n"
                        "14:00-15:00 День (Грунт/Хард)\n\n"
                        '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard, parse_mode='HTML')
    await callback_query.answer() #Убирает часики с кнопки

@dp.callback_query(F.data == 'button_Nalichnay_schedule')
async def process_show_price_vaska(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)#Убирает часики с кнопки
   
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_show_schedule]])
    
    await callback_query.message.edit_text(text='Вы выбрали <b>Наличная</b>\n\n'
                        "<u>ПОНЕДЕЛЬНИК</u> (Продолжающие, NTRP 2.0-3.5)\n"
                        "21:00-22:30\n\n"
                        "<u>ВТОРНИК</u> (Продолжающие, NTRP 2.0-3.5)\n"
                        "21:00-22:30\n\n"
                        "<u>СРЕДА</u> (Средние, NTRP 3.5-4.5)\n"
                        "21:00-22:30\n\n"
                        "<u>ЧЕТВЕРГ</u> (Продолжающие, NTRP 2.0-3.5)\n"
                        "21:00-22:30\n\n"
                        "<u>ПЯТНИЦА</u> (Средние, NTRP 3.5-4.5)\n"
                        "21:00-22:30\n"
                        '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard, parse_mode='HTML')
    await callback_query.answer() #Убирает часики с кнопки

@dp.callback_query(F.data == 'show_address')
async def process_show_address_callback(callblack: CallbackQuery):
    await bot.answer_callback_query(callblack.id) #Убирает часики с кнопки
     # Создаем клавиатуру только с кнопкой "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[dynamit_button_location],[dinamo_button_location],[vaska_button_location],[back_button]])
    await callblack.message.edit_text(text='Выбери нужную кнопку для получения <u>адреса</u>.\n'
    '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard, parse_mode='HTML')
    await callblack.answer() #Убирает часики с кнопки
  
@dp.callback_query(F.data == 'vaska_button_location')
async def process_vaska_button(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)#Убирает часики с кнопки
    # Создаем клавиатуру только с кнопкой "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_show_address]])   
    await callback_query.message.edit_text(
        text='Вы выбрали <b>"Наличная"</b>\n\nАдрес: Наличная улица 44, корпу.6К\n\n'
        'Тип корта: Хард, закрытый корт\n(Каркас)\n\n'
        'Описание: Посещение на этот тип корта, <b>разрешено</b> только в кроссовках с <b>чистой подошвой</b>.\n'
        'Раздевалки с душем имеются.\n'
        'Парковка бесплатная.\n\n'
        'Нажмите кнопку "Назад", чтобы вернуться назад.', reply_markup=back_keyboard, parse_mode='HTML')
    # Отправляем координаты точки на карте
    await bot.send_location(callback_query.from_user.id) #latitude=latitude, longitude=longitude)

@dp.callback_query(F.data == 'dynamit_button_location')
async def process_dynamit_button(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)  # Убирает часики с кнопки
    # Создаем клавиатуру только с кнопкой "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_show_address]])
    await callback_query.message.edit_text(
        text='Вы выбрали <b>"ВМФ"</b>\n\nАдрес: Средний просп. Васильевского острова, 87\n\n'
        'Тип корта: Грунт, открытый корт\n\n'
        'Описание: На этот тип корта стоит брать кроссовки которые не жалко испачкать, в жаркие дни стоит брать с собой достаточное количество воды и крем от загара.\n'
        'Раздевалки с душем есть в соседнем здании (ВМФ бассейн).\n' 
        'Парковка бесплатная\n\n'
        'Нажмите кнопку "Назад", чтобы вернуться назад.', reply_markup=back_keyboard, parse_mode='HTML')
    # Отправляем координаты точки на карте
    await bot.send_location(callback_query.from_user.id) #latitude=latitude, longitude=longitude)

@dp.callback_query(F.data == 'dinamo_button_location')
async def process_dynamit_button(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)  # Убирает часики с кнопки
    # Создаем клавиатуру только с кнопкой "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_show_address]])
    await callback_query.message.edit_text(
        text='Вы выыбрали <b>"Динамо"</b>\n\nАдрес: Центр тенниса, Спортивная ул. 8\n\n'
        'Тип корта: Хард, закрытый корт\n(каркас)\n'
        'Грунт, открытый корт\n\n'
        'Описание : В зависимости от выбора вашей группы вам стоит подобрать кроссовки подходящие под покрытие корта.\n' 
        'Есть раздевалки с душем.\n'
        'Парковка городская 100р/час или прямо у кортов (заезд через шлагбаум - 400р/день).\n\n'
        'Нажмите кнопку "Назад", чтобы вернуться назад.', reply_markup=back_keyboard, parse_mode='HTML')
    # Отправляем координаты точки на карте
    await bot.send_location(callback_query.from_user.id) #latitude=latitude, longitude=longitude)

# Здесь заполняется информация по кнопке Контакты тренеров
@dp.callback_query(F.data == 'contact')
async def process_conctact_callback(callblack: CallbackQuery):
    await bot.answer_callback_query(callblack.id) #Убирает часики с кнопки
     # Создаем клавиатуру только с кнопкой "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[Kuznetsova_button],[Ivanova_button],[Savin_button],[back_button]])
    await callblack.message.edit_text(text='Здесь информация о тренерах школы.\nВыбери нужного тренера для детальной информации\n'
    '.\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard)
    await callblack.answer() #Убирает часики с кнопки

@dp.callback_query(F.data == 'Kuznetsova')
async def process_Kuznetsova_press(callblack: CallbackQuery):
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_contact]])
    await bot.answer_callback_query(callblack.id) #Убирает часики с кнопки
    await callblack.message.edit_text(text='▪️Тренер : Кузнецова Елизавета Евгеньевна\n'
'▪️Любимый удар: бэкхенд (слева)\n'
'помимо тенниса, любит танцы и путешествия\n'
'▪️Коронная фраза : «ну и всё»\n'
'▪️Любимый смайл : 😈\n'
'▪️Особенности: судья по теннису 👩‍⚖️\n'
'▪️Специфика работы :\n'
'- Тренировки с "нуля"\n'
'- Детские и взрослые групповые и индивидуальные тренировки\n'
'- Спарринг\n' 
'- Сплит тренировки\n'
'▪️Обучаю профессиональной технике, благодаря которой сможете не только активно проводить время, но и получать удовольствие от своей игры 🎾\n' \
'https://t.me/ссылк_На_Юзера', reply_markup=back_keyboard)
    await callblack.answer() #Убирает часики с кнопки

# Возврат в предыдущие меню
@dp.callback_query(F.data == 'back_button_contact')
async def process_conctact_callback(callblack: CallbackQuery):
    await bot.answer_callback_query(callblack.id) #Убирает часики с кнопки
     # Создаем клавиатуру только с кнопкой "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[Kuznetsova_button],[Ivanova_button],[Savin_button],[back_button]])
    await callblack.message.edit_text(text='Здесь информация о тренерах школы.\nВыбери нужного тренера для детальной информации\n'
    '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard)
    await callblack.answer()

@dp.callback_query(F.data == 'back')
async def process_contact_press(callblack: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callblack.id)  # Убирает часики с кнопки
    # Здесь Вы можете вернуть пользователя в предыдущее меню
    previous_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Кузнецова', callback_data='Kuznetsova')],
        [InlineKeyboardButton(text='Другой тренер', callback_data='OtherCoach')]
    ]) 
    await callblack.message.edit_text(
        text='Выберите тренера:',
        reply_markup=previous_menu_keyboard
    )

@dp.callback_query(F.data == 'Ivanova')
async def process_Kuznetsova_press(callblack: CallbackQuery):
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_contact]])
    await bot.answer_callback_query(callblack.id) #Убирает часики с кнопки
    await callblack.message.edit_text(text='🔹Тренер : Грега Дарья Александровна\n'
'🔹Любимый удар: подача\n'
'🔹Увлечения : помимо тенниса, любит машины 🛞\n'
'Коронная фраза : «расслабься, как на йоге»\n'
'🔹Любимый смайл : 😏\n'
'🔹Специфика работы :\n'
'- Обучение от 0 до 100\n'
'- Подготовки к турнирам\n'
'- Тактика\n'
'- Индивидуальные/сплит/групповые тренировки\n'
'🔹Обучаю играть красиво и без напряга, к каждому игроку индивидуальный подход и подходящая техника. Тренирую нежно и с любовью)\n'
'🔹P.S Не фанат садомазного обучения 🥵\n' 
'https://t.me/ссылка_На_тренера', reply_markup=back_keyboard)
    await callblack.answer() #Убирает часики с кнопки

@dp.callback_query(F.data == 'back_button_contact')
async def process_conctact_callback(callblack: CallbackQuery):
    await bot.answer_callback_query(callblack.id) #Убирает часики с кнопки
     # Создаем клавиатуру только с кнопкой "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[Kuznetsova_button],[Ivanova_button],[Savin_button],[back_button]])
    await callblack.message.edit_text(text='Здесь информация о тренерах школы.\nВыбери нужного тренера для детальной информации\n'
    '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard)
    await callblack.answer()

@dp.callback_query(F.data == 'Savin')
async def process_Kuznetsova_press(callblack: CallbackQuery):
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button_contact]])
    await bot.answer_callback_query(callblack.id) #Убирает часики с кнопки
    await callblack.message.edit_text(text='🔺Тренер: Савин Роман Андреевич\n'
'🔺Любимый смайл: ☝️\n'
'🔺Любимый удар: форхенд (левша)\n'
'🔺Любимая фраза: «вот это было здорово!»\n'
'🔺Помимо тенниса: люблю бегать, играть в волейбол и баскетбол, науку и технику\n'
'🔺Специфика работы:\n'
'- Индивидуальные тренировки\n'
'- Групповые тренировки\n'
'- Спарринг\n'
'- Сплит-тренировки\n'
'- Партнер по парным турнирам\n'
'🔺Особенности: Люблю спорт и привлекать людей им заниматься 😏\n'

'P. S Считаю, что все проблемы на корте из за плохо работающих ног\n'
'https://t.me/ссылка_На_тренера', reply_markup=back_keyboard)
    await callblack.answer() #Убирает часики с кнопки    

@dp.callback_query(F.data == 'back_button_contact')
async def process_conctact_callback(callblack: CallbackQuery):
    await bot.answer_callback_query(callblack.id) #Убирает часики с кнопки
     # Создаем клавиатуру только с кнопкой "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[Kuznetsova_button],[Ivanova_button],[Savin_button],[back_button]])
    await callblack.message.edit_text(text='Здесь информация о тренерах школы.\nВыбери нужного тренера для детальной информации\n'
    '\nНажмите кнопку "Назад", чтобы вернуться в главное меню.', reply_markup=back_keyboard)
    await callblack.answer()

@dp.callback_query(F.data == 'abonement')
async def process_abonement_press(callblack: CallbackQuery):
     # Создаем клавиатуру только с кнопкой "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
   
# Редактируем сообщение, заменяя старую клавиатуру на новую
    await callblack.message.edit_text(text='1. Абонемент приобретается на период одного месяца (на 28 календарных дней или 4 недели).\n\n'
'2. В случае заболевания необходимо заранее уведомить о невозможности посещения тренировок!\n\n'
'3. При пропуске более чем одного занятия по причине заболевания - предоставляйте, пожалуйста, справку, если это возможно.\n\n'
'4. По другим причинам допускается однократное отсутствие на занятии с возможностью отыгрыша в другой день при наличии свободных мест. В случае отсутствия мест тренировка может быть проведена на "ВМФ (Средний проспект 87 В.О.)" или "Наличная ул 44к6".\n\n'
'5. Заранее уведомляйте о своем желании закрепить место в определенный день для бронирования с использованием вашего абонемента. При изменении предпочтений в выборе дня тренировок, гарантия зарезервированного места не предоставляется, так как место может быть выделено другому ученику.\n\n'
'6. Длительность тренировок определяется количеством участников: до 2 человек включительно – 1 час, от 3 человек – 1,5 часа.\n\n'
'Важно! При полном наборе группы в 4 человека тренировка длится 1,5 часа. Если кто-то не пришел, тренировка у отсутствующего «сгорает».\n\n'
'7. Если вы предупреждаете менее чем за 24 часа о своем отсутствии на тренировке, ваше занятие «сгорает».', reply_markup=back_keyboard)

@dp.message()
async def fallback(message: types.Message):
    await message.answer("Необходимо ввести более точный запрос")

@dp.errors()
async def error_handler(update: types.Update, exception: Exception):
    logging.error(f"Update: {update} caused error: {exception}")

if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    asyncio.run(dp.start_polling(bot))