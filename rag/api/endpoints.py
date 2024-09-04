from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, HttpUrl
from rag.services.data_capture import DataCaptureService
from rag.services.embedding import EmbeddingService
from rag.services.qa import QAService

router = APIRouter()

class URLInput(BaseModel):
    url: HttpUrl

class QuestionInput(BaseModel):
    question: str

@router.post("/capture/url")
async def capture_url(url_input: URLInput):
    try:
        doc_id = await DataCaptureService.capture_url(str(url_input.url))
        embedding_service = EmbeddingService()
        await embedding_service.update_document_embedding(doc_id)
        return {"message": "URL captured and processed successfully", "document_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/capture/pdf")
async def capture_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(file.filename, "wb") as f:
            f.write(contents)
        
        doc_id = await DataCaptureService.capture_pdf(file.filename)
        embedding_service = EmbeddingService()
        await embedding_service.update_document_embedding(doc_id)
        return {"message": "PDF captured and processed successfully", "document_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/qa")
async def answer_question(question_input: QuestionInput):
    try:
        qa_service = QAService()
        answer = await qa_service.get_answer(question_input.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))