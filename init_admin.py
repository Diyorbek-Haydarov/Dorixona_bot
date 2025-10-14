#!/usr/bin/env python3
"""
Admin user initialization script
"""

import asyncio
import sys
import os
import getpass

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.database import db
from bot.config import ADMIN_USERNAME, ADMIN_PASSWORD

async def create_admin_user():
    """Create admin user"""
    print("🔐 PharmaGuide Bot - Admin User Setup")
    print("=====================================")
    print()
    
    # Initialize database
    await db.init_db()
    print("✅ Database initialized")
    
    # Get admin credentials
    print("Enter admin credentials:")
    username = ADMIN_USERNAME
    password = ADMIN_PASSWORD
    
    if not password:
        print("❌ Password cannot be empty")
        return
    
    # Create admin user
    success = await db.create_admin_user(username, password)
    
    if success:
        print(f"✅ Admin user '{username}' created successfully")
    else:
        print("❌ Failed to create admin user")
    
    print()
    print("You can now login to the admin panel with these credentials.")

if __name__ == "__main__":
    asyncio.run(create_admin_user())
