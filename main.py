from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

SENTIENT_API_KEY = os.getenv("SENTIENT_API_KEY")
SENTIENT_BASE_URL = os.getenv("SENTIENT_BASE_URL")

# Fireworks Dobby-70B model
MODEL = "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new"

# Create Fireworks client
client = OpenAI(
    api_key=SENTIENT_API_KEY,
    base_url=SENTIENT_BASE_URL
)

app = FastAPI(title="Smart Startup Validator")

# Static + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": None, "idea": ""}
    )


@app.post("/validate", response_class=HTMLResponse)
async def validate_startup(request: Request, idea: str = Form(...)):
    # Query Fireworks model
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        messages=[
            {"role": "system", "content": (
                "You are a precise venture analyst. Return a concise, actionable validation:\n"
                "1) Competitors (3–5)\n2) Strengths\n3) Weaknesses\n"
                "4) Improvements\n5) Risk score (0–100) and Go/No-Go.\n"
                "Keep it clean and skimmable."
            )},
            {"role": "user", "content": idea}
        ]
    )

    result = resp.choices[0].message.content

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result, "idea": idea}
    )
    
