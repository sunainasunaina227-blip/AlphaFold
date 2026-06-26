from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class T(BaseModel):
    x: int

cfg = types.GenerateContentConfig(response_schema=T, response_mime_type="application/json")
print(type(cfg.response_schema))
