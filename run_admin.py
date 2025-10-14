#!/usr/bin/env python3
"""
PharmaGuide Admin Panel Runner
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from admin.app import app

if __name__ == "__main__":
    try:
        print("🚀 Starting PharmaGuide Admin Panel...")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("👤 Default login: admin / admin123")
        print("⚠️  Remember to change the default password!")
        print()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Admin panel stopped by user")
    except Exception as e:
        print(f"❌ Error starting admin panel: {e}")
        sys.exit(1)
