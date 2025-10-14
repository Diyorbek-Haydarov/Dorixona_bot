"""
Voice message retrieval utility
"""

import logging
import re
from typing import Optional
from aiogram import Bot
from aiogram.types import Message
from ..config import PRIVATE_CHANNEL_ID

logger = logging.getLogger(__name__)

def extract_message_id_from_link(message_link: str) -> Optional[int]:
    """
    Extract message ID from Telegram message link
    Expected format: https://t.me/channel_name/123 or https://t.me/c/channel_id/123
    """
    try:
        # Pattern for t.me links
        pattern = r'https://t\.me/(?:c/)?([^/]+)/(\d+)'
        match = re.search(pattern, message_link)
        
        if match:
            return int(match.group(2))
        
        # Pattern for direct message ID (fallback)
        if message_link.isdigit():
            return int(message_link)
            
        return None
        
    except (ValueError, AttributeError) as e:
        logger.error(f"Error extracting message ID from link {message_link}: {e}")
        return None

async def get_voice_from_channel(bot: Bot, message_link: str) -> Optional[str]:
    """
    Retrieve voice message from channel using message link
    Returns the voice file_id if successful, None otherwise
    """
    try:
        if not PRIVATE_CHANNEL_ID:
            logger.error("PRIVATE_CHANNEL_ID not configured")
            return None
            
        # Extract message ID from link
        message_id = extract_message_id_from_link(message_link)
        if not message_id:
            logger.error(f"Could not extract message ID from link: {message_link}")
            return None
        
        # Parse the channel username/ID from the link
        channel_pattern = r'https://t\.me/(?:c/)?([^/]+)'
        channel_match = re.search(channel_pattern, message_link)
        
        if not channel_match:
            logger.error(f"Could not extract channel from link: {message_link}")
            return None
            
        channel_identifier = channel_match.group(1)
        
        try:
            # Try to get the message using the channel identifier and message ID
            # Convert channel identifier to proper format
            if channel_identifier.isdigit() or channel_identifier.startswith('-'):
                # It's a channel ID
                chat_id = int(channel_identifier)
            else:
                # It's a channel username
                chat_id = f"@{channel_identifier}"
            
            # Get the message from the channel
            # Note: This requires the bot to be an admin in the channel
            # and have permission to read messages
            try:
                # Use the Telegram API to get the message
                # This is a simplified approach - you might need to use
                # a different method depending on your bot's permissions
                
                # For now, we'll use a workaround by trying to forward the message
                # This requires the bot to have forward permissions
                logger.info(f"Attempting to retrieve message {message_id} from channel {chat_id}")
                
                # Alternative: Use the message link to create a forward
                # This is a placeholder implementation
                # In practice, you would need to implement proper message retrieval
                
                # For demonstration, we'll return a placeholder
                # Replace this with actual implementation
                return f"voice_placeholder_{message_id}"
                
            except Exception as e:
                logger.error(f"Error retrieving message from channel: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing channel identifier: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Error in get_voice_from_channel: {e}")
        return None

async def send_voice_from_link(bot: Bot, chat_id: int, message_link: str) -> bool:
    """
    Send voice message to user by retrieving it from channel using message link
    """
    try:
        # Get voice file_id from channel
        voice_file_id = await get_voice_from_channel(bot, message_link)
        
        if not voice_file_id:
            logger.error(f"Could not retrieve voice from link: {message_link}")
            return False
            
        # Send voice message
        await bot.send_voice(chat_id=chat_id, voice=voice_file_id)
        return True
        
    except Exception as e:
        logger.error(f"Error sending voice from link: {e}")
        return False
