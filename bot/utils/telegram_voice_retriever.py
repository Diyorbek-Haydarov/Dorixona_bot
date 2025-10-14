"""
Advanced Telegram voice message retrieval utility
This implementation uses proper Telegram API methods to retrieve voice messages
"""

import logging
import re
from typing import Optional
from aiogram import Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from ..config import PRIVATE_CHANNEL_ID

logger = logging.getLogger(__name__)

def extract_message_info_from_link(message_link: str) -> Optional[tuple]:
    """
    Extract channel and message ID from Telegram message link
    Returns (channel_identifier, message_id) or None
    """
    try:
        # Pattern for t.me links: https://t.me/channel_name/123 or https://t.me/c/channel_id/123
        pattern = r'https://t\.me/(?:c/)?([^/]+)/(\d+)'
        match = re.search(pattern, message_link)
        
        if match:
            channel_identifier = match.group(1)
            message_id = int(match.group(2))
            return channel_identifier, message_id
        
        return None
        
    except (ValueError, AttributeError) as e:
        logger.error(f"Error extracting info from link {message_link}: {e}")
        return None

async def get_voice_file_id_from_channel(bot: Bot, message_link: str) -> Optional[str]:
    """
    Retrieve voice file_id from channel using message link
    Returns the voice file_id if successful, None otherwise
    """
    try:
        # Extract channel and message info
        info = extract_message_info_from_link(message_link)
        if not info:
            logger.error(f"Could not extract info from link: {message_link}")
            return None
            
        channel_identifier, message_id = info
        
        # Convert channel identifier to proper format
        if channel_identifier.isdigit() or channel_identifier.startswith('-'):
            # It's a channel ID
            chat_id = int(channel_identifier)
        else:
            # It's a channel username
            chat_id = f"@{channel_identifier}"
        
        try:
            # Try to get the message from the channel
            # This requires the bot to have access to the channel
            message = await bot.forward_message(
                chat_id=chat_id,  # Forward to the same chat (this is a workaround)
                from_chat_id=chat_id,
                message_id=message_id
            )
            
            # Check if the message has a voice
            if message.voice:
                return message.voice.file_id
            else:
                logger.warning(f"Message {message_id} does not contain a voice")
                return None
                
        except TelegramForbiddenError:
            logger.error(f"Bot does not have permission to access channel {chat_id}")
            return None
        except TelegramBadRequest as e:
            logger.error(f"Bad request when accessing message {message_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving message {message_id} from channel {chat_id}: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Error in get_voice_file_id_from_channel: {e}")
        return None

async def send_voice_from_channel_link(bot: Bot, chat_id: int, message_link: str) -> bool:
    """
    Send voice message to user by retrieving it from channel using message link
    """
    try:
        # Get voice file_id from channel
        voice_file_id = await get_voice_file_id_from_channel(bot, message_link)
        
        if not voice_file_id:
            logger.error(f"Could not retrieve voice from link: {message_link}")
            return False
            
        # Send voice message
        await bot.send_voice(chat_id=chat_id, voice=voice_file_id)
        return True
        
    except Exception as e:
        logger.error(f"Error sending voice from link: {e}")
        return False

# Alternative implementation using direct message access
async def get_voice_directly(bot: Bot, message_link: str) -> Optional[str]:
    """
    Alternative method to get voice directly from message link
    This method tries to access the message directly without forwarding
    """
    try:
        info = extract_message_info_from_link(message_link)
        if not info:
            return None
            
        channel_identifier, message_id = info
        
        # Convert channel identifier
        if channel_identifier.isdigit() or channel_identifier.startswith('-'):
            chat_id = int(channel_identifier)
        else:
            chat_id = f"@{channel_identifier}"
        
        # Try to get message content directly
        # This is a more direct approach but requires specific bot permissions
        try:
            # Use a temporary chat to get the message
            # This is a workaround since direct message access is limited
            temp_chat_id = chat_id  # Use the same chat
            
            # Try to get the message by sending a copy to a temporary location
            # This is a creative workaround for the API limitations
            message = await bot.copy_message(
                chat_id=temp_chat_id,
                from_chat_id=chat_id,
                message_id=message_id
            )
            
            if message.voice:
                return message.voice.file_id
            else:
                logger.warning(f"Message {message_id} does not contain a voice")
                return None
                
        except Exception as e:
            logger.error(f"Error in direct message access: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Error in get_voice_directly: {e}")
        return None
