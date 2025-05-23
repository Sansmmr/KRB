import sqlite3

# Підключення до бази даних
conn = sqlite3.connect('data/documents.db')
cursor = conn.cursor()

# Виконання SQL-запиту
cursor.execute('SELECT * FROM queries')
rows = cursor.fetchall()

# Виведення результатів
for row in rows:
    print(f"ID: {row[0]}, Запит: {row[1]}, Відповідь: {row[2]}, Дата: {row[3]}")

# Закриття з'єднання
conn.close()