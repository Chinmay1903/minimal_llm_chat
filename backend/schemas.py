import uuid
from decimal import Decimal
from pydantic import BaseModel, Field


class SupportedModelOut(BaseModel):
    id: uuid.UUID
    name: str
    display_name: str
    provider: str
    cost_per_input_token: Decimal
    cost_per_output_token: Decimal
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    model_id: uuid.UUID = Field(..., description="UUID of supported model")
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    response: str
    input_tokens: int
    output_tokens: int
    cost: float
    