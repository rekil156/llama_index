"""LlamaIndex toolkit."""

from typing import List

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool
from pydantic import Field

from gpt_index.langchain_helpers.agents.tools import (
    IndexToolConfig,
    LlamaIndexTool,
)


class LlamaToolkit(BaseToolkit):
    """Toolkit for interacting with Llama indices."""

    index_configs: List[IndexToolConfig] = Field(default_factory=list)

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        index_tools: List[BaseTool] = [
            LlamaIndexTool.from_tool_config(tool_config=tool_config)
            for tool_config in self.index_configs
        ]

        return index_tools
