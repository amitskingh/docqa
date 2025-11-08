from groq import Groq
from decouple import config


grok_api_key = config("grok_api_key")

grok_api_key = config("gork_api_key")

# client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
client = Groq(
    api_key=grok_api_key,
)


def generate_answer(context, question):
    prompt = f"""You are an assistant that answers questions using ONLY the context below.
If the question is unrelated, reply exactly "This question is not related to the document."

Context:
{context}

Question: {question}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
