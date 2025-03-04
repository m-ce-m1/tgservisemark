import sqlite3
import datetime

class Database:
    def __init__(self, db_file="users.db"):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.init_db()

    def connect(self):
        """Establish connection to the database"""
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def disconnect(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def init_db(self):
        """Initialize database tables if they don't exist"""
        self.connect()
        
        # Create users table
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            website_reg_date TEXT,
            bot_reg_date TEXT,
            has_subscription INTEGER DEFAULT 0,
            balance INTEGER DEFAULT 0
        )
        ''')
        
        # Create subscriptions table
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            user_id INTEGER PRIMARY KEY,
            full_subscription INTEGER DEFAULT 0,
            full_subscription_end TEXT,
            basic_subscription INTEGER DEFAULT 0,
            basic_subscription_end TEXT,
            ad_free INTEGER DEFAULT 0,
            ad_free_end TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')
        
        self.conn.commit()
        self.disconnect()

    def add_user(self, user_id, website_reg_date=None, bot_reg_date=None):
        """Add a new user to the database"""
        self.connect()
        
        # Set default dates if not provided
        if not bot_reg_date:
            bot_reg_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if user already exists
        self.conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        existing_user = self.conn.cursor().fetchone()
        
        if not existing_user:
            # Add new user
            self.conn.execute(
                "INSERT INTO users (user_id, website_reg_date, bot_reg_date, has_subscription, balance) VALUES (?, ?, ?, ?, ?)",
                (user_id, website_reg_date, bot_reg_date, 0, 0)
            )
            self.conn.commit()
        
        self.disconnect()
        return not bool(existing_user)  # Return True if new user was added

    def update_website_reg_date(self, user_id, website_reg_date):
        """Update the website registration date for a user"""
        self.connect()
        self.conn.execute(
            "UPDATE users SET website_reg_date = ? WHERE user_id = ?",
            (website_reg_date, user_id)
        )
        self.conn.commit()
        self.disconnect()

    def get_user(self, user_id):
        """Get user information from the database"""
        self.connect()
        self.conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = self.conn.cursor().fetchone()
        self.disconnect()
        
        if user:
            return {
                "user_id": user['user_id'],
                "website_reg_date": user['website_reg_date'],
                "bot_reg_date": user['bot_reg_date'],
                "has_subscription": bool(user['has_subscription']),
                "balance": user['balance']
            }
        return None

    def add_subscription(self, user_id, subscription_type, duration_months):
        """Add or update a subscription for a user
        
        Args:
            user_id: The user's ID
            subscription_type: 'full', 'basic', or 'ad_free'
            duration_months: Number of months (1, 3, 6, 12) or 0 for permanent ad_free
        """
        self.connect()
        
        # Check if user exists, if not add them
        user = self.get_user(user_id)
        if not user:
            self.add_user(user_id)
        
        # Calculate end date
        if duration_months > 0:
            end_date = (datetime.datetime.now() + datetime.timedelta(days=30*duration_months)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            end_date = None  # For permanent ad_free subscription
        
        # Check if subscription record exists
        self.conn.execute("SELECT user_id FROM subscriptions WHERE user_id = ?", (user_id,))
        subscription_exists = self.conn.cursor().fetchone()
        
        if subscription_exists:
            # Update existing subscription
            if subscription_type == 'full':
                self.conn.execute(
                    "UPDATE subscriptions SET full_subscription = ?, full_subscription_end = ? WHERE user_id = ?",
                    (duration_months, end_date, user_id)
                )
            elif subscription_type == 'basic':
                self.conn.execute(
                    "UPDATE subscriptions SET basic_subscription = ?, basic_subscription_end = ? WHERE user_id = ?",
                    (duration_months, end_date, user_id)
                )
            elif subscription_type == 'ad_free':
                self.conn.execute(
                    "UPDATE subscriptions SET ad_free = ?, ad_free_end = ? WHERE user_id = ?",
                    (duration_months, end_date, user_id)
                )
        else:
            # Create new subscription record
            if subscription_type == 'full':
                self.conn.execute(
                    "INSERT INTO subscriptions (user_id, full_subscription, full_subscription_end) VALUES (?, ?, ?)",
                    (user_id, duration_months, end_date)
                )
            elif subscription_type == 'basic':
                self.conn.execute(
                    "INSERT INTO subscriptions (user_id, basic_subscription, basic_subscription_end) VALUES (?, ?, ?)",
                    (user_id, duration_months, end_date)
                )
            elif subscription_type == 'ad_free':
                self.conn.execute(
                    "INSERT INTO subscriptions (user_id, ad_free, ad_free_end) VALUES (?, ?, ?)",
                    (user_id, duration_months, end_date)
                )
        
        # Update user's subscription status
        self.conn.execute(
            "UPDATE users SET has_subscription = 1 WHERE user_id = ?",
            (user_id,)
        )
        
        self.conn.commit()
        self.disconnect()

    def get_subscription(self, user_id):
        """Get subscription information for a user"""
        self.connect()
        self.conn.execute("SELECT * FROM subscriptions WHERE user_id = ?", (user_id,))
        subscription = self.conn.cursor().fetchone()
        self.disconnect()
        
        if subscription:
            return {
                "user_id": subscription['user_id'],
                "full_subscription": subscription['full_subscription'],
                "full_subscription_end": subscription['full_subscription_end'],
                "basic_subscription": subscription['basic_subscription'],
                "basic_subscription_end": subscription['basic_subscription_end'],
                "ad_free": subscription['ad_free'],
                "ad_free_end": subscription['ad_free_end']
            }
        return None

    def check_active_subscription(self, user_id):
        """Check if user has any active subscription"""
        self.connect()
        
        # Get current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Check for active subscriptions
        self.conn.execute("""
            SELECT 
                (full_subscription > 0 AND (full_subscription_end > ? OR full_subscription_end IS NULL)) OR
                (basic_subscription > 0 AND (basic_subscription_end > ? OR basic_subscription_end IS NULL)) OR
                (ad_free > 0 AND (ad_free_end > ? OR ad_free_end IS NULL))
            FROM subscriptions 
            WHERE user_id = ?
        """, (current_date, current_date, current_date, user_id))
        
        result = self.conn.cursor().fetchone()
        self.disconnect()
        
        return bool(result and result[0])

    def clean_expired_subscriptions(self):
        """Remove expired subscriptions"""
        self.connect()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update full subscriptions
        self.conn.execute(
            "UPDATE subscriptions SET full_subscription = 0 WHERE full_subscription_end < ?",
            (current_date,)
        )
        
        # Update basic subscriptions
        self.conn.execute(
            "UPDATE subscriptions SET basic_subscription = 0 WHERE basic_subscription_end < ?",
            (current_date,)
        )
        
        # Update ad_free subscriptions (only those with end dates)
        self.conn.execute(
            "UPDATE subscriptions SET ad_free = 0 WHERE ad_free_end IS NOT NULL AND ad_free_end < ?",
            (current_date,)
        )
        
        # Update user subscription status
        self.conn.execute("""
            UPDATE users SET has_subscription = 0
            WHERE user_id IN (
                SELECT user_id FROM subscriptions
                WHERE full_subscription = 0 
                AND basic_subscription = 0 
                AND ad_free = 0
            )
        """)
        
        self.conn.commit()
        self.disconnect()

    def sync_website_user(self, user_id, website_reg_date):
        """Sync user data from website"""
        self.connect()
        
        # Check if user exists
        user = self.get_user(user_id)
        if user:
            # Update existing user
            self.conn.execute(
                "UPDATE users SET website_reg_date = ? WHERE user_id = ?",
                (website_reg_date, user_id)
            )
        else:
            # Add new user
            self.add_user(user_id, website_reg_date)
        
        self.conn.commit()
        self.disconnect()

    def update_balance(self, user_id, amount):
        """Update user balance
        
        Args:
            user_id: The user's ID
            amount: Amount to add to balance (can be negative)
        
        Returns:
            New balance
        """
        self.connect()
        
        # Check if user exists
        user = self.get_user(user_id)
        if not user:
            self.add_user(user_id)
            current_balance = 0
        else:
            current_balance = user['balance']
        
        # Update balance
        new_balance = current_balance + amount
        if new_balance < 0:
            new_balance = 0
        
        self.conn.execute(
            "UPDATE users SET balance = ? WHERE user_id = ?",
            (new_balance, user_id)
        )
        
        self.conn.commit()
        self.disconnect()
        
        return new_balance

    def get_balance(self, user_id):
        """Get user balance
        
        Args:
            user_id: The user's ID
        
        Returns:
            Current balance or 0 if user not found
        """
        user = self.get_user(user_id)
        if user:
            return user['balance']
        return 0