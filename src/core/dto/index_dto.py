from pydantic import BaseModel

class IndexResponse(BaseModel):
    num_chunks: int
