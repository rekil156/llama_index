from typing import List, Optional, Sequence
from gpt_index.data_structs.node_v2 import NodeWithScore
from gpt_index.indices.query.base import BaseQueryEngine
from gpt_index.indices.query.query_transform.base import BaseQueryTransform
from gpt_index.indices.query.schema import QueryBundle
from gpt_index.response.schema import RESPONSE_TYPE


class TransformQueryEngine(BaseQueryEngine):
    """Transform query engine.

    Applies a query transform to a query bundle before passing
        it to a query engine.

    Args:
        query_engine (BaseQueryEngine): A query engine object.
        query_transform (BaseQueryTransform): A query transform object.
        transform_extra_info (Optional[dict]): Extra info to pass to the
            query transform.

    """

    def __init__(
        self,
        query_engine: BaseQueryEngine,
        query_transform: BaseQueryTransform,
        transform_extra_info: Optional[dict] = None,
    ) -> None:
        self._query_engine = query_engine
        self._query_transform = query_transform
        self._transform_extra_info = transform_extra_info

    def retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        query_bundle = self._query_transform.run(
            query_bundle, extra_info=self._transform_extra_info
        )
        return self._query_engine.retrieve(query_bundle)

    def synthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        query_bundle = self._query_transform.run(
            query_bundle, extra_info=self._transform_extra_info
        )
        return self._query_engine.synthesize(
            query_bundle=query_bundle,
            nodes=nodes,
            additional_source_nodes=additional_source_nodes,
        )

    async def asynthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[Sequence[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        query_bundle = self._query_transform.run(
            query_bundle, extra_info=self._transform_extra_info
        )
        return await self._query_engine.asynthesize(
            query_bundle=query_bundle,
            nodes=nodes,
            additional_source_nodes=additional_source_nodes,
        )

    def _query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        """Answer a query."""
        query_bundle = self._query_transform.run(
            query_bundle, extra_info=self._transform_extra_info
        )
        return self._query_engine.query(query_bundle)

    async def _aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        """Answer a query."""
        query_bundle = self._query_transform.run(
            query_bundle, extra_info=self._transform_extra_info
        )
        return await self._query_engine.aquery(query_bundle)
