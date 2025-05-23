import fitz

def check_pdf_content():
    print("Перевірка вмісту файлу 3kurs.pdf...")
    
    doc = fitz.open("PDFS/3kurs.pdf")
    full_text = ""
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        full_text += text
        print(f"\nСторінка {page_num + 1}:")
        print(text[:500] + "..." if len(text) > 500 else text)
    
    # Шукаємо інформацію про комп'ютерні науки
    if "комп'ютерні науки" in full_text.lower():
        print("\nЗнайдено інформацію про комп'ютерні науки!")
        # Знаходимо контекст навколо згадки
        index = full_text.lower().find("комп'ютерні науки")
        start = max(0, index - 200)
        end = min(len(full_text), index + 200)
        print("\nКонтекст:")
        print(full_text[start:end])
    else:
        print("\nІнформацію про комп'ютерні науки не знайдено")

if __name__ == "__main__":
    check_pdf_content() 