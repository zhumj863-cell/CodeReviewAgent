from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from ..core.reviewer import review
from ..core.chat_history import get_chat_history, query_chat
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
class ReviewRequest(BaseModel):
    # file_path: str
    code: str
    model: str = None
    chat_id: str = None

@app.post("/review")
async def review_code(req: ReviewRequest):
    return StreamingResponse(review(req.code, req.model, req.chat_id),  media_type="text/plain")

@app.get("/listChat")
async def list_chat():
    return get_chat_history()

@app.get("/getChat")
async def get_chat(id: str):
    return query_chat(id)