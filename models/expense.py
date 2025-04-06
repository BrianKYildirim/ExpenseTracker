import sqlite3
from datetime import datetime


class Expense:
    def __init__(self, id, user_id, amount, category, date, description):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    @property
    def date_mdy(self):
        try:
            dt = datetime.strptime(self.date, "%Y-%m-%d")
            return dt.strftime("%m/%d/%Y")
        except ValueError:
            return self.date or "N/A"

    @staticmethod
    def add_expense(db_file, user_id, amount, category, date, description):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""
                INSERT INTO expenses (user_id, amount, category, date, description)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, amount, category, date, description))
        conn.commit()
        conn.close()

    @staticmethod
    def get_expenses(db_file, user_id, categories=None, start_date=None, end_date=None,
                     min_amount=None, max_amount=None, sort_field='date', sort_order='ASC'):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Base query and parameter list
        query = "SELECT id, user_id, amount, category, date, description FROM expenses WHERE user_id = ?"
        params = [user_id]

        # Filter by multiple categories
        if categories and len(categories) > 0:
            query += " AND category IN ({})".format(",".join("?" for _ in categories))
            params.extend(categories)

        # Other filters
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        if min_amount:
            query += " AND amount >= ?"
            params.append(min_amount)
        if max_amount:
            query += " AND amount <= ?"
            params.append(max_amount)

        # Sorting
        valid_sort_fields = {'date': 'date', 'category': 'category', 'amount': 'amount'}
        sort_field = valid_sort_fields.get(sort_field, 'date')
        sort_order = 'DESC' if sort_order.upper() == 'DESC' else 'ASC'
        query += f" ORDER BY {sort_field} {sort_order}"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        conn.close()
        return [Expense(*row) for row in rows]

    @staticmethod
    def get_distinct_categories(db_file, user_id):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM expenses WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    @staticmethod
    def update_expense(db_file, expense_id, amount, category, date, description):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""
                UPDATE expenses
                SET amount = ?, category = ?, date = ?, description = ?
                WHERE id = ?
            """, (amount, category, date, description, expense_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_expense(db_file, expense_id):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_summary(db_file, user_id):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""
                SELECT category, SUM(amount) FROM expenses
                WHERE user_id = ?
                GROUP BY category
            """, (user_id,))
        summary_data = cursor.fetchall()
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
        total = cursor.fetchone()[0]
        if total is None:
            total = 0
        conn.close()
        return total, summary_data
