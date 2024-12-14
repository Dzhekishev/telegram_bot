from telebot import types
from telebot.types import InputMediaPhoto
import os
class Tour:
    def __init__(self, chat_id, bot):
        self.chat_id = chat_id
        self.bot = bot

    def send_text(self, text):
        self.bot.send_message(self.chat_id, text)

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
        self.bot.send_location(self.chat_id, latitude, longitude)

    def send_buttons(self, button_text, callback_data, detail_url=None):
        keyboard = types.InlineKeyboardMarkup()

        # Кнопка "Далее"
        next_button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
        keyboard.add(next_button)

        # Кнопка "Подробнее", если указана ссылка
        if detail_url:
            detail_button = types.InlineKeyboardButton(text="Подробнее", url=detail_url)
            keyboard.add(detail_button)

        self.bot.send_message(self.chat_id, "Нажмите кнопку ниже:", reply_markup=keyboard)


# Функция для регистрации обработчиков
def register_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == 'start_tour')
    def handle_start_tour(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517387_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517392_y.jpg'],
                        "Ваша первая точка — Каракой.\n"
                        "Чтобы добраться сюда можете воспользоваться трамваем T1 или если вы со стороны Галатской башни, можете доехать на Тюнеле.")
        tour.send_location(41.022173, 28.975135)
        tour.send_buttons("Далее", "perehod", "https://tr.wikipedia.org/wiki/Karak%C3%B6y")

    @bot.callback_query_handler(func=lambda call: call.data == 'perehod')
    def handle_second_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517395_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517398_y.jpg'],
                        "Когда вы доехали до станции, выйдете с нее и направьтесь в правую сторону. Перейдите дорогу и пройдите направо, спуститесь через ступеньки и пройдите через проход")
        tour.send_buttons("Далее", "umbrella")

    @bot.callback_query_handler(func=lambda call: call.data == 'umbrella')
    def handle_third_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517406_y.jpg'],
                        "Ваша вторая точка — Улица Зонтиков.\n"
                        "Это одна из улиц с зонтиками в Стамбуле, раньше в этих местах находился большой челночный рынок, куда приезжали много покупателей со стран СНГ.\n"
                        'Они покупали товары здесь и на кораблях отправляли их в порты Сочи, Одессы...\n'
                        'В связи с этим здесь можете увидеть несколько заведений с русскими названиями-Odessa, Бабушка и Дедушка\n'
                        'Идите дальше по этой улице для нашей третьей точки.')
        tour.send_location(41.022175, 28.976544)
        tour.send_buttons("Далее", "moon", "https://example.com/umbrella")


    @bot.callback_query_handler(func=lambda call: call.data == 'moon')
    def handle_fourth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517409_y.jpg'],
                        'Ваша третья точка — Подземная мечеть.\n'
                        'Подземная мечеть-мечеть находящееся под землей, на фасаде мечети можете увидеть даты постройки мечети на 2 календарях: "Hicri"-(Григорианский, который мы все используем) и "Miladi"(Мусульманский, лунный календарь)')
        tour.send_location(41.022319, 28.976817)
        tour.send_buttons("Далее", "perehod2", "https://example.com/moon")

    @bot.callback_query_handler(func=lambda call: call.data == 'perehod2')
    def handle_fifth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517411_y.jpg'],
                        "После Подземной мечети, поверните налево на первом повороте и потом поверните направо\n"
                        'Идите прямо по этой улице.\n'
                        'Сейчас вы находитесь в новой части Стамбула, здесь вы можете заметить более европейскую архитектуру и культуру жизни.')
        tour.send_location(41.022903, 28.976842)
        tour.send_buttons("Далее", "perehod_balik")


    @bot.callback_query_handler(func=lambda call: call.data == 'perehod_balik')
    def handle_sixth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517414_y.jpg'],
                        "Поверните налево около заведения с алкоголью, которая на фотке.\n"
                        'Идите прямо по этой улице. По этой улице вы можете заметить Турецкую Ортодоксальную Церковь.\n'
                        'В Стамбуле как и мечетей много очень церквей и Православных, и Католических.\n'
                        'Когда выйдите на большую улицу идите влево и увидите заведение с Рыбой в лаваше.')
        tour.send_location(41.024932, 28.979054)
        tour.send_buttons("Далее", "balik")



    @bot.callback_query_handler(func=lambda call: call.data == 'balik')
    def handle_seventh_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\20241124_170558.jpg'],
                        "Ваша четвертая точка — Рыба в лаваше.\n"
                        "Balık Ekmek(Шаурма с рыбой)-вкусный Стамбульский уличный фаст-фуд, которому стоит уделить внимание")
        tour.send_location(41.025088, 28.978279)
        tour.send_buttons("Далее", "perehod_baklava", "https://example.com/balik")

    @bot.callback_query_handler(func=lambda call: call.data == 'perehod_baklava')
    def handle_eighth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517424_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517426_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517429_y.jpg',],
                        "Для следующей точки надо вернуться на прошлую улицу с ресторанами\n"
                        "Идите по этой улице прямо\n"
                        "По дороге вы увидите место где продают жаренные кишки и турецкий зимний напиток Салеп.\n"
                        "Поверните на повороте направо и сразу налево.")
        tour.send_buttons("Далее", "baklava")

    @bot.callback_query_handler(func=lambda call: call.data == 'baklava')
    def handle_nineth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\20241124_171450.jpg',
                        'C:\\Users\\User\\Downloads\\20241124_171249.jpg'],
                        "Ваша пятая  точка — Баклава Гулоглу.\n"
                        "Karaköy Güllüoğlu - Кондитерская с самыми вкусной пахлавой во всей Турции, здесь вы можете попробовать все виды пахлавы\n"
                        "Это заведение входит в Топ 10 Мест со сладостями по версии TasteAtlas.\n"
                        "Здесь мы вам советуем попробовать Soğuk Baklava(Соук Пахлава) не приторная пахлава с молоком в составе.")
        tour.send_location(41.025340, 28.980137)
        tour.send_buttons("Далее", "perehod_galataport", "https://example.com/baklava")

    @bot.callback_query_handler(func=lambda call: call.data == 'perehod_galataport')
    def handle_tenth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517446_y.jpg',
                        'C:\\Users\\User\\Downloads\\photo_5354815055872517449_y.jpg',
                        'C:\\Users\\User\\Downloads\\photo_5354815055872517450_y.jpg'],
                        "После пахлавы, мы выходим через задний вход\n"
                        "Переходим дорогу и заходим в вход в магазин\n"
                        "Здесь вы должны пройти проверку, пропустите сумки, портфели через сканнер, а телефоны поствьте на стойку рядом с металлоискателем\n"
                        "Вы окажетесь магазине одежды и обуви, но нам это не важно, вы должны пройти через выход на фотке.")
        tour.send_buttons("Далее", "galataport")


    @bot.callback_query_handler(func=lambda call: call.data == 'galataport')
    def handle_eleventh_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517457_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517460_y.jpg'],
                        "Ваша шестая точка — Галатопорт.\n"
                        "Галатапорт-порт, торговый центр с невероятным видом на Босфор, Азиатскую часть Стамбула.\n"
                        "Галатопорт современнный порт с множеством заведений и магазинов.")
        tour.send_location(41.024515, 28.981252)
        tour.send_buttons("Далее", "galataport_inside", "https://example.com/galataport")


    @bot.callback_query_handler(func=lambda call: call.data == 'galataport_inside')
    def handle_twelveth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517463_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517465_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517466_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517469_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517472_y.jpg'],
                        'Внутри Галатапорта вы сможете увидеть Стамбульский музей современных исскуств "Istanbul Modern" \n'
                        "Также за музеем вы увидите мечеть Нусретие. Мечеть Нусретие, показатель того что Стамбул является местом встречи Востока и Запада.\n"
                        "Мечеть представляет из себя восточное, а архитектура этой мечети сделана в европейском стиле. Также рядом с мечетью вы можете заметить Часовую башню\n"
                        "В конце Галатапорта вы увидите арт-обьект на котором написаны все названия Стамбула. ")
        tour.send_buttons("Далее", "exit_galataport", "https://example.com/galataport")


    @bot.callback_query_handler(func=lambda call: call.data == 'exit_galataport')
    def handle_thirteenth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517475_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517476_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517480_y.jpg'],
                        "Дойдя до конца Галатапорта вам откроется отличный вид на Босфорский мост, сейчас он называется Мост Мучеников 15 Июля, почему он так назван можете узнать нажав на кнопку подробнее.\n"
                        "После прекрасного вида, вам нужно пройти направо к выходу.\n"
                        "Выйдите с Галатапорта и пройдите на улицу.")
        tour.send_buttons("Далее", "perehod_mimar", "https://example.com/galataport")


    @bot.callback_query_handler(func=lambda call: call.data == 'perehod_mimar')
    def handle_fourteenth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517482_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517489_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517492_y.jpg'],
                        "После выхода с Галатапорта, вам надо повернуть направо и идти прямо по этой улице.\n"
                        "По дороге вы можете увидеть Университет прекрасных исскуств имени Мимара Синана.\n"
                        "Мимар Синан, является одним из великих архитекторов своего времени, а именно 16 века.")
        tour.send_location(41.030491, 28.988808)
        tour.send_buttons("Далее", "perehod_tsunami", "https://example.com/galataport")


    @bot.callback_query_handler(func=lambda call: call.data == 'perehod_tsunami')
    def handle_fifteenth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517497_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517493_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517496_y.jpg'],
                        "Вам нужно дойти до арки на фото.\n"
                        "По дороге можете увидеть знак в случае куда нужно бежать если будет цунами.\n"
                        "Довольно необычный знак, согалситесь, но не беспокойтесь в Стамбуле цунами почти не бывает.")
        tour.send_buttons("Далее", "perehod_funikuler")


    @bot.callback_query_handler(func=lambda call: call.data == 'perehod_funikuler')
    def handle_sixteenth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517500_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517503_y (1).jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517505_y.jpg'],
                        "Пройдите через арку, справа вы можете увидеть холм с видом на Босфор и приплывающие корабли к порту, советую пройти туда и сделать несколько красивых фото.\n"
                        "Для следующей нашей точки вы должны спуститься вниз в Фуникулер, пройти через турникеты.")
        tour.send_buttons("Далее", "funikuler")


    @bot.callback_query_handler(func=lambda call: call.data == 'funikuler')
    def handle_seventeenth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517507_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517514_y.jpg'],
                        "Фуникулер-это вид рельсового транспорта под землей. Инными словами это смесь Канатной дороги и Метро.\n"
                        "Имеет только 2 станции, катается вверх-вниз.")
        tour.send_location(41.033497, 28.992372)
        tour.send_buttons("Далее", "perehod_taksim", "https://example.com/funikuler")


    @bot.callback_query_handler(func=lambda call: call.data == 'perehod_taksim')
    def handle_eighteenth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517519_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517520_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517521_y.jpg'],
                        "Как вам поездка на фуникулере?Необычно правда?\n"
                        "А теперь вам нужно выйти с фуникулера и пройти через левый проход, который на фото и подняться вверх.")
        tour.send_buttons("Далее", "taksim")



    @bot.callback_query_handler(func=lambda call: call.data == 'taksim')
    def handle_nineteenth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517525_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517527_y.jpg'],
                         "Вы на площади Таксим!\n"
                         "Площадь Taksim- это один центров Стамбула, являющийся символом Турецкой Республики.\n"
                         'По середине плошади находится монумент "Республика"(Cumhuriyet Anıtı).\n'
                         'Монумент символизирует армию-освободительницу и установление республики.\n'
                         'В центре памятника находится Мустафа Кемаль Ататюрк.')
        tour.send_location(41.036908, 28.985379)
        tour.send_buttons("Далее", "istiklal", "https://example.com/taksim")

    @bot.callback_query_handler(func=lambda call: call.data == 'istiklal')
    def handle_nineth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517532_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517535_y.jpg'],
                         "Ваша 9 точка — Istiklal.\n"
                         "İstiklal Caddesi- проспект независимости, пешеходная улица Стамбула длинной 1.5 км.\n"
                         "Является одной из самых популярных туристических мест.\n"
                         "Здесь вы можете увидеть красный исторический трамвай, здания в европейском стиле, множество магазинов и заведений.\n"
                         'Также на этой улице много красивых пассажей, например "Çiçek Pasajı" и консульств многих стран.\n')
        tour.send_location(41.036188, 28.984323)
        tour.send_buttons("Далее", "pub", "https://example.com/istiklal")




    @bot.callback_query_handler(func=lambda call: call.data == 'pub')
    def handle_tenth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517543_y.jpg',
                        'C:\\Users\\User\\Downloads\\photo_5354815055872517546_y.jpg',
                        'C:\\Users\\User\\Downloads\\photo_5354815055872517547_y.jpg',
                        'C:\\Users\\User\\Downloads\\photo_5354815055872517548_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517540_y.jpg'],
                         "Ваша 10 точка — U2 pub.\n"
                         "Если вы устали и хотите отдохнуть и вы сне против алкоголя, то можем вам предложить сходить Ирландский паб U2.\n"
                         "Это очень интересное заведение оказавшись тут , вы переместитесь из Стамбула в Ирландию.\n"
                         "Это единственный Ирландский паб в Турции имеющий сертификат Guiness от Компании Guiness, сертификат показывает, что в этом месте пиво Guiness разливается по всем стандартам и имеет оригинальный вкус.\n"
                         "Здесь вы встретитесь с добрым и общительным барменом Лео, также вы здесь можете встретиться и пообщаться с людьми со всех уголков нашей планеты.\n"
                         "Чтобы пройти сюда, вам нужно повернуть направо на улице Bekar и идти прямо.")
        tour.send_location(41.036544, 28.981972)
        tour.send_buttons("Далее", "perehod_istiklal")


    @bot.callback_query_handler(func=lambda call: call.data == 'perehod_istiklal')
    def handle_nineth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517550_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517555_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517562_y.jpg'],
                         "Если вы решили выпить и отдохнуть в пабе, то чтобы продолжить нашу экскурсию, вам нужно венруться на проспект Истикляль.\n"
                         'Как я говорил раннее здесь много красивых пассажей, по пути вы увидите пассажи "Grand Pera" и "Çiçek Pasajı" последний раньше являлся театром.\n'
                         "Так же по дороге вы увидите очень красивую Церковь Святой Марии, если она открыта то советую вам туда тоже заглянуть.\n"
                         "Кстати если вы из России, то вот вам наверное интересно будет снаружи взглянуть на Российское консульство, которое также находится здесь, про это консульство есть очень интересная информация.\n")
        tour.send_buttons("Далее", "music_street", "https://example.com/istiklal")



    @bot.callback_query_handler(func=lambda call: call.data == 'music_street')
    def handle_eleventh_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517568_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517573_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517565_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517563_y.jpg'],
                         "Ваша 11 точка — Music Street!\n"
                         "Музыкальная улица - улица на которой продаются много музальных инструментов, а так же здесь вы можете приобрести сувениры по приемлемым ценнам.\n"
                         "Чтобы пройти сюда, вам нужно повернуть налево, в сторону, которая указана на фото.")
        tour.send_location(41.028484, 28.974539)
        tour.send_buttons("Далее", "perehod_tower", "https://example.com/music_street")


    @bot.callback_query_handler(func=lambda call: call.data == 'perehod_tower')
    def handle_eleventh_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517570_y.jpg',
                         'C:\\Users\\User\\Downloads\\photo_5354815055872517575_y.jpg'],
                         "Чтобы пройти до нашей следующей точке, на развилке, вам следует повернуть в левую сторону, там где стоит обменник.\n"
                         "Идите прямо, пока не увидите большое скопление людей, место похожее на 2 фотку.\n"
                         "Повернув голову направо, вы увидите прекрасную башню.")
        tour.send_buttons("Далее", "tower")


    @bot.callback_query_handler(func=lambda call: call.data == 'tower')
    def handle_twelveth_point(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_photo(['C:\\Users\\User\\Downloads\\photo_5354815055872517578_y.jpg'],
                        "Ваша 12 точка — Galata Tower!\n"
                        "Галатская башня- смотровая башня построенная в 14 веке Генуэзами, основавшие этот район.\n"
                        "Раньше использовался как ориентир для мореплавателей. Вначале имел высоту 65 метров, сейчас высотой 45 метров.\n"
                        "С башни открываются прекрасные виды на Стамбул.\n"
                        "Есть история что в 1632 году османский инженер спрыгнул с башни на самодельных крыльях и перелетел Босфор, благополучно приземлился в азиатской части города, за что был награждён султаном, а позже изгнан в Алжир.")
        tour.send_location(41.026121, 28.974787)
        tour.send_buttons("Завершить экскурсию", "end_tour", "https://example.com/tower")

    @bot.callback_query_handler(func=lambda call: call.data == 'end_tour')
    def handle_end_tour(call):
        tour = Tour(call.message.chat.id, bot)
        tour.send_text("Экскурсия завершена! Спасибо за участие.")
