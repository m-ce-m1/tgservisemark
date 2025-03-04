import telebot
from telebot import types
from telebot.types import WebAppInfo
import database
import config
import datetime

# Инициализация базы данных
db = database.Database()

# Инициализация переменных из конфигурационного файла
BOT_TOKEN = config.BOT_token
CHANNEL_ID = config.id
CHANNEL_LINK = config.link

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Функция для проверки подписки пользователя на канал
def check_subscription(user_id):
    try:
        # Получаем информацию о статусе пользователя в канале
        chat_member = bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Проверяем, является ли пользователь подписчиком, администратором или создателем канала
        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False

# Функция для отправки меню доступных действий после подписки
def send_actions_menu(chat_id):
    # Проверяем наличие активной подписки
    has_subscription = db.check_active_subscription(chat_id)
    
    subscription_text = ""
    if has_subscription:
        subscription_text = "\n/my_subscription — Информация о подписке"
    
    bot.send_message(
        chat_id,
        "🎉 <b>Спасибо за вашу подписку!</b> 🎉\n"
        "Теперь вы можете пользоваться всеми функциями нашего бота. Наслаждайтесь удобством и новыми возможностями!\n"
        "✨ <b>Если вы уже были подписанны</b>, рады видеть вас снова! Ваш доступ ко всем функциям сохранен."
        "\n\nВыберите действие, чтобы продолжить:"
        "\n/services — Доступные сервисы"
        "\n/help — Помощь и инструкции"
        "\n/pay_subscription - Оплатить подписку"
        "\n/donate - Пополнить баланс"
        f"{subscription_text}",
        parse_mode="html"
    )

# Функция для отправки меню доступных сервисов
def send_services_menu(chat_id):
    markup = types.InlineKeyboardMarkup()

    # Создаем кнопки для каждого сервиса
    button1 = types.InlineKeyboardButton("Удалить водяной знак", callback_data='watermark')
    button2 = types.InlineKeyboardButton("Скачать фото Инстаграмм", callback_data='inst_photo')
    button3 = types.InlineKeyboardButton("Переводчик", callback_data='translator')
    button4 = types.InlineKeyboardButton("Сгенерировать картинку", callback_data='midjourne')
    button5 = types.InlineKeyboardButton("Чат гпт", callback_data='chat_gpt')

    # Располагаем кнопки в меню
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.add(button5)

    # Отправляем сообщение с меню сервисов
    bot.send_message(
        chat_id,
        'Выбери сервис, который тебе нужен:',
        reply_markup=markup
    )

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Получаем имя и фамилию пользователя
    last_name = message.from_user.last_name or ""
    first_name = message.from_user.first_name or ""
    full_user_name = f"{last_name} {first_name}".strip()
    
    # Регистрируем пользователя в базе данных
    user_id = message.from_user.id
    is_new_user = db.add_user(user_id)
    
    # Отправляем приветственное сообщение
    bot.send_message(
        message.chat.id,
        f'<b>🌟 Добро пожаловать, {full_user_name}! 🌟</b>'
        '\n\nПриветствуем в самом функциональном <u>Telegram-сервисе!</u>🚀'
        '\nЗдесь ты сможешь взаимодействовать с множеством полезных ботов, которые сделают твою жизнь проще, удобнее и приятнее. 💡'
        '\n\n📌 Что у нас есть?'
        '\n— Умные помощники для повседневных задач'
        '\n— Удобные инструменты для работы и отдыха'
        '\n— Постоянно растущий список функций и сервисов',
        parse_mode='html'
    )

    # Проверяем, подписан ли пользователь на канал
    if not check_subscription(message.from_user.id):
        # Если не подписан, предлагаем подписаться
        markup = types.InlineKeyboardMarkup()
        subscribe_button = types.InlineKeyboardButton("Подписаться на канал", url=CHANNEL_LINK)
        check_button = types.InlineKeyboardButton("Я подписался ✅", callback_data='check_subscription')
        markup.add(subscribe_button, check_button)

        bot.send_message(
            message.chat.id,
            "Чтобы продолжить пользоваться ботом, подпишитесь на наш канал:",
            reply_markup=markup
        )
    else:
        # Если подписан, отправляем меню действий
        send_actions_menu(message.chat.id)

