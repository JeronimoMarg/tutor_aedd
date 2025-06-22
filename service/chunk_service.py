import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from repository.environment import Environment
from repository.mongo_chunk_repository import MongoChunkRepository
from model.chunk import Chunk

class ChunkService(object):
    def __init__(self, env: Environment, chunk_repository: MongoChunkRepository):
        self.chunk_repository = chunk_repository
        self.model = SentenceTransformer(env.EMBEDDING_MODEL)
        base_index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())
        self.index = faiss.IndexIDMap(base_index)

    def get_chunk_id(self) -> np.int64:
        # buscar el ultimo id en mongo
        return self.chunk_repository.get_id()

    def chunk_text(self, text: str, chunk_size: int=500, overlap: int=100) -> list[Chunk]:
        start_id = self.get_chunk_id()
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk_text = " ".join(words[i:i + chunk_size])
            chunk = Chunk(start_id + i + 1, chunk_text)
            chunks.append(chunk)

            # Guardar en mongo
            self.chunk_repository.save(chunk)

            # Guardar en bdd vectorial
            vector = np.array([self.model.encode(chunk.text)]) 
            self.index.add_with_ids(vector, np.array([chunk.id]))

        return chunks

    def find_chunks(self, text: str, top_k: int=3) -> list[str]:
        distances, indices = self.index.search(text, top_k)
        chunks = []
        for i in indices:
            chunk = self.chunk_repository.find(i)
            if chunk:
                chunks.append(chunk)
        return chunks

    
