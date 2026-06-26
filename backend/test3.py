import json
from pydantic import BaseModel
from utils.gemini_client import call_gemini_structured
from graph.models import ProjectTimeline
prompt="Generate a simple timeline with total 10 days and 1 phase."
print(call_gemini_structured(prompt, response_schema=ProjectTimeline))
