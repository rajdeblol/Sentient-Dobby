from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Mount static files for CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Sentient Client
client = OpenAI(api_key=os.getenv("SENTIENT_API_KEY"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/validate", response_class=HTMLResponse)
async def validate_startup(request: Request, idea: str = Form(...)):
    response = client.chat.completions.create(
        model="SentientAGI/Dobby-Mini-Unhinged-Plus-Llama-3.1-8B_GGUF",
        messages=[
            {"role": "system", "content": "You are an AI startup validator."},
            {"role": "user", "content": f"Validate this startup idea: {idea}"}
        ]
    )
    result = response.choices[0].message.content
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "idea": idea})
  
