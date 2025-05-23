import os
import fitz
from database import load_pdfs_to_db, get_all_pdfs

def test_pdf_loading():
    print("Починаємо тестування завантаження PDF...")
    
    # Перевіряємо наявність файлів
    pdf_folder = "PDFS"
    print("\nФайли в папці PDFS:")
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            print(f"- {file}")
    
    # Завантажуємо PDF-файли
    print("\nЗавантаження PDF-файлів...")
    load_pdfs_to_db()
    
    # Перевіряємо завантажені документи
    print("\nЗавантажені документи:")
    documents = get_all_pdfs()
    print(f"Кількість завантажених документів: {len(documents)}")
    
    # Виводимо перші 200 символів кожного документа
    for i, doc in enumerate(documents):
        print(f"\nДокумент {i+1}:")
        print(doc[:200] + "...")

if __name__ == "__main__":
    test_pdf_loading() 