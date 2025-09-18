from fastapi import FastAPI
from pydantic import BaseModel
from app.bigram_model import BigramModel

app = FastAPI()

corpus = [
    "The Count of Monte Cristo is a novel written by Alexandre Dumas.",
    "this is another example sentence",
    "we are generating text based on bigram probabilities",
    "bigram models are simple but effective",
]

bigram_model = BigramModel(corpus)

class TextGenerationRequest(BaseModel):
    start_word: str
    length: int

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate")
def generate_text(request: TextGenerationRequest):
    text = bigram_model.generate_text(request.start_word, request.length)
    return {"generated_text": text}
from fastapi import HTTPException
from app.embeddings import word_embedding
from pydantic import BaseModel

class EmbedRequest(BaseModel):
    query: str

class EmbedResponse(BaseModel):
    query: str
    vector: list[float]
    dim: int

@app.post("/embed", response_model=EmbedResponse)
def embed(req: EmbedRequest):
    q = (req.query or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Query must be non-empty.")
    vec = word_embedding(q)
    if not vec:
        raise HTTPException(status_code=422, detail="No embedding for input.")
    return EmbedResponse(query=q, vector=vec, dim=len(vec))
