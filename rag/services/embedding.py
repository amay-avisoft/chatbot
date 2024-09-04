from sentence_transformers import SentenceTransformer
from rag.models.document import TextDocument

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    async def generate_embedding(self, text: str) -> list:
        return self.model.encode(text).tolist()

    async def update_document_embedding(self, doc_id: str):
        doc = TextDocument.objects(id=doc_id).first()
        if doc:
            doc.embedding = await self.generate_embedding(doc.content)
            doc.save()
