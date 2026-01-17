import os

from dotenv import load_dotenv

load_dotenv(override=True)

LLM_API_KEY=os.environ.get("LLM_API_KEY")

LLM_BASE_URL=os.environ.get("LLM_BASE_URL")





