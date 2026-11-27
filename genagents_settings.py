import os
from pathlib import Path
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
KEY_OWNER = "TahminAI"
DEBUG = False
MAX_CHUNK_SIZE = 4
LLM_VERS = os.environ.get("TAHMIN_MODEL", "gpt-4o-mini")
BASE_DIR = str(Path(__file__).resolve().parent.parent)
POPULATIONS_DIR = f"{BASE_DIR}/agent_bank/populations"
LLM_PROMPT_DIR = f"{BASE_DIR}/simulation_engine/prompt_template"