# Обработчик для кнопки "Я подписался"
@bot.callback_query_handler(func=lambda call: call.data == 'check_subscription')
def check_subscription_callback(call):
    if check_subscription(call.from_user.id):
        # Если пользователь подписался, отправляем сообщение и меню действий
        bot.answer_callback_query(call.id, "Спасибо за подписку! Теперь вы можете пользоваться ботом.")
        send_actions_menu(call.message.chat.id)
    else:
        # Если пользователь всё ещё не подписан, уведомляем его
        bot.answer_callback_query(call.id, "Вы ещё не подписались на канал. Пожалуйста, подпишитесь.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def helper(message):
    # Проверяем наличие активной подписки
    has_subscription = db.check_active_subscription(message.from_user.id)
    
    subscription_text = ""
    if has_subscription:
        subscription_text = "4. /my_subscription - Информация о вашей подписке\n"
    
    bot.send_message(
        message.chat.id,
        "Помощь и инструкции:\n\n"
        "1. /start - Начать работу с ботом\n"
        "2. /services - Список доступных сервисов\n"
        "3. /pay_subscription - Оплатить подписку\n"
        "4. /donate - Пополнить баланс\n"
        f"{subscription_text}\n"
        "Если у вас есть вопросы, обратитесь в поддержку."
    )

# Обработчик команды /services
@bot.message_handler(commands=['services'])
def bots(message):
    if check_subscription(message.from_user.id):
        # Если пользователь подписан, отправляем меню сервисов
        send_services_menu(message.chat.id)
    else:
        # Если не подписан, просим подписаться
        bot.send_message(
            message.chat.id,
            "Пожалуйста, подпишитесь на канал, чтобы использовать сервисы."
        )

# Обработчик команды /my_subscription
@bot.message_handler(commands=['my_subscription'])
def my_subscription(message):
    user_id = message.from_user.id
    subscription = db.get_subscription(user_id)
    
    if not subscription:
        bot.send_message(
            message.chat.id,
            "У вас нет активных подписок. Используйте /pay_subscription, чтобы приобрести подписку."
        )
        return
    
    # Формируем сообщение о подписках
    subscription_text = "Ваши активные подписки:\n\n"
    
    if subscription["full_subscription"] > 0:
        months = subscription["full_subscription"]
        end_date = subscription["full_subscription_end"]
        subscription_text += f"✅ Полная подписка: {months} мес. (до {end_date})\n"
    
    if subscription["basic_subscription"] > 0:
        months = subscription["basic_subscription"]
        end_date = subscription["basic_subscription_end"]
        subscription_text += f"✅ Базовая подписка: {months} мес. (до {end_date})\n"
    
    if subscription["ad_free"] > 0:
        months = subscription["ad_free"]
        if subscription["ad_free_end"]:
            subscription_text += f"✅ Отключение рекламы: {months} мес. (до {subscription['ad_free_end']})\n"
        else:
            subscription_text += "✅ Отключение рекламы: навсегда\n"
    
    if "✅" not in subscription_text:
        subscription_text = "У вас нет активных подписок. Используйте /pay_subscription, чтобы приобрести подписку."
    
    # Добавляем информацию о балансе
    balance = db.get_balance(user_id)
    subscription_text += f"\n💰 Ваш текущий баланс: {balance} звезд (≈ {balance/50:.2f}$)"
    
    bot.send_message(message.chat.id, subscription_text)

# Обработчик callback_query для взаимодействия с кнопками меню сервисов
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'watermark':
        # Обработка выбора сервиса "Удалить водяной знак"
        bot.answer_callback_query(call.id, "Удалить водяной знак")
        caption = (
            'Данный сервис использует технологии искусственного интеллекта и компьютерного зрения для анализа видео и автоматического удаления водяных знаков, таких как логотипы, тексты или другие наложенные элементы. '
            'Он восстанавливает участки изображения под водяным знаком, делая видео чистым и профессиональным. Сервис подходит для обработки роликов с минимальными усилиями и может быть доступен онлайн или через специальное программное обеспечение.'
        )
        with open('photo/photo.jpeg', 'rb') as photo:
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton("Открыть", url=config.watermark)
            back_button = types.InlineKeyboardButton("Вернуться к списку сервисов", callback_data='back_to_services')
            markup.add(button)
            markup.add(back_button)
            bot.send_photo(
                call.message.chat.id,
                photo,
                caption=caption,
                reply_markup=markup
            )

    elif call.data == 'inst_photo':
        # Обработка выбора сервиса "Скачать фото Инстаграмм"
        bot.answer_callback_query(call.id, "Скачать фото Инстаграмм")
        caption = (
            'Данный сервис позволяет загружать и сохранять фото из Instagram на ваше устройство. '
            'Для этого достаточно вставить ссылку на публикацию Instagram, после чего сервис обработает запрос и предоставит возможность скачать изображение в высоком качестве. '
            'Это удобный инструмент для сохранения понравившихся фотографий, доступный онлайн или через приложения.'
        )
        with open('photo/inst.jpeg', 'rb') as photo:
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton("Открыть", url=config.inst_photo)
            back_button = types.InlineKeyboardButton("Вернуться к списку сервисов", callback_data='back_to_services')
            markup.add(button)
            markup.add(back_button)
            bot.send_photo(
                call.message.chat.id,
                photo,
                caption=caption,
                reply_markup=markup
            )

    elif call.data == 'translator':
        # Обработка выбора сервиса "Переводчик"
        bot.answer_callback_query(call.id, "Переводчик")
        caption = (
            'Данный сервис автоматически переводит текст, аудио, видео или речь с одного языка на другой. '
            'Он использует современные технологии, такие как искусственный интеллект и нейронные сети, чтобы обеспечить точный и естественный перевод. '
            'Сервис поддерживает множество языков и может работать с текстом, документами, изображениями (с распознаванием текста) и даже предоставлять实时 перевод речи. '
            'Доступен онлайн, через мобильные приложения или как встроенный инструмент в других платформах.'
        )
        with open('photo/trans.jpeg', 'rb') as photo:
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton("Открыть", url=config.translator)
            back_button = types.InlineKeyboardButton("Вернуться к списку сервисов", callback_data='back_to_services')
            markup.add(button)
            markup.add(back_button)
            bot.send_photo(
                call.message.chat.id,
                photo,
                caption=caption,
                reply_markup=markup
            )

    elif call.data == 'midjourne':
        # Обработка выбора сервиса "Сгенерировать картинку"
        bot.answer_callback_query(call.id, "Сгенерировать картинку")
        caption = (
            'Данный сервис использует технологии искусственного интеллекта, такие как нейронные сети, для генерации уникальных изображений на основе текстовых описаний или других входных данных. '
            'Вы можете ввести запрос (например, "закат в горах" или "футуристический город"), и сервис создаст соответствующее изображение. '
            'Он подходит для создания иллюстраций, концепт-арта, дизайна и других творческих задач. '
            'Сервис доступен онлайн или через специальные платформы, а некоторые инструменты также позволяют настраивать стиль и детализацию изображений.'
        )
        with open('photo/mid.jpeg', 'rb') as photo:
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton("Открыть", url=config.midjourne)
            back_button = types.InlineKeyboardButton("Вернуться к списку сервисов", callback_data='back_to_services')
            markup.add(button)
            markup.add(back_button)
            bot.send_photo(
                call.message.chat.id,
                photo,
                caption=caption,
                reply_markup=markup
            )

    elif call.data == 'chat_gpt':
        # Обработка выбора сервиса "Чат гпт"
        bot.answer_callback_query(call.id, "Чат гпт")
        caption = (
            'ChatGPT — это сервис на основе искусственного интеллекта, разработанный OpenAI, который использует модель GPT (Generative Pre-trained Transformer) для генерации текста. '
            'Он способен вести диалоги, отвечать на вопросы, помогать с написанием текстов, решением задач, обучением и многим другим. '
            'ChatGPT понимает контекст и может адаптироваться под запросы пользователя, предоставляя развернутые и осмысленные ответы. '
            'Сервис применяется в различных сферах, включая образование, бизнес, программирование и творчество. '
            'Доступен через веб-интерфейс, API или интеграцию в другие приложения.'
        )
        with open('photo/gpt.jpeg', 'rb') as photo:
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton("Открыть", url=config.chat_gpt)
            back_button = types.InlineKeyboardButton("Вернуться к списку сервисов", callback_data='back_to_services')
            markup.add(button)
            markup.add(back_button)
            bot.send_photo(
                call.message.chat.id,
                photo,
                caption=caption,
                reply_markup=markup
            )

    elif call.data == 'back_to_services':
        # Возвращаем пользователя к списку сервисов
        send_services_menu(call.message.chat.id)

# Обработчик команды /pay_subscription
@bot.message_handler(commands=['pay_subscription'])
def webshop(message):
    markup = types.InlineKeyboardMarkup()
    open_shop = types.InlineKeyboardButton('Список тарифов', web_app=WebAppInfo(url=config.web_site_link))
    markup.add(open_shop)

    bot.send_message(message.chat.id, "Для выбора тарифа перейдите в наше небольшое встроенное приложение в боте", reply_markup=markup)

# Обработчик команды /donate для пополнения баланса
@bot.message_handler(commands=['donate'])
def donate(message):
    bot.send_message(
        message.chat.id,
        "💰 <b>Пополнение баланса</b> 💰\n\n"
        "Введите сумму в звездах, которую хотите добавить на свой баланс.\n"
        "Минимальная сумма: 100 звезд (2$)\n"
        "Максимальная сумма: 10000 звезд (200$)\n\n"
        "Формат: <code>/add_stars [количество]</code>\n"
        "Например: <code>/add_stars 500</code>",
        parse_mode="html"
    )

# Обработчик команды /add_stars для добавления звезд
@bot.message_handler(commands=['add_stars'])
def add_stars(message):
    try:
        # Получаем количество звезд из сообщения
        command_parts = message.text.split()
        if len(command_parts) != 2:
            bot.send_message(
                message.chat.id,
                "❌ Неверный формат команды. Используйте: /add_stars [количество]"
            )
            return
        
        stars = int(command_parts[1])
        
        # Проверяем ограничения
        if stars < 100 or stars > 10000:
            bot.send_message(
                message.chat.id,
                "❌ Количество звезд должно быть от 100 до 10000."
            )
            return
        
        # Создаем платежную ссылку (в реальном проекте здесь была бы интеграция с платежной системой)
        payment_link = f"https://t.me/{bot.get_me().username}?start=payment_{message.from_user.id}_{stars}"
        
        # Отправляем сообщение с информацией о платеже
        markup = types.InlineKeyboardMarkup()
        pay_button = types.InlineKeyboardButton("Оплатить", url=payment_link)
        markup.add(pay_button)
        
        bot.send_message(
            message.chat.id,
            f"💫 <b>Пополнение баланса</b> 💫\n\n"
            f"Сумма: {stars} звезд (≈ {stars/50:.2f}$)\n"
            f"Пользователь: {message.from_user.first_name}\n\n"
            f"Нажмите кнопку ниже для оплаты:",
            parse_mode="html",
            reply_markup=markup
        )
        
        # В реальном проекте здесь был бы код для обработки платежа
        # Для демонстрации просто добавим звезды пользователю
        new_balance = db.update_balance(message.from_user.id, stars)
        
        # Отправляем подтверждение
        bot.send_message(
            message.chat.id,
            f"✅ <b>Платеж успешно обработан!</b>\n\n"
            f"Добавлено: {stars} звезд\n"
            f"Текущий баланс: {new_balance} звезд (≈ {new_balance/50:.2f}$)",
            parse_mode="html"
        )
        
    except ValueError:
        bot.send_message(
            message.chat.id,
            "❌ Неверный формат числа. Пожалуйста, введите целое число."
        )
    except Exception as e:
        print(f"Ошибка при обработке команды /add_stars: {e}")
        bot.send_message(
            message.chat.id,
            "❌ Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."
        )

# Обработчик для веб-приложения (получение данных о покупке)
@bot.message_handler(content_types=['web_app_data'])
def web_app_data(message):
    try:
        # Получаем данные от веб-приложения
        data = message.web_app_data.data
        
        # Предполагаем, что данные приходят в формате "subscription_type:duration"
        # Например: "full:3" для полной подписки на 3 месяца
        subscription_info = data.split(':')
        
        if len(subscription_info) == 2:
            subscription_type = subscription_info[0]  # 'full', 'basic', или 'ad_free'
            duration = int(subscription_info[1])      # количество месяцев
            
            # Получаем стоимость подписки в звездах
            stars_cost = 0
            if subscription_type == 'full':
                if duration == 1:
                    stars_cost = 350  # 7$ * 50 = 350 звезд
                elif duration == 3:
                    stars_cost = 900  # 18$ * 50 = 900 звезд
                elif duration == 6:
                    stars_cost = 1500  # 30$ * 50 = 1500 звезд
                elif duration == 12:
                    stars_cost = 2750  # 55$ * 50 = 2750 звезд
            elif subscription_type == 'basic':
                if duration == 1:
                    stars_cost = 250  # 5$ * 50 = 250 звезд
                elif duration == 3:
                    stars_cost = 650  # 13$ * 50 = 650 звезд
                elif duration == 6:
                    stars_cost = 1200  # 24$ * 50 = 1200 звезд
                elif duration == 12:
                    stars_cost = 2000  # 40$ * 50 = 2000 звезд
            elif subscription_type == 'ad_free':
                if duration == 0:  # Навсегда
                    stars_cost = 1000  # 20$ * 50 = 1000 звезд
                elif duration == 1:
                    stars_cost = 100  # 2$ * 50 = 100 звезд
                elif duration == 3:
                    stars_cost = 200  # 4$ * 50 = 200 звезд
                elif duration == 6:
                    stars_cost = 300  # 6$ * 50 = 300 звезд
            
            # Проверяем, достаточно ли у пользователя звезд
            user_balance = db.get_balance(message.from_user.id)
            
            if user_balance < stars_cost:
                bot.send_message(
                    message.chat.id,
                    f"❌ <b>Недостаточно звезд для покупки!</b>\n\n"
                    f"Стоимость: {stars_cost} звезд\n"
                    f"Ваш баланс: {user_balance} звезд\n\n"
                    f"Используйте команду /donate для пополнения баланса.",
                    parse_mode="html"
                )
                return
            
            # Списываем звезды с баланса пользователя
            db.update_balance(message.from_user.id, -stars_cost)
            
            # Добавляем подписку в базу данных
            db.add_subscription(message.from_user.id, subscription_type, duration)
            
            # Отправляем подтверждение пользователю
            if subscription_type == 'full':
                sub_name = "Полная подписка"
            elif subscription_type == 'basic':
                sub_name = "Базовая подписка"
            elif subscription_type == 'ad_free':
                sub_name = "Отключение рекламы"
            else:
                sub_name = "Подписка"
            
            if duration > 0:
                bot.send_message(
                    message.chat.id,
                    f"✅ {sub_name} успешно оформлена на {duration} месяцев!\n\n"
                    f"Списано: {stars_cost} звезд\n"
                    f"Текущий баланс: {user_balance - stars_cost} звезд\n\n"
                    "Используйте /my_subscription для просмотра информации о подписке."
                )
            else:
                bot.send_message(
                    message.chat.id,
                    f"✅ {sub_name} успешно оформлена навсегда!\n\n"
                    f"Списано: {stars_cost} звезд\n"
                    f"Текущий баланс: {user_balance - stars_cost} звезд\n\n"
                    "Используйте /my_subscription для просмотра информации о подписке."
                )
        else:
            bot.send_message(
                message.chat.id,
                "❌ Произошла ошибка при обработке данных о подписке. Пожалуйста, попробуйте еще раз."
            )
    except Exception as e:
        print(f"Ошибка при обработке данных веб-приложения: {e}")
        bot.send_message(
            message.chat.id,
            "❌ Произошла ошибка при обработке данных. Пожалуйста, попробуйте еще раз или обратитесь в поддержку."
        )

# Функция для синхронизации данных с веб-сайтом
def sync_with_website(user_id, website_data):
    """
    Синхронизирует данные пользователя с веб-сайтом
    
    Args:
        user_id: ID пользователя в Telegram
        website_data: Данные с веб-сайта (словарь)
    """
    try:
        # Обновляем дату регистрации на сайте
        if 'website_reg_date' in website_data:
            db.update_website_reg_date(user_id, website_data['website_reg_date'])
        
        # Обновляем подписки, если они есть в данных с сайта
        if 'subscriptions' in website_data:
            for sub in website_data['subscriptions']:
                if 'type' in sub and 'duration' in sub:
                    db.add_subscription(user_id, sub['type'], sub['duration'])
    except Exception as e:
        print(f"Ошибка при синхронизации данных с веб-сайтом: {e}")

# Периодическая очистка истекших подписок
# Эту функцию можно вызывать по расписанию, например, с помощью threading.Timer или APScheduler
def clean_expired_subscriptions_task():
    db.clean_expired_subscriptions()

# Запуск бота
if __name__ == "__main__":
    # Очищаем истекшие подписки при запуске
    clean_expired_subscriptions_task()
    
    # Запускаем бота
    bot.infinity_polling()