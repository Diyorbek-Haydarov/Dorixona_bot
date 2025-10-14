"""
Database operations for PharmaGuide Bot
"""

import aiosqlite
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import hashlib
from .config import DATABASE_URL

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "pharma_bot.db"):
        self.db_path = db_path
    
    async def init_db(self):
        """Initialize database with all required tables"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Users table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        telegram_id INTEGER UNIQUE NOT NULL,
                        username TEXT,
                        first_name TEXT,
                        language_code TEXT DEFAULT 'uz_latin',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Medicines table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS medicines (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_latin TEXT NOT NULL,
                        name_cyrillic TEXT NOT NULL,
                        description_latin TEXT,
                        description_cyrillic TEXT,
                        composition_latin TEXT,
                        composition_cyrillic TEXT,
                        usage_latin TEXT,
                        usage_cyrillic TEXT,
                        side_effects_latin TEXT,
                        side_effects_cyrillic TEXT,
                        voice_message_link TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # First aid table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS first_aid (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title_latin TEXT NOT NULL,
                        title_cyrillic TEXT NOT NULL,
                        content_latin TEXT NOT NULL,
                        content_cyrillic TEXT NOT NULL,
                        category TEXT DEFAULT 'general',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Admin users table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS admin_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP
                    )
                """)
                
                # Bot statistics table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS bot_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE UNIQUE NOT NULL,
                        total_users INTEGER DEFAULT 0,
                        active_users INTEGER DEFAULT 0,
                        searches_count INTEGER DEFAULT 0,
                        medicines_viewed INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes for better performance
                await db.execute("CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id)")
                await db.execute("CREATE INDEX IF NOT EXISTS idx_medicines_name_latin ON medicines(name_latin)")
                await db.execute("CREATE INDEX IF NOT EXISTS idx_medicines_name_cyrillic ON medicines(name_cyrillic)")
                await db.execute("CREATE INDEX IF NOT EXISTS idx_first_aid_category ON first_aid(category)")
                await db.execute("CREATE INDEX IF NOT EXISTS idx_bot_stats_date ON bot_stats(date)")
                
                await db.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    async def add_user(self, telegram_id: int, username: str = None, first_name: str = None) -> bool:
        """Add or update user information"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                # Check if user exists
                cursor = await db.execute(
                    "SELECT id FROM users WHERE telegram_id = ?", 
                    (telegram_id,)
                )
                user = await cursor.fetchone()
                
                if user:
                    # Update last activity
                    await db.execute(
                        "UPDATE users SET last_activity = CURRENT_TIMESTAMP WHERE telegram_id = ?",
                        (telegram_id,)
                    )
                else:
                    # Add new user
                    await db.execute(
                        """INSERT INTO users (telegram_id, username, first_name) 
                           VALUES (?, ?, ?)""",
                        (telegram_id, username, first_name)
                    )
                
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            return False
    
    async def get_user_language(self, telegram_id: int) -> str:
        """Get user's preferred language"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT language_code FROM users WHERE telegram_id = ?",
                    (telegram_id,)
                )
                user = await cursor.fetchone()
                return user['language_code'] if user else 'uz_latin'
                
        except Exception as e:
            logger.error(f"Error getting user language: {e}")
            return 'uz_latin'
    
    async def set_user_language(self, telegram_id: int, language_code: str) -> bool:
        """Set user's preferred language"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "UPDATE users SET language_code = ?, last_activity = CURRENT_TIMESTAMP WHERE telegram_id = ?",
                    (language_code, telegram_id)
                )
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error setting user language: {e}")
            return False
    
    async def search_medicine(self, query: str, language_code: str) -> Optional[Dict[str, Any]]:
        """Search for medicine by name - searches in both Latin and Cyrillic fields"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                # Search in both Latin and Cyrillic fields for better results
                # Also make the search case-insensitive
                cursor = await db.execute(
                    """SELECT * FROM medicines 
                       WHERE LOWER(name_latin) LIKE LOWER(?) 
                          OR LOWER(name_cyrillic) LIKE LOWER(?) 
                       LIMIT 1""",
                    (f"%{query}%", f"%{query}%")
                )
                medicine = await cursor.fetchone()
                
                if medicine:
                    return dict(medicine)
                
                # If no exact match, try partial matching with individual words
                words = query.lower().split()
                if len(words) > 1:
                    for word in words:
                        if len(word) > 2:  # Only search words longer than 2 characters
                            cursor = await db.execute(
                                """SELECT * FROM medicines 
                                   WHERE LOWER(name_latin) LIKE LOWER(?) 
                                      OR LOWER(name_cyrillic) LIKE LOWER(?) 
                                   LIMIT 1""",
                                (f"%{word}%", f"%{word}%")
                            )
                            medicine = await cursor.fetchone()
                            if medicine:
                                return dict(medicine)
                
                return None
                
        except Exception as e:
            logger.error(f"Error searching medicine: {e}")
            return None
    
    async def get_medicines_paginated(self, page: int = 1, per_page: int = 10) -> List[Dict[str, Any]]:
        """Get paginated list of medicines"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                offset = (page - 1) * per_page
                
                cursor = await db.execute(
                    "SELECT * FROM medicines ORDER BY name_latin LIMIT ? OFFSET ?",
                    (per_page, offset)
                )
                medicines = await cursor.fetchall()
                
                return [dict(medicine) for medicine in medicines]
                
        except Exception as e:
            logger.error(f"Error getting medicines: {e}")
            return []
    
    async def get_medicines_count(self) -> int:
        """Get total count of medicines"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("SELECT COUNT(*) as count FROM medicines")
                result = await cursor.fetchone()
                return result[0] if result else 0
                
        except Exception as e:
            logger.error(f"Error getting medicines count: {e}")
            return 0
    
    async def get_first_aid_articles(self, category: str = 'general') -> List[Dict[str, Any]]:
        """Get first aid articles by category"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT * FROM first_aid WHERE category = ? ORDER BY title_latin",
                    (category,)
                )
                articles = await cursor.fetchall()
                
                return [dict(article) for article in articles]
                
        except Exception as e:
            logger.error(f"Error getting first aid articles: {e}")
            return []
    
    async def increment_search_count(self):
        """Increment search counter in statistics"""
        try:
            today = datetime.now().date()
            async with aiosqlite.connect(self.db_path) as db:
                # Try to update existing record
                cursor = await db.execute(
                    "UPDATE bot_stats SET searches_count = searches_count + 1 WHERE date = ?",
                    (today,)
                )
                
                if cursor.rowcount == 0:
                    # Insert new record if none exists for today
                    await db.execute(
                        "INSERT INTO bot_stats (date, searches_count) VALUES (?, 1)",
                        (today,)
                    )
                
                await db.commit()
                
        except Exception as e:
            logger.error(f"Error incrementing search count: {e}")
    
    async def increment_medicine_view_count(self):
        """Increment medicine view counter in statistics"""
        try:
            today = datetime.now().date()
            async with aiosqlite.connect(self.db_path) as db:
                # Try to update existing record
                cursor = await db.execute(
                    "UPDATE bot_stats SET medicines_viewed = medicines_viewed + 1 WHERE date = ?",
                    (today,)
                )
                
                if cursor.rowcount == 0:
                    # Insert new record if none exists for today
                    await db.execute(
                        "INSERT INTO bot_stats (date, medicines_viewed) VALUES (?, 1)",
                        (today,)
                    )
                
                await db.commit()
                
        except Exception as e:
            logger.error(f"Error incrementing medicine view count: {e}")
    
    # Admin methods
    async def create_admin_user(self, username: str, password: str) -> bool:
        """Create admin user with hashed password"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT OR REPLACE INTO admin_users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash)
                )
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error creating admin user: {e}")
            return False
    
    async def verify_admin_user(self, username: str, password: str) -> bool:
        """Verify admin user credentials"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    "SELECT id FROM admin_users WHERE username = ? AND password_hash = ?",
                    (username, password_hash)
                )
                user = await cursor.fetchone()
                
                if user:
                    # Update last login
                    await db.execute(
                        "UPDATE admin_users SET last_login = CURRENT_TIMESTAMP WHERE username = ?",
                        (username,)
                    )
                    await db.commit()
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"Error verifying admin user: {e}")
            return False
    
    async def add_medicine(self, medicine_data: Dict[str, Any]) -> bool:
        """Add new medicine to database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """INSERT INTO medicines (
                        name_latin, name_cyrillic, description_latin, description_cyrillic,
                        composition_latin, composition_cyrillic, usage_latin, usage_cyrillic,
                        side_effects_latin, side_effects_cyrillic, voice_message_link
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        medicine_data.get('name_latin', ''),
                        medicine_data.get('name_cyrillic', ''),
                        medicine_data.get('description_latin', ''),
                        medicine_data.get('description_cyrillic', ''),
                        medicine_data.get('composition_latin', ''),
                        medicine_data.get('composition_cyrillic', ''),
                        medicine_data.get('usage_latin', ''),
                        medicine_data.get('usage_cyrillic', ''),
                        medicine_data.get('side_effects_latin', ''),
                        medicine_data.get('side_effects_cyrillic', ''),
                        medicine_data.get('voice_message_link', '')
                    )
                )
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error adding medicine: {e}")
            return False
    
    async def update_medicine(self, medicine_id: int, medicine_data: Dict[str, Any]) -> bool:
        """Update existing medicine"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """UPDATE medicines SET 
                        name_latin = ?, name_cyrillic = ?, description_latin = ?, description_cyrillic = ?,
                        composition_latin = ?, composition_cyrillic = ?, usage_latin = ?, usage_cyrillic = ?,
                        side_effects_latin = ?, side_effects_cyrillic = ?, voice_message_link = ?,
                        updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?""",
                    (
                        medicine_data.get('name_latin', ''),
                        medicine_data.get('name_cyrillic', ''),
                        medicine_data.get('description_latin', ''),
                        medicine_data.get('description_cyrillic', ''),
                        medicine_data.get('composition_latin', ''),
                        medicine_data.get('composition_cyrillic', ''),
                        medicine_data.get('usage_latin', ''),
                        medicine_data.get('usage_cyrillic', ''),
                        medicine_data.get('side_effects_latin', ''),
                        medicine_data.get('side_effects_cyrillic', ''),
                        medicine_data.get('voice_message_link', ''),
                        medicine_id
                    )
                )
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error updating medicine: {e}")
            return False
    
    async def delete_medicine(self, medicine_id: int) -> bool:
        """Delete medicine from database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("DELETE FROM medicines WHERE id = ?", (medicine_id,))
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error deleting medicine: {e}")
            return False
    
    async def get_medicine_by_id(self, medicine_id: int) -> Optional[Dict[str, Any]]:
        """Get medicine by ID"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("SELECT * FROM medicines WHERE id = ?", (medicine_id,))
                medicine = await cursor.fetchone()
                return dict(medicine) if medicine else None
                
        except Exception as e:
            logger.error(f"Error getting medicine by ID: {e}")
            return None
    
    async def add_first_aid_article(self, article_data: Dict[str, Any]) -> bool:
        """Add new first aid article"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """INSERT INTO first_aid (title_latin, title_cyrillic, content_latin, content_cyrillic, category)
                       VALUES (?, ?, ?, ?, ?)""",
                    (
                        article_data.get('title_latin', ''),
                        article_data.get('title_cyrillic', ''),
                        article_data.get('content_latin', ''),
                        article_data.get('content_cyrillic', ''),
                        article_data.get('category', 'general')
                    )
                )
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error adding first aid article: {e}")
            return False
    
    async def update_first_aid_article(self, article_id: int, article_data: Dict[str, Any]) -> bool:
        """Update existing first aid article"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """UPDATE first_aid SET 
                        title_latin = ?, title_cyrillic = ?, content_latin = ?, content_cyrillic = ?,
                        category = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?""",
                    (
                        article_data.get('title_latin', ''),
                        article_data.get('title_cyrillic', ''),
                        article_data.get('content_latin', ''),
                        article_data.get('content_cyrillic', ''),
                        article_data.get('category', 'general'),
                        article_id
                    )
                )
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error updating first aid article: {e}")
            return False
    
    async def delete_first_aid_article(self, article_id: int) -> bool:
        """Delete first aid article"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("DELETE FROM first_aid WHERE id = ?", (article_id,))
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error deleting first aid article: {e}")
            return False
    
    async def get_first_aid_article_by_id(self, article_id: int) -> Optional[Dict[str, Any]]:
        """Get first aid article by ID"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("SELECT * FROM first_aid WHERE id = ?", (article_id,))
                article = await cursor.fetchone()
                return dict(article) if article else None
                
        except Exception as e:
            logger.error(f"Error getting first aid article by ID: {e}")
            return None

    async def get_bot_statistics(self) -> Dict[str, Any]:
        """Get bot usage statistics"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                # Get total users
                cursor = await db.execute("SELECT COUNT(*) as count FROM users")
                total_users = (await cursor.fetchone())[0]
                
                # Get active users (last 7 days)
                cursor = await db.execute(
                    "SELECT COUNT(*) as count FROM users WHERE last_activity >= datetime('now', '-7 days')"
                )
                active_users = (await cursor.fetchone())[0]
                
                # Get total medicines
                cursor = await db.execute("SELECT COUNT(*) as count FROM medicines")
                total_medicines = (await cursor.fetchone())[0]
                
                # Get recent users
                cursor = await db.execute(
                    "SELECT * FROM users ORDER BY created_at DESC LIMIT 10"
                )
                recent_users = await cursor.fetchall()
                
                return {
                    'total_users': total_users,
                    'active_users': active_users,
                    'total_medicines': total_medicines,
                    'recent_users': [dict(user) for user in recent_users]
                }
                
        except Exception as e:
            logger.error(f"Error getting bot statistics: {e}")
            return {
                'total_users': 0,
                'active_users': 0,
                'total_medicines': 0,
                'recent_users': []
            }

# Global database instance
db = Database()
