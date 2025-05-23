import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModel
from openai import OpenAI
from database import load_pdfs_to_db, save_query_and_answer, get_all_pdfs, close_connection, get_all_queries
import logging
import markdown  


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація клієнта DeepSeek
client = OpenAI(
    api_key="YOUR_API_KEY", 
    base_url="https://api.deepseek.com"  
)

в
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
model = AutoModel.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


try:
    load_pdfs_to_db()
    logger.info("PDF files loaded successfully")
except Exception as e:
    logger.error(f"Error loading PDF files: {str(e)}")

# Отримання всіх документів з бази даних
try:
    documents = get_all_pdfs()
    logger.info(f"Retrieved {len(documents)} documents from database")
except Exception as e:
    logger.error(f"Error getting documents: {str(e)}")
    documents = []

# Функція для створення ембеддингів тексту
def get_embedding(text):
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()
    except Exception as e:
        logger.error(f"Error creating embedding: {str(e)}")
        raise

# Створення індексу для пошуку
try:
    embeddings = np.array([get_embedding(doc) for doc in documents])
    embeddings = embeddings.squeeze(axis=1) 
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    logger.info("Search index created successfully")
except Exception as e:
    logger.error(f"Error creating search index: {str(e)}")
    raise


def search_relevant_documents(query, k=8): 
    try:
       
        keywords = query.lower().split()
        
       
        query_embedding = get_embedding(query)
        query_embedding = query_embedding.squeeze(axis=0)
        
        
        distances, indices = index.search(np.array([query_embedding]), k)
        
        
        relevant_docs = [documents[i] for i in indices[0]]
        
        keyword_matches = []
        for doc in documents:
            doc_lower = doc.lower()
            if any(keyword in doc_lower for keyword in keywords):
                keyword_matches.append(doc)
        
        all_results = list(set(relevant_docs + keyword_matches))
        
        sorted_results = []
        for doc in all_results:
            doc_lower = doc.lower()
            relevance_score = sum(1 for keyword in keywords if keyword in doc_lower)
            # Додатково перевіряємо наявність фраз з запиту
            if len(keywords) > 1:
                phrases = [' '.join(keywords[i:i+2]) for i in range(len(keywords)-1)]
                relevance_score += sum(2 for phrase in phrases if phrase in doc_lower)
            sorted_results.append((doc, relevance_score))
        
        sorted_results.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in sorted_results[:k]]
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise

# Функція для генерації відповіді з використанням DeepSeek API
def generate_answer_with_deepseek(query):
    try:
        logger.info(f"Processing query: {query}")
        
        # Пошук релевантних документів
        relevant_docs = search_relevant_documents(query)
        logger.info(f"Found {len(relevant_docs)} relevant documents")
        
        # Створюємо контекст з кращим форматуванням
        context_parts = []
        for i, doc in enumerate(relevant_docs, 1):
            
            context_parts.append(f"--- Документ {i} ---\n{doc}")
        
        context = "\n\n".join(context_parts)
        logger.info("Created context from relevant documents")
        
        # Генерація відповіді
        response = client.chat.completions.create(
            model="deepseek-chat",  
            messages=[
                {"role": "system", "content": "Ти помічник, який відповідає на питання на основі наданого контексту. Використовуй всю доступну інформацію з контексту для формування повної та точної відповіді. Якщо інформація є в контексті, обов'язково включи її у відповідь. Форматуй відповідь використовуючи Markdown для кращої читабельності: використовуй заголовки (# для основних заголовків, ## для підзаголовків), списки (- або * для маркованих списків, 1. 2. 3. для нумерованих), **жирний текст** для важливих деталей, та інші елементи Markdown для структурування відповіді."},
                {"role": "user", "content": f"Контекст: {context}\n\nПитання: {query}\n\nВідповідь:"}
            ],
            stream=False,
            temperature=0.3
        )
        
        answer = response.choices[0].message.content.strip()
        logger.info("Generated answer successfully")
        
       
        save_query_and_answer(query, answer)
        logger.info("Saved query and answer to database")
        
        return answer  
    except Exception as e:
        logger.error(f"Error in generate_answer_with_deepseek: {str(e)}")
        return f"Вибачте, сталася помилка при обробці вашого запиту: {str(e)}"


def run_console_mode():
    while True:
        query = input("Напишіть запит (або введіть 'вихід' для завершення): ")
        if query.lower() == "вихід":
            print("Програма завершена.")
            break
        answer = generate_answer_with_deepseek(query)
        print("\nВідповідь:", answer, "\n")
    
    
    print("Всі запити та відповіді з бази даних:")
    queries = get_all_queries()
    for q in queries:
        print(f"Запит: {q[0]}\nВідповідь: {q[1]}\nДата: {q[2]}\n")

    
    close_connection()

if __name__ == "__main__":
    run_console_mode()