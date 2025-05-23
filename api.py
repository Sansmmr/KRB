from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from agent import generate_answer_with_deepseek, get_all_pdfs
from database import get_all_queries, clear_query_history
import logging
from datetime import datetime
import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Очистка истории запросов при запуске сервера
clear_query_history()
logger.info("Query history cleared on startup")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str

class QueryResponse(BaseModel):
    query: str
    answer: str
    timestamp: Optional[str]

@app.post("/api/query", response_model=QueryResponse)
async def process_query(query: Query):
    try:
        logger.info(f"Received query: {query.text}")
        answer = generate_answer_with_deepseek(query.text)
        logger.info(f"Generated answer: {answer}")
        
        response = QueryResponse(
            query=query.text,
            answer=answer,
            timestamp=datetime.now().isoformat()
        )
        logger.info(f"Sending response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history", response_model=List[QueryResponse])
async def get_history():
    try:
        queries = get_all_queries()
        logger.info(f"Retrieved {len(queries)} queries from history")
        return [
            QueryResponse(
                query=q[0],
                answer=q[1],
                timestamp=q[2]
            ) for q in queries
        ]
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents")
async def get_documents():
    try:
        docs = get_all_pdfs()
        logger.info(f"Retrieved {len(docs)} documents")
        return {"documents": docs}
    except Exception as e:
        logger.error(f"Error getting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rouge-results")
async def get_rouge_results():
    try:
        # Read the Excel file
        df = pd.read_excel('rouge_results.xlsx')
        # Convert to list of dictionaries
        results = df.to_dict('records')
        logger.info(f"Retrieved {len(results)} ROUGE results")
        return results
    except Exception as e:
        logger.error(f"Error getting ROUGE results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 