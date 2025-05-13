# Expense Tracker

A simple Flask-based web application to track personal expenses. Users can register, log in, add/edit/delete expenses, view and filter their expense list, and see a summary by category.

---

## Features

- **User Authentication**  
  - Registration with password strength validation (bcrypt)  
  - Login / logout with session management  

- **Expense Management**  
  - Add new expenses (amount, category, date, description)  
  - Edit or delete existing expenses  
  - Dashboard with sorting and filtering by date, category, amount  

- **Reporting**  
  - Summary view showing total spent and breakdown by category  

- **Responsive UI**  
  - Mobile-friendly navigation menu  
  - Flash messages for user feedback  

---

## Tech Stack

- **Backend:** Flask, SQLite (`sqlite3`), Jinja2 templates  
- **Auth & Security:** Flask sessions, bcrypt for password hashing  
- **Frontend:** HTML, CSS (static files in `static/`)  
- **Database:** SQLite file (`expense_tracker.db`)  

---

## Prerequisites

- Python 3.7+  
- pip  

---

## Installation

```bash
git clone https://github.com/BrianKYildirim/ExpenseTracker.git
cd ExpenseTracker

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install Flask bcrypt
````

> **Note:** The SQLite database will be created automatically on first run.

---

## Configuration

1. Open `__init__.py` and set a secure secret key:

   ```python
   app.secret_key = 'your_own_secret_key'
   ```

2. (Optional) Change the database file path in `__init__.py`:

   ```python
   app.config['DATABASE'] = '/path/to/your/expense_tracker.db'
   ```

---

## Running the App

```bash
python app.py
```

Then visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## Usage

1. **Register** with a valid email and a strong password (≥8 chars, uppercase, number, special char).
2. **Log in** to access your Dashboard.
3. **Add** expenses by filling out the amount, category, date, and an optional description.
4. **Edit/Delete** entries directly from the dashboard.
5. **Sort & Filter** your list via the “Sort & Filter” panel.
6. **Summary** page displays overall spending and category-wise totals.

---
