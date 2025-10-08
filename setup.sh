#!/bin/bash

# PharmaGuide Bot Setup Script for Linux/Mac
# This script sets up the complete environment for the PharmaGuide Bot

set -e  # Exit on any error

echo "🚀 PharmaGuide Bot Setup Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is installed
print_status "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3.8+ is required but not installed"
    exit 1
fi

# Check if pip is installed
print_status "Checking pip..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 found"
else
    print_error "pip3 is required but not installed"
    exit 1
fi

# Create virtual environment
print_status "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip
print_success "pip upgraded"

# Install requirements
print_status "Installing Python packages..."
pip install -r requirements.txt
print_success "All packages installed"

# Create .env file if it doesn't exist
print_status "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_success ".env file created from template"
    print_warning "Please edit .env file with your bot token and other settings"
else
    print_warning ".env file already exists"
fi

# Initialize database
print_status "Initializing database..."
python -c "
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('.')))
from bot.database import db

async def init():
    await db.init_db()
    print('Database initialized successfully')

asyncio.run(init())
"
print_success "Database initialized"

# Create admin user
print_status "Creating admin user..."
python init_admin.py
print_success "Admin user created"

# Ask if user wants to add sample data
echo ""
read -p "Do you want to add sample data? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Adding sample data..."
    python sample_data.py
    print_success "Sample data added"
fi

# Create run scripts
print_status "Creating run scripts..."

# Bot run script
cat > run_bot.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python run_bot.py
EOF
chmod +x run_bot.sh

# Admin run script
cat > run_admin.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python run_admin.py
EOF
chmod +x run_admin.sh

print_success "Run scripts created"

# Final instructions
echo ""
echo "🎉 Setup completed successfully!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your bot token and settings"
echo "2. Start the bot: ./run_bot.sh"
echo "3. Start admin panel: ./run_admin.sh"
echo "4. Open admin panel: http://localhost:5000"
echo ""
echo "Default admin credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "⚠️  Remember to change the default admin password!"
echo ""
echo "For help, check README.md or QUICKSTART.md"
echo ""
print_success "Setup complete! 🚀"
