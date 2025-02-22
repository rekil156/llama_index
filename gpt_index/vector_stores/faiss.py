"""Faiss Vector store index.

An index that that is built on top of an existing vector store.

"""

import os
from typing import Any, List, cast

import numpy as np

from gpt_index.vector_stores.types import (
    DEFAULT_PERSIST_DIR,
    DEFAULT_PERSIST_FNAME,
    NodeEmbeddingResult,
    VectorStore,
    VectorStoreQueryResult,
    VectorStoreQuery,
)

import logging

logger = logging.getLogger()


class FaissVectorStore(VectorStore):
    """Faiss Vector Store.

    Embeddings are stored within a Faiss index.

    During query time, the index uses Faiss to query for the top
    k embeddings, and returns the corresponding indices.

    Args:
        faiss_index (faiss.Index): Faiss index instance

    """

    stores_text: bool = False

    def __init__(
        self,
        faiss_index: Any,
    ) -> None:
        """Initialize params."""
        import_err_msg = """
            `faiss` package not found. For instructions on
            how to install `faiss` please visit
            https://github.com/facebookresearch/faiss/wiki/Installing-Faiss
        """
        try:
            import faiss  # noqa: F401
        except ImportError:
            raise ImportError(import_err_msg)

        self._faiss_index = cast(faiss.Index, faiss_index)

    @classmethod
    def from_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
    ) -> "FaissVectorStore":
        persist_path = os.path.join(persist_dir, DEFAULT_PERSIST_FNAME)
        return cls.from_persist_path(persist_path=persist_path)

    @classmethod
    def from_persist_path(
        cls,
        persist_path: str,
    ) -> "FaissVectorStore":
        import faiss

        if not os.path.exists(persist_path):
            raise ValueError(f"No existing {__name__} found at {persist_path}.")

        logger.info(f"Loading {__name__} from {persist_path}.")
        faiss_index = faiss.read_index(persist_path)
        return cls(faiss_index=faiss_index)

    def add(
        self,
        embedding_results: List[NodeEmbeddingResult],
    ) -> List[str]:
        """Add embedding results to index.

        NOTE: in the Faiss vector store, we do not store text in Faiss.

        Args
            embedding_results: List[NodeEmbeddingResult]: list of embedding results

        """
        new_ids = []
        for result in embedding_results:
            text_embedding = result.embedding
            text_embedding_np = np.array(text_embedding, dtype="float32")[np.newaxis, :]
            new_id = str(self._faiss_index.ntotal)
            self._faiss_index.add(text_embedding_np)
            new_ids.append(new_id)
        return new_ids

    @property
    def client(self) -> Any:
        """Return the faiss index."""
        return self._faiss_index

    def persist(
        self,
        persist_path: str,
    ) -> None:
        """Save to file.

        This method saves the vector store to disk.

        Args:
            save_path (str): The save_path of the file.

        """
        import faiss

        dirpath = os.path.dirname(persist_path)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        faiss.write_index(self._faiss_index, persist_path)

    def delete(self, doc_id: str, **delete_kwargs: Any) -> None:
        """Delete a document.

        Args:
            doc_id (str): document id

        """
        raise NotImplementedError("Delete not yet implemented for Faiss index.")

    def query(
        self,
        query: VectorStoreQuery,
    ) -> VectorStoreQueryResult:
        """Query index for top k most similar nodes.

        Args:
            query_embedding (List[float]): query embedding
            similarity_top_k (int): top k most similar nodes

        """
        query_embedding = cast(List[float], query.query_embedding)
        query_embedding_np = np.array(query_embedding, dtype="float32")[np.newaxis, :]
        dists, indices = self._faiss_index.search(
            query_embedding_np, query.similarity_top_k
        )
        dists = [d for d in dists[0]]
        # if empty, then return an empty response
        if len(indices) == 0:
            return VectorStoreQueryResult(similarities=[], ids=[])

        # returned dimension is 1 x k
        node_idxs = list([str(i) for i in indices[0]])

        return VectorStoreQueryResult(similarities=dists, ids=node_idxs)
