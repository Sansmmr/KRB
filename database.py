import os
import sqlite3
import fitz  # PyMuPDF

# Шлях до бази даних у папці data
db_path = os.path.join('data', 'documents.db')

# Перевірка, чи існує папка data, і створення її, якщо ні
os.makedirs('data', exist_ok=True)

# Підключення до бази даних (або створення нової, якщо вона не існує)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Створення таблиць, якщо вони ще не існують
cursor.execute('''
CREATE TABLE IF NOT EXISTS pdfs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    content TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()

# Функція для читання тексту з PDF-файлу
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Завантаження PDF-файлів у базу даних
def load_pdfs_to_db(folder_path="PDFS"):
    # Очищаємо стару таблицю
    cursor.execute('DELETE FROM pdfs')
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            try:
                text = extract_text_from_pdf(pdf_path)
                cursor.execute('INSERT INTO pdfs (filename, content) VALUES (?, ?)', (filename, text))
                print(f"Loaded PDF: {filename}")
            except Exception as e:
                print(f"Error loading PDF {filename}: {str(e)}")
    conn.commit()

# Функція для збереження запитів та відповідей у базу даних
def save_query_and_answer(query, answer):
    cursor.execute('INSERT INTO queries (query, answer) VALUES (?, ?)', (query, answer))
    conn.commit()

# Функція для отримання всіх PDF-файлів з бази даних
def get_all_pdfs():
    cursor.execute('SELECT content FROM pdfs')
    return [row[0] for row in cursor.fetchall()]

# Функція для отримання всіх запитів та відповідей з бази даних
def get_all_queries():
    cursor.execute('SELECT query, answer, timestamp FROM queries')
    return cursor.fetchall()

# Функція для очищення історії запитів
def clear_query_history():
    cursor.execute('DELETE FROM queries')
    conn.commit()

# Закриття з'єднання з базою даних (викликати в кінці роботи)
def close_connection():
    conn.close()