import os
from decimal import Decimal
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .config import load_env
load_env()


from .database import Base, engine, get_db
from .repositories.supported_models_repo import SupportedModelsRepository
from .services.chat_service import ChatService
from .schemas import SupportedModelOut, ChatRequest, ChatResponse


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Plumloom LLM Chat API")


origins = os.getenv("CORS_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins.split(",")] if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# # Serve built frontend if present
# static_dir = os.path.join(os.path.dirname(__file__), "static")
# if os.path.isdir(static_dir):
#     app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


@app.get("/api/models", response_model=list[SupportedModelOut])
def list_models(db: Session = Depends(get_db)):
    repo = SupportedModelsRepository(db)
    return repo.list()


@app.post("/api/chat", response_model=ChatResponse)
def chat(body: ChatRequest, db: Session = Depends(get_db)):
    repo = SupportedModelsRepository(db)
    model = repo.get_by_id(body.model_id)
    if not model:
        raise HTTPException(status_code=400, detail="Invalid model_id")


    chat_svc = ChatService()
    try:
        text, input_tokens, output_tokens = chat_svc.chat(model.name, body.message)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Model call failed: {e}")


    # Cost = in_tokens * cpi + out_tokens * cpo
    cpi = Decimal(model.cost_per_input_token)
    cpo = Decimal(model.cost_per_output_token)
    cost = (Decimal(input_tokens) * cpi) + (Decimal(output_tokens) * cpo)


    return ChatResponse(
    response=text,
    input_tokens=input_tokens,
    output_tokens=output_tokens,
    cost=float(round(cost, 8)),
    )

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
