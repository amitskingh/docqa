from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Document
from .utils.pdf_utils import extract_text_from_pdf
from .utils.vector_utils import chunk_text, create_vector_store

# store in memory temporarily
VECTOR_DB = {}


class UploadDocument(APIView):
    def post(self, request):
        file = request.FILES["file"]
        doc = Document.objects.create(file=file)
        text = extract_text_from_pdf(doc.file.path)
        doc.text = text
        doc.save()

        chunks = chunk_text(text)
        index, embeddings, chunk_list = create_vector_store(chunks)
        VECTOR_DB[doc.id] = {"index": index, "chunks": chunk_list}

        return Response(
            {"id": doc.id, "message": "Document uploaded and indexed successfully"}
        )


from .models import Question
from .utils.vector_utils import search_similar_chunks
from .utils.groq_utils import generate_answer


class AskQuestion(APIView):
    def post(self, request):
        doc_id = request.data.get("document_id")
        question_text = request.data.get("question")

        if doc_id not in VECTOR_DB:
            return Response({"error": "Document not found or not indexed"}, status=404)

        data = VECTOR_DB[doc_id]
        context_chunks = search_similar_chunks(
            data["index"], data["chunks"], question_text
        )
        context = "\n\n".join(context_chunks)

        answer = generate_answer(context, question_text)
        Question.objects.create(
            document_id=doc_id, question=question_text, answer=answer
        )
        return Response({"answer": answer})
