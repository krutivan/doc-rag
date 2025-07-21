import os
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.index.index_service import IndexService
from src.core.dto.index_dto import IndexResponse

router = APIRouter()


@router.post("/index", response_model=IndexResponse)
async def index_document(file: UploadFile = File(...)):
    # Save uploaded file to a temp location
    try:
        suffix = os.path.splitext(file.filename)[1]
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File upload failed: {str(e)}")

    try:
        # index service for indexing the document
        num_chunks = IndexService.index(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")
    finally:
        os.remove(tmp_path)

    return IndexResponse(num_chunks=num_chunks)
