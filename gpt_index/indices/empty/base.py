"""Empty index.

An index that doesn't contain any documents. Can only be used for
pure LLM calls.

"""

from typing import Any, Optional, Sequence

from gpt_index.data_structs.data_structs_v2 import EmptyIndex
from gpt_index.data_structs.node_v2 import Node
from gpt_index.indices.base import BaseGPTIndex
from gpt_index.indices.base_retriever import BaseRetriever
from gpt_index.indices.service_context import ServiceContext


class GPTEmptyIndex(BaseGPTIndex[EmptyIndex]):
    """GPT Empty Index.

    An index that doesn't contain any documents. Used for
    pure LLM calls.
    NOTE: this exists because an empty index it allows certain properties,
    such as the ability to be composed with other indices + token
    counting + others.

    """

    index_struct_cls = EmptyIndex

    def __init__(
        self,
        index_struct: Optional[EmptyIndex] = None,
        service_context: Optional[ServiceContext] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize params."""
        super().__init__(
            nodes=None,
            index_struct=index_struct or EmptyIndex(),
            service_context=service_context,
            **kwargs,
        )

    def as_retriever(self, **kwargs: Any) -> BaseRetriever:
        # NOTE: lazy import
        from gpt_index.indices.empty.retrievers import EmptyIndexRetriever

        return EmptyIndexRetriever(self)

    def _build_index_from_nodes(self, nodes: Sequence[Node]) -> EmptyIndex:
        """Build the index from documents.

        Args:
            documents (List[BaseDocument]): A list of documents.

        Returns:
            IndexList: The created list index.
        """
        del nodes  # Unused
        index_struct = EmptyIndex()
        return index_struct

    def _insert(self, nodes: Sequence[Node], **insert_kwargs: Any) -> None:
        """Insert a document."""
        del nodes  # Unused
        raise NotImplementedError("Cannot insert into an empty index.")

    def _delete(self, doc_id: str, **delete_kwargs: Any) -> None:
        """Delete a document."""
        raise NotImplementedError("Cannot delete from an empty index.")
