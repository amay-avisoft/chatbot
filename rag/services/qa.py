import openai
from rag.config import settings
from rag.models.document import TextDocument
from rag.services.embedding import EmbeddingService

openai.api_key = settings.OPENAI_API_KEY

class QAService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    async def get_answer(self, question: str) -> str:
        question_embedding = await self.embedding_service.generate_embedding(question)
        
        pipeline = [
            {
                "$search": {
                    "index": "default",
                    "knnBeta": {
                        "vector": question_embedding,
                        "path": "embedding",
                        "k": 3
                    }
                }
            },
            {
                "$project": {
                    "content": 1,
                    "score": { "$meta": "searchScore" }
                }
            }
        ]
        
        similar_docs = TextDocument.objects.aggregate(pipeline)
        
        context = "\n".join([doc['content'] for doc in similar_docs])
        
        system_prompt = f"You are a helpful customer service agent working for the organization {settings.ORGANIZATION_NAME}. {settings.ORGANIZATION_SUMMARY}."
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ]
        )
        
        return response.choices[0].message.content