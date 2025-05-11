from pydantic import BaseModel, Field

from typing_extensions import Optional


class Documents(BaseModel):
    documents: Optional[list[dict[str, str]]] = Field(
        ..., description="Lista de documentos carregados do S.O."
    )
