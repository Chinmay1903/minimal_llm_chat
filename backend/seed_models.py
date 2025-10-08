from decimal import Decimal
from .database import Base, engine, SessionLocal
from .repositories.supported_models_repo import SupportedModelsRepository

# Pricing per TOKEN (converted from per 1M)
PER_MILLION = Decimal("1000000")

PRICING = {
    "gpt-4o":        ("GPT-4o",        Decimal("2.50")/PER_MILLION, Decimal("10.00")/PER_MILLION),
    "gpt-4o-mini":   ("GPT-4o Mini",   Decimal("0.15")/PER_MILLION, Decimal("0.60")/PER_MILLION),
    "gpt-3.5-turbo": ("GPT-3.5 Turbo", Decimal("0.50")/PER_MILLION, Decimal("1.50")/PER_MILLION),
}

def main():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:  # type: Session
        repo = SupportedModelsRepository(db)

        for name, (disp, cpi, cpo) in PRICING.items():
            m = repo.upsert_by_name(name=name, display_name=disp, provider="openai", cpi=cpi, cpo=cpo)
            print("Upserted:", m.display_name, cpi, cpo)

    print("Seeding complete.")


if __name__ == "__main__":
    main()
    