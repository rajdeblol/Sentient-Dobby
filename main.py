from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

SENTIENT_API_KEY = os.getenv("SENTIENT_API_KEY")
SENTIENT_BASE_URL = os.getenv("SENTIENT_BASE_URL")  # optional if your tenant needs it
MODEL = "SentientAGI/Dobby-Mini-Unhinged-Plus-Llama-3.1-8B_GGUF"

# Create client (works with or without custom base_url)
client = OpenAI(
    api_key=SENTIENT_API_KEY,
    base_url=SENTIENT_BASE_URL if SENTIENT_BASE_URL else None
)

app = FastAPI(title="Smart Startup Validator")

# Static + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None, "idea": ""})

@app.post("/validate", response_class=HTMLResponse)
async def validate_startup(request: Request, idea: str = Form(...)):
    # You can tune temperature if you want a spicier/steadier output
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        messages=[
            {"role": "system", "content": (
                "You are a precise venture analyst. Return a concise, actionable validation: "
                "1) Competitors (3–5), 2) Strengths, 3) Weaknesses, 4) Improvements, "
                "5) Risk score (0–100) and Go/No-Go. Keep it clean and skimmable."
            )},
            {"role": "user", "content": idea}
        ]
    )
    result = resp.choices[0].message.content
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "idea": idea})
    
