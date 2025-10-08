# backend/config.py
from pathlib import Path
from dotenv import load_dotenv

def load_env():
    """
    Load env from project root so it works no matter the CWD.
    Priority order:
      .env.local  (not committed, overrides)
      .env        (not committed)
    """
    root = Path(__file__).resolve().parents[1]  # .../plumloom-llm-chat
    for name in (".env.local", ".env"):
        p = root / name
        if p.exists():
            # override=False lets already-set OS envs win (good for CI/Heroku)
            load_dotenv(p, override=False)
