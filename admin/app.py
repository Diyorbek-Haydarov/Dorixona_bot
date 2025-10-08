"""
Flask admin panel application
"""

import asyncio
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import os
import sys

# Add parent directory to path to import bot modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.database import db
from bot.config import FLASK_SECRET_KEY, FLASK_ENV, AdminTexts

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = AdminTexts.LOGIN_REQUIRED

class AdminUser(UserMixin):
    """Admin user class for Flask-Login"""
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    """Load user for Flask-Login"""
    return AdminUser(username)

def run_async(coro):
    """Helper to run async functions in Flask"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@app.route('/')
@login_required
def dashboard():
    """Admin dashboard"""
    try:
        stats = run_async(db.get_bot_statistics())
        return render_template('dashboard.html', stats=stats)
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        flash("Error loading dashboard", "error")
        return render_template('dashboard.html', stats={})

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            # Verify credentials
            is_valid = run_async(db.verify_admin_user(username, password))
            
            if is_valid:
                user = AdminUser(username)
                login_user(user)
                flash(AdminTexts.LOGIN_SUCCESS, "success")
                return redirect(url_for('dashboard'))
            else:
                flash(AdminTexts.INVALID_CREDENTIALS, "error")
        else:
            flash("Please fill in all fields", "error")
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Admin logout"""
    logout_user()
    flash(AdminTexts.LOGOUT_SUCCESS, "success")
    return redirect(url_for('login'))

@app.route('/medicines')
@login_required
def medicines_list():
    """List all medicines"""
    try:
        medicines = run_async(db.get_medicines_paginated(page=1, per_page=100))
        return render_template('medicines_list.html', medicines=medicines)
    except Exception as e:
        logger.error(f"Error loading medicines: {e}")
        flash("Error loading medicines", "error")
        return render_template('medicines_list.html', medicines=[])

@app.route('/medicines/add', methods=['GET', 'POST'])
@login_required
def add_medicine():
    """Add new medicine"""
    if request.method == 'POST':
        try:
            medicine_data = {
                'name_latin': request.form.get('name_latin', ''),
                'name_cyrillic': request.form.get('name_cyrillic', ''),
                'description_latin': request.form.get('description_latin', ''),
                'description_cyrillic': request.form.get('description_cyrillic', ''),
                'composition_latin': request.form.get('composition_latin', ''),
                'composition_cyrillic': request.form.get('composition_cyrillic', ''),
                'usage_latin': request.form.get('usage_latin', ''),
                'usage_cyrillic': request.form.get('usage_cyrillic', ''),
                'side_effects_latin': request.form.get('side_effects_latin', ''),
                'side_effects_cyrillic': request.form.get('side_effects_cyrillic', ''),
                'voice_file_id': request.form.get('voice_file_id', '')
            }
            
            # Validate required fields
            if not medicine_data['name_latin'] or not medicine_data['name_cyrillic']:
                flash("Medicine name is required in both languages", "error")
                return render_template('medicine_form.html', medicine=medicine_data)
            
            success = run_async(db.add_medicine(medicine_data))
            
            if success:
                flash(AdminTexts.MEDICINE_ADDED, "success")
                return redirect(url_for('medicines_list'))
            else:
                flash("Error adding medicine", "error")
                
        except Exception as e:
            logger.error(f"Error adding medicine: {e}")
            flash("Error adding medicine", "error")
    
    return render_template('medicine_form.html', medicine={})

@app.route('/medicines/edit/<int:medicine_id>', methods=['GET', 'POST'])
@login_required
def edit_medicine(medicine_id):
    """Edit existing medicine"""
    try:
        medicine = run_async(db.get_medicine_by_id(medicine_id))
        
        if not medicine:
            flash("Medicine not found", "error")
            return redirect(url_for('medicines_list'))
        
        if request.method == 'POST':
            medicine_data = {
                'name_latin': request.form.get('name_latin', ''),
                'name_cyrillic': request.form.get('name_cyrillic', ''),
                'description_latin': request.form.get('description_latin', ''),
                'description_cyrillic': request.form.get('description_cyrillic', ''),
                'composition_latin': request.form.get('composition_latin', ''),
                'composition_cyrillic': request.form.get('composition_cyrillic', ''),
                'usage_latin': request.form.get('usage_latin', ''),
                'usage_cyrillic': request.form.get('usage_cyrillic', ''),
                'side_effects_latin': request.form.get('side_effects_latin', ''),
                'side_effects_cyrillic': request.form.get('side_effects_cyrillic', ''),
                'voice_file_id': request.form.get('voice_file_id', '')
            }
            
            # Validate required fields
            if not medicine_data['name_latin'] or not medicine_data['name_cyrillic']:
                flash("Medicine name is required in both languages", "error")
                return render_template('medicine_form.html', medicine=medicine_data)
            
            success = run_async(db.update_medicine(medicine_id, medicine_data))
            
            if success:
                flash(AdminTexts.MEDICINE_UPDATED, "success")
                return redirect(url_for('medicines_list'))
            else:
                flash("Error updating medicine", "error")
        
        return render_template('medicine_form.html', medicine=medicine)
        
    except Exception as e:
        logger.error(f"Error editing medicine: {e}")
        flash("Error loading medicine", "error")
        return redirect(url_for('medicines_list'))

