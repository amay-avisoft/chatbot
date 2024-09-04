import newspaper
from goose3 import Goose
from langchain_community.document_loaders import PyPDFLoader
from rag.models.document import TextDocument

class DataCaptureService:
    @staticmethod
    async def capture_url(url: str) -> str:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        
        if not article.text:
            g = Goose()
            article = g.extract(url=url)
        
        doc = TextDocument(content=article.text, source_url=url)
        doc.save()
        return str(doc.id)

    @staticmethod
    async def capture_pdf(file_path: str) -> str:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        content = "\n".join([page.page_content for page in pages])
        
        doc = TextDocument(content=content, source_url=file_path)
        doc.save()
        return str(doc.id)
