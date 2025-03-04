import json
import sqlite3
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# API для получения данных о пользователе
@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    # Получаем информацию о подписках
    subscription = conn.execute('SELECT * FROM subscriptions WHERE user_id = ?', (user_id,)).fetchone()
    
    user_data = {
        'user_id': user['user_id'],
        'website_reg_date': user['website_reg_date'],
        'bot_reg_date': user['bot_reg_date'],
        'has_subscription': bool(user['has_subscription']),
        'balance': user['balance'],
        'subscriptions': None
    }
    
    if subscription:
        user_data['subscriptions'] = {
            'full_subscription': subscription['full_subscription'],
            'full_subscription_end': subscription['full_subscription_end'],
            'basic_subscription': subscription['basic_subscription'],
            'basic_subscription_end': subscription['basic_subscription_end'],
            'ad_free': subscription['ad_free'],
            'ad_free_end': subscription['ad_free_end']
        }
    
    conn.close()
    return jsonify(user_data)

# API для регистрации пользователя с веб-сайта
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    
    if not data or 'user_id' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user_id = data['user_id']
    website_reg_date = data.get('website_reg_date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    conn = get_db_connection()
    
    # Проверяем, существует ли пользователь
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    
    if user:
        # Обновляем существующего пользователя
        conn.execute('UPDATE users SET website_reg_date = ? WHERE user_id = ?', 
                    (website_reg_date, user_id))
    else:
        # Создаем нового пользователя
        conn.execute('INSERT INTO users (user_id, website_reg_date, bot_reg_date, has_subscription, balance) VALUES (?, ?, NULL, 0, 0)',
                    (user_id, website_reg_date))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'user_id': user_id})

# API для добавления подписки
@app.route('/api/subscription', methods=['POST'])
def add_subscription():
    data = request.json
    
    if not data or 'user_id' not in data or 'subscription_type' not in data or 'duration' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user_id = data['user_id']
    subscription_type = data['subscription_type']
    duration = int(data['duration'])
    
    # Проверяем корректность типа подписки
    if subscription_type not in ['full', 'basic', 'ad_free']:
        return jsonify({'error': 'Invalid subscription type'}), 400
    
    conn = get_db_connection()
    
    # Проверяем, существует ли пользователь
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    
    if not user:
        # Создаем пользователя, если он не существует
        website_reg_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute('INSERT INTO users (user_id, website_reg_date, bot_reg_date, has_subscription, balance) VALUES (?, ?, NULL, 1, 0)',
                    (user_id, website_reg_date))
    else:
        # Обновляем статус подписки
        conn.execute('UPDATE users SET has_subscription = 1 WHERE user_id = ?', (user_id,))
    
    # Рассчитываем дату окончания подписки
    if duration > 0:
        end_date = (datetime.datetime.now() + datetime.timedelta(days=30*duration)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        end_date = None  # Для постоянной подписки
    
    # Проверяем, есть ли уже запись о подписке
    subscription = conn.execute('SELECT * FROM subscriptions WHERE user_id = ?', (user_id,)).fetchone()
    
    if subscription:
        # Обновляем существующую подписку
        if subscription_type == 'full':
            conn.execute('UPDATE subscriptions SET full_subscription = ?, full_subscription_end = ? WHERE user_id = ?',
                        (duration, end_date, user_id))
        elif subscription_type == 'basic':
            conn.execute('UPDATE subscriptions SET basic_subscription = ?, basic_subscription_end = ? WHERE user_id = ?',
                        (duration, end_date, user_id))
        elif subscription_type == 'ad_free':
            conn.execute('UPDATE subscriptions SET ad_free = ?, ad_free_end = ? WHERE user_id = ?',
                        (duration, end_date, user_id))
    else:
        # Создаем новую запись о подписке
        if subscription_type == 'full':
            conn.execute('INSERT INTO subscriptions (user_id, full_subscription, full_subscription_end) VALUES (?, ?, ?)',
                        (user_id, duration, end_date))
        elif subscription_type == 'basic':
            conn.execute('INSERT INTO subscriptions (user_id, basic_subscription, basic_subscription_end) VALUES (?, ?, ?)',
                        (user_id, duration, end_date))
        elif subscription_type == 'ad_free':
            conn.execute('INSERT INTO subscriptions (user_id, ad_free, ad_free_end) VALUES (?, ?, ?)',
                        (user_id, duration, end_date))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'user_id': user_id, 'subscription_type': subscription_type, 'duration': duration})

# API для пополнения баланса
@app.route('/api/topup', methods=['POST'])
def topup_balance():
    data = request.json
    
    if not data or 'user_id' not in data or 'amount' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user_id = data['user_id']
    amount = int(data['amount'])  # Сумма в долларах
    stars = amount * 50  # Конвертация в звезды (1$ = 50 звезд)
    
    conn = get_db_connection()
    
    # Проверяем, существует ли пользователь
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    
    if not user:
        # Создаем пользователя, если он не существует
        website_reg_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute('INSERT INTO users (user_id, website_reg_date, bot_reg_date, has_subscription, balance) VALUES (?, ?, NULL, 0, ?)',
                    (user_id, website_reg_date, stars))
        new_balance = stars
    else:
        # Обновляем баланс пользователя
        current_balance = user['balance']
        new_balance = current_balance + stars
        conn.execute('UPDATE users SET balance = ? WHERE user_id = ?', (new_balance, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True, 
        'user_id': user_id, 
        'added_stars': stars,
        'new_balance': new_balance,
        'dollars_equivalent': new_balance / 50
    })

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, port=5000)