import telebot
from telebot import types
import os
import tour_rotes
from telebot.types import InputMediaPhoto
# Создаем бота с вашим API-ключом
bot = telebot.TeleBot('7195856034:AAHe1E3IEctEnk0oUEb45ZwPg3fQBirOSAg')

# Токен платежного провайдера от BotFather для ЮKassa
PAYMENT_PROVIDER_TOKEN = '381764678:TEST:89735'  # Замените на ваш токен от BotFather

class Tour:
    def __init__(self,chat_id):
        self.chat_id=chat_id

    def send_text(self,text):
        bot.send_message(self.chat_id, text)

    def send_photo(self, photo_paths, caption=None):
        media = []
        open_files = []  # Список для хранения открытых файлов

        try:
            for i, photo_path in enumerate(photo_paths):
                if not os.path.exists(photo_path):
                    self.bot.send_message(self.chat_id, f"Файл {photo_path} не найден.")
                    return

                # Открываем файл и добавляем в список
                photo = open(photo_path, 'rb')
                open_files.append(photo)

                # Добавляем подпись к последнему фото, если указано
                if i == len(photo_paths) - 1 and caption:
                    media.append(InputMediaPhoto(photo, caption=caption))
                else:
                    media.append(InputMediaPhoto(photo))

            # Отправляем группу фотографий
            self.bot.send_media_group(self.chat_id, media)

        except Exception as e:
            self.bot.send_message(self.chat_id, f"Ошибка отправки медиа-группы: {e}")

        finally:
            # Закрываем все открытые файлы
            for photo in open_files:
                photo.close()

    def send_location(self, latitude, longitude):
        bot.send_location(self.chat_id, latitude, longitude)

    def send_button(self, button_text, callback_data):
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
        keyboard.add(button)
        bot.send_message(self.chat_id, "Нажмите кнопку ниже:", reply_markup=keyboard)



# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("Азиатский маршрут", callback_data='asian_route')
    btn2 = types.InlineKeyboardButton("Галатский  маршрут", callback_data='evening_route')
    btn3 = types.InlineKeyboardButton("Европейский маршрут", callback_data='european_route')

    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, "Добро пожаловать в Стамбул. По какому маршруту вы хотите пройтись?", reply_markup=markup)


# Обработка нажатий на инлайн-кнопки выбора маршрута
@bot.callback_query_handler(func=lambda call: call.data in ['asian_route', 'evening_route', 'european_route'])
def handle_route_selection(call):
    if call.data == 'asian_route':
        bot.send_message(call.message.chat.id, "Вы выбрали Азиатский маршрут!")
    elif call.data == 'evening_route':
        # Отправляем фотографию с инлайн-кнопкой оплаты
        markup = types.InlineKeyboardMarkup()
        pay_button = types.InlineKeyboardButton("Оплатить 300 ", callback_data='successful_payment')
        markup.add(pay_button)

        # Замените 'image.jpg' на путь к вашей картинке или URL
        photo = open('C:\\Users\\User\\Downloads\\photo_5354815055872517578_y.jpg', 'rb')  # если фото на сервере
        bot.send_photo(call.message.chat.id, photo, caption="Вы выбрали Галатский маршрут!", reply_markup=markup)
    elif call.data == 'european_route':
        bot.send_message(call.message.chat.id, "Вы выбрали Галатский маршрут!")


# Обработка нажатия на кнопку "Оплатить 300" (имитация успешной оплаты)
@bot.callback_query_handler(func=lambda call: call.data == 'successful_payment')
def handle_fake_payment(call):
    bot.send_message(call.message.chat.id, 'Оплата успешно проведена! Спасибо за ваш выбор!')

    # Описание тура после успешной оплаты
    tour_description = """
    Галатский маршрут- маршрут покажет вам новый город Стамбула, Стамбул который больше близок к Европе и западной культуре.
    На этой экскурсии вас ждет много интересных мест с красивыми видами и необычной вкусной едой!
    Основные точки маршрута:
    1. Район Каракой
    2. Улица с зонтиками и подземная мечеть.
    3. Рыба в лаваше 
    4. Баклава Karaköy Güllüoğlu
    5. Галатапорт
    6. Фуникулер
    7. Площадь Taksim
    8. Улица Istiklal
    9. Ирландский pub U2
    10. Галатская башня.
    """

    # Отправляем описание экскурсии
    bot.send_message(call.message.chat.id, tour_description)

    # Отправляем сообщение с вопросом и кнопкой "Начать экскурсию"
    markup = types.InlineKeyboardMarkup()
    start_tour_button = types.InlineKeyboardButton("Начать экскурсию", callback_data='start_tour')
    markup.add(start_tour_button)

    bot.send_message(call.message.chat.id, "Хотите начать экскурсию?", reply_markup=markup)


tour_rotes.register_handlers(bot)


# Запуск бота
bot.polling(none_stop=True)
