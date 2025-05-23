import json
import pandas as pd
from rouge_score import rouge_scorer
from agent import generate_answer_with_deepseek
import openpyxl

# 🔧 Нормалізація тексту: пробіли, регістр
def normalize_text(text):
    return ' '.join(text.lower().split())

# 📥 Завантаження тестових даних
with open('test_data.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

# 📏 Ініціалізація метрик з стемінгом
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

# 📊 Збір результатів
results = []

for item in test_data:
    query = item["query"]
    reference = normalize_text(item["reference_answer"])
    
    # 🧠 Генерація відповіді
    generated_raw = generate_answer_with_deepseek(query)
    generated = normalize_text(generated_raw)
    
    # 🔎 Пропуск порожніх або коротких відповідей
    if len(generated.strip()) < 10:
        print(f"⚠️ Пропущено запит через коротку відповідь: '{generated_raw}'")
        continue
    
    # 📈 ROUGE-оцінювання
    scores = scorer.score(reference, generated)

    # 📋 Додавання результату
    results.append({
        'Query': query,
        'Reference': reference,
        'Generated': generated,
        'ROUGE-1 F1': scores['rouge1'].fmeasure,
        'ROUGE-1 Precision': scores['rouge1'].precision,
        'ROUGE-1 Recall': scores['rouge1'].recall,
        'ROUGE-L F1': scores['rougeL'].fmeasure,
        'ROUGE-L Precision': scores['rougeL'].precision,
        'ROUGE-L Recall': scores['rougeL'].recall
    })

    # 🖨️ Вивід у консоль
    print(f"Query: {query}")
    print(f"Reference: {reference}")
    print(f"Generated: {generated}")
    print(f"ROUGE-1 F1: {scores['rouge1'].fmeasure:.4f} | Precision: {scores['rouge1'].precision:.4f} | Recall: {scores['rouge1'].recall:.4f}")
    print(f"ROUGE-L F1: {scores['rougeL'].fmeasure:.4f} | Precision: {scores['rougeL'].precision:.4f} | Recall: {scores['rougeL'].recall:.4f}")
    print("-" * 60)

# 💾 Збереження в Excel
df = pd.DataFrame(results)
df.to_excel('rouge_results.xlsx', index=False)

# 📊 Агрегація середніх значень
avg_metrics = df[['ROUGE-1 F1', 'ROUGE-L F1', 'ROUGE-1 Precision', 'ROUGE-L Precision', 'ROUGE-1 Recall', 'ROUGE-L Recall']].mean()

print("\n📊 Середні значення по всіх відповідях:")
for metric, value in avg_metrics.items():
    print(f"{metric}: {value:.4f}")

print("\n✅ Результати збережено у файл 'rouge_results.xlsx'")