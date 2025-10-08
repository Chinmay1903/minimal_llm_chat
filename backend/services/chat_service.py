import os
from typing import Tuple
from openai import OpenAI
from ..config import load_env


class ChatService:
    def __init__(self):
        load_env()
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.client = OpenAI(api_key=self.api_key) if (OpenAI and self.api_key) else None

    def chat(self, model_name: str, message: str) -> Tuple[str, int, int]:
        """
        Returns (text, input_tokens, output_tokens).
        Uses OpenAI Chat Completions when an API key is present; otherwise returns a mock.
        """
        if not self.client:
            # Safe fallback so your endpoint still works during setup
            text = f"(mock) You said: {message}"
            return text, 0, 0

        # NOTE: ensure httpx<0.28 if using openai==1.51.x
        resp = self.client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": message}],
            temperature=0.2,
        )
        text = resp.choices[0].message.content or ""
        usage = getattr(resp, "usage", None)

        # OpenAI returns either prompt/completion or input/output depending on model
        in_tok = getattr(usage, "prompt_tokens", None) or getattr(usage, "input_tokens", 0) or 0
        out_tok = getattr(usage, "completion_tokens", None) or getattr(usage, "output_tokens", 0) or 0

        return text, int(in_tok), int(out_tok)
