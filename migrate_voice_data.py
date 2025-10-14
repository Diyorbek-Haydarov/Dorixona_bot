#!/usr/bin/env python3
"""
Database migration script to update voice_file_id to voice_message_link
"""

import asyncio
import aiosqlite
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def migrate_voice_data():
    """Migrate voice_file_id column to voice_message_link"""
    try:
        async with aiosqlite.connect('pharma_bot.db') as db:
            # Check if voice_message_link column exists
            cursor = await db.execute("PRAGMA table_info(medicines)")
            columns = await cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            if 'voice_message_link' not in column_names:
                logger.info("Adding voice_message_link column...")
                await db.execute("ALTER TABLE medicines ADD COLUMN voice_message_link TEXT")
                await db.commit()
                logger.info("✅ voice_message_link column added")
            else:
                logger.info("✅ voice_message_link column already exists")
            
            # Check if voice_file_id column exists and migrate data
            if 'voice_file_id' in column_names:
                logger.info("Migrating data from voice_file_id to voice_message_link...")
                
                # Copy data from voice_file_id to voice_message_link where voice_message_link is empty
                cursor = await db.execute("""
                    UPDATE medicines 
                    SET voice_message_link = voice_file_id 
                    WHERE voice_file_id IS NOT NULL 
                    AND voice_file_id != '' 
                    AND (voice_message_link IS NULL OR voice_message_link = '')
                """)
                
                updated_rows = cursor.rowcount
                await db.commit()
                logger.info(f"✅ Migrated {updated_rows} records")
                
                # Optionally drop the old column (uncomment if you want to remove it)
                # await db.execute("ALTER TABLE medicines DROP COLUMN voice_file_id")
                # await db.commit()
                # logger.info("✅ Removed old voice_file_id column")
                
            else:
                logger.info("✅ No voice_file_id column found, migration not needed")
                
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(migrate_voice_data())