@app.route('/medicines/delete/<int:medicine_id>', methods=['POST'])
@login_required
def delete_medicine(medicine_id):
    """Delete medicine"""
    try:
        success = run_async(db.delete_medicine(medicine_id))
        
        if success:
            flash(AdminTexts.MEDICINE_DELETED, "success")
        else:
            flash("Error deleting medicine", "error")
            
    except Exception as e:
        logger.error(f"Error deleting medicine: {e}")
        flash("Error deleting medicine", "error")
    
    return redirect(url_for('medicines_list'))

@app.route('/first_aid')
@login_required
def first_aid_list():
    """List all first aid articles"""
    try:
        articles = run_async(db.get_first_aid_articles())
        return render_template('first_aid_list.html', articles=articles)
    except Exception as e:
        logger.error(f"Error loading first aid articles: {e}")
        flash("Error loading first aid articles", "error")
        return render_template('first_aid_list.html', articles=[])

@app.route('/first_aid/add', methods=['GET', 'POST'])
@login_required
def add_first_aid():
    """Add new first aid article"""
    if request.method == 'POST':
        try:
            article_data = {
                'title_latin': request.form.get('title_latin', ''),
                'title_cyrillic': request.form.get('title_cyrillic', ''),
                'content_latin': request.form.get('content_latin', ''),
                'content_cyrillic': request.form.get('content_cyrillic', ''),
                'category': request.form.get('category', 'general')
            }
            
            # Validate required fields
            if not article_data['title_latin'] or not article_data['title_cyrillic']:
                flash("Article title is required in both languages", "error")
                return render_template('first_aid_form.html', article=article_data)
            
            if not article_data['content_latin'] or not article_data['content_cyrillic']:
                flash("Article content is required in both languages", "error")
                return render_template('first_aid_form.html', article=article_data)
            
            # Add article to database
            success = run_async(db.add_first_aid_article(article_data))
            
            if success:
                flash(AdminTexts.FIRST_AID_ADDED, "success")
                return redirect(url_for('first_aid_list'))
            else:
                flash("Error adding first aid article", "error")
                
        except Exception as e:
            logger.error(f"Error adding first aid article: {e}")
            flash("Error adding first aid article", "error")
    
    return render_template('first_aid_form.html', article={})

@app.route('/first_aid/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_first_aid(article_id):
    """Edit existing first aid article"""
    try:
        article = run_async(db.get_first_aid_article_by_id(article_id))
        
        if not article:
            flash("First aid article not found", "error")
            return redirect(url_for('first_aid_list'))
        
        if request.method == 'POST':
            article_data = {
                'title_latin': request.form.get('title_latin', ''),
                'title_cyrillic': request.form.get('title_cyrillic', ''),
                'content_latin': request.form.get('content_latin', ''),
                'content_cyrillic': request.form.get('content_cyrillic', ''),
                'category': request.form.get('category', 'general')
            }
            
            # Validate required fields
            if not article_data['title_latin'] or not article_data['title_cyrillic']:
                flash("Article title is required in both languages", "error")
                return render_template('first_aid_form.html', article=article_data)
            
            if not article_data['content_latin'] or not article_data['content_cyrillic']:
                flash("Article content is required in both languages", "error")
                return render_template('first_aid_form.html', article=article_data)
            
            success = run_async(db.update_first_aid_article(article_id, article_data))
            
            if success:
                flash(AdminTexts.FIRST_AID_UPDATED, "success")
                return redirect(url_for('first_aid_list'))
            else:
                flash("Error updating first aid article", "error")
        
        return render_template('first_aid_form.html', article=article)
        
    except Exception as e:
        logger.error(f"Error editing first aid article: {e}")
        flash("Error loading first aid article", "error")
        return redirect(url_for('first_aid_list'))

@app.route('/first_aid/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_first_aid(article_id):
    """Delete first aid article"""
    try:
        success = run_async(db.delete_first_aid_article(article_id))
        
        if success:
            flash(AdminTexts.FIRST_AID_DELETED, "success")
        else:
            flash("Error deleting first aid article", "error")
            
    except Exception as e:
        logger.error(f"Error deleting first aid article: {e}")
        flash("Error deleting first aid article", "error")
    
    return redirect(url_for('first_aid_list'))

if __name__ == '__main__':
    # Initialize database
    run_async(db.init_db())
    
    # Run Flask app
    app.run(debug=(FLASK_ENV == 'development'), host='0.0.0.0', port=443)
