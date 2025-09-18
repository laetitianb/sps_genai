import numpy as np
import spacy

_nlp = spacy.load("en_core_web_md")

def word_embedding(word: str) -> list[float]:
    doc = _nlp(word)
    if not doc:
        return []
    vecs = [t.vector for t in doc if t.has_vector]
    return (np.mean(vecs, axis=0) if vecs else np.zeros(_nlp.vocab.vectors_length)).astype(float).tolist()
