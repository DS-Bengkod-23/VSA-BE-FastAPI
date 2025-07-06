from pydantic import BaseModel
from typing import Any, Dict, Optional


class TextRequest(BaseModel):
    text: str

class MetaResponse(BaseModel):
    status: str
    code: int
    message: str

class ApiResponse(BaseModel):
    meta: MetaResponse
    data: Optional[Dict[str, Any]] = None  # Data bisa berupa apa saja dan opsional
