from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import SupportedModel


class SupportedModelsRepository:
    def __init__(self, db: Session):
        self.db = db


    def list(self) -> List[SupportedModel]:
        return self.db.query(SupportedModel).order_by(SupportedModel.display_name.asc()).all()


    def get_by_id(self, model_id) -> Optional[SupportedModel]:
        return self.db.query(SupportedModel).filter(SupportedModel.id == model_id).first()


    def upsert_by_name(self, *, name: str, display_name: str, provider: str, cpi, cpo) -> SupportedModel:
        m = self.db.query(SupportedModel).filter(SupportedModel.name == name).first()
        if m is None:
            m = SupportedModel(name=name, display_name=display_name, provider=provider,
            cost_per_input_token=cpi, cost_per_output_token=cpo)
            self.db.add(m)
        else:
            m.display_name = display_name
            m.provider = provider
            m.cost_per_input_token = cpi
            m.cost_per_output_token = cpo
            self.db.commit()
            self.db.refresh(m)
        return m
    