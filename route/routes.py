# route/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import User
from models.expense import Expense
import os

bp = Blueprint('routes', __name__)

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'expense_tracker.db')


@bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            flash('Email is required.')
            return render_template('register.html')
        if not User.valid_password(password):
            flash('Password must be at least 8 characters and include a capital letter, a number, and a special character.')
            return render_template('register.html')

        if User.create_user(DB_FILE, username, email, password):
            flash('Registration successful. Please log in.')
            return redirect(url_for('routes.login'))
        else:
            flash('Username or email already exists, or password is invalid.')
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')  # Could be username OR email.
        password = request.form.get('password')
        user = User.get_user_by_identifier(DB_FILE, identifier)
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid username/email or password.')
    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.index'))


@bp.route('/expense/add', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        date = request.form.get('date')
        description = request.form.get('description')
        Expense.add_expense(DB_FILE, session['user_id'], amount, category, date, description)
        flash('Expense added successfully.')
        return redirect(url_for('routes.dashboard'))
    return render_template('add_expense.html')


@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    distinct_categories = Expense.get_distinct_categories(DB_FILE, session['user_id'])

    sort_field = request.args.get('sort_field', 'date')
    sort_order = request.args.get('sort_order', 'ASC')
    category_filters = request.args.getlist('cat')  # e.g., ['Gym', 'Netflix']
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    min_amount = request.args.get('min_amount')
    max_amount = request.args.get('max_amount')

    expenses = Expense.get_expenses(
        DB_FILE,
        user_id=session['user_id'],
        categories=category_filters,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount,
        sort_field=sort_field,
        sort_order=sort_order
    )

    return render_template(
        'dashboard.html',
        expenses=expenses,
        categories=distinct_categories
    )


@bp.route('/expense/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        date = request.form.get('date')
        description = request.form.get('description')
        Expense.update_expense(DB_FILE, expense_id, amount, category, date, description)
        flash('Expense updated successfully.')
        return redirect(url_for('routes.dashboard'))
    else:
        expenses = Expense.get_expenses(DB_FILE, session['user_id'])
        expense = next((e for e in expenses if e.id == expense_id), None)
        return render_template('edit_expense.html', expense=expense)


@bp.route('/expense/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    Expense.delete_expense(DB_FILE, expense_id)
    flash('Expense deleted successfully.')
    return redirect(url_for('routes.dashboard'))


@bp.route('/summary')
def summary():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    total, summary_data = Expense.get_summary(DB_FILE, session['user_id'])
    return render_template('summary.html', total=total, summary_data=summary_data)
