"""Simple reader that turns an iterable of strings into a list of Documents."""
from typing import List

from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document


class StringIterableReader(BaseReader):
    """String Iterable Reader.

    Gets a list of documents, given an iterable (e.g. list) of strings.

    Example:
        .. code-block:: python

            from gpt_index import StringIterableReader, GPTTreeIndex

            documents = StringIterableReader().load_data(
                texts=["I went to the store", "I bought an apple"])
            index = GPTTreeIndex.from_documents(documents)
            query_engine = index.as_query_engine()
            query_engine.query("what did I buy?")

            # response should be something like "You bought an apple."
    """

    def load_data(self, texts: List[str]) -> List[Document]:
        """Load the data."""
        results = []
        for text in texts:
            results.append(Document(text))

        return results
