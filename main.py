from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import yt_dlp

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/download")
async def download(request: Request):
    data = await request.json()
    url = data.get("url")
    try:
        with yt_dlp.YoutubeDL({'format': 'best'}) as ydl:
            info = ydl.extract_info(url, download=False)
            return {"url": info.get("url"), "thumb": info.get("thumbnail")}
    except Exception as e:
        return {"error": str(e)}
