from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from openai import OpenAI

# Загружаем API-ключ из .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

@app.post("/check")
async def check_text(input: TextInput):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты антиплагиат-бот. Твоя задача — анализировать тексты на русском и казахском языках и определять их уникальность. Оцени: насколько текст может быть оригинальным или заимствованным, укажи предполагаемый процент совпадения (0–100%) и объясни, почему ты так решил (по структуре, фразам, стилю, терминам). Даже если у тебя нет доступа к интернету, оцени текст по шаблонности, стилю и типичным выражениям."},
                {"role": "user", "content": f"Оцени уникальность следующего текста:\n\n{input.text}"}
            ]
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
