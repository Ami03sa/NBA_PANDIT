# server.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from main import NBAStatsChatbot

app = FastAPI(title="NBA Stats Chatbot Bridge")

# Allow local frontend to access backend (development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot once (keeps your logic as-is)
chatbot = NBAStatsChatbot()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return {"reply": "Please provide a message."}

    # This calls your existing process_query() method (no modification)
    result = chatbot.process_query(user_message)

    # result is the dict your code returns. Return the parts the frontend needs.
    reply = result.get("answer", "No answer generated.")
    # If you later want visualization, result.get("visualization") exists but may be a PIL image object.
    return {"reply": reply}
