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
        dim = self.model.get_sentence_embedding_dimension()
        base_index = faiss.IndexFlatL2(int(dim))
        self.index = faiss.IndexIDMap(base_index)
        self.load_chunks()

    def get_chunk_id(self) -> np.int64:
        # buscar el ultimo id en mongo
        return self.chunk_repository.get_id()

    def chunk_text(self, text: str, chunk_size: int=500, overlap: int=100) -> list[Chunk]:
        chunk_id = self.get_chunk_id() + 1
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_text = " ".join(words[i:i + chunk_size])
            chunk = Chunk(chunk_id , chunk_text)
            chunks.append(chunk)
            chunk_id += 1

        return chunks
    
    def save_chunks(self, chunks: list[Chunk]):
        self.index_chunks(chunks)
        self.chunk_repository.save(chunks)

    def index_chunks(self, chunks) -> int:
        vecs = self.model.encode([c.text for c in chunks])
        self.index.add_with_ids(vecs, np.array([c.id for c in chunks]))

    def load_chunks(self):
        chunks = self.chunk_repository.findAll()
        if len(chunks) > 0:
            self.index_chunks(chunks)

    def find_chunks(self, text: str, top_k: int=3) -> list[str]:
        vec = self.model.encode(text)
        distances, indices = self.index.search(np.array([vec]), top_k)
        chunks = self.chunk_repository.find([int(i) for i in indices[0]])
        return [c.text for c in chunks]

    
