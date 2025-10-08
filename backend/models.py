import uuid
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Numeric, UniqueConstraint
from .database import Base


class SupportedModel(Base):
    __tablename__ = "supported_models"
    __table_args__ = (UniqueConstraint("name", name="uq_supported_models_name"),)


    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128), nullable=False) # e.g., 'gpt-4o-mini'
    display_name: Mapped[str] = mapped_column(String(128), nullable=False) # e.g., 'GPT-4o Mini'
    provider: Mapped[str] = mapped_column(String(32), nullable=False, default="openai")
    cost_per_input_token: Mapped[Decimal] = mapped_column(Numeric(18, 10), nullable=False, default=Decimal("0"))
    cost_per_output_token: Mapped[Decimal] = mapped_column(Numeric(18, 10), nullable=False, default=Decimal("0"))
    