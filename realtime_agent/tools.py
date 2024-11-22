import abc
import json
import logging
from typing import Any, Callable, assert_never

from attr import dataclass
from pydantic import BaseModel

from .logger import setup_logger

# Set up the logger with color and timestamp support
logger = setup_logger(name=__name__, log_level=logging.INFO)


@dataclass(frozen=True, kw_only=True)
class LocalFunctionToolDeclaration:
    """Declaration of a tool that can be called by the model, and runs a function locally on the tool context."""

    name: str
    description: str
    parameters: dict[str, Any]
    function: Callable[..., Any]

    def model_description(self) -> dict[str, Any]:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


@dataclass(frozen=True, kw_only=True)
class PassThroughFunctionToolDeclaration:
    """Declaration of a tool that can be called by the model."""

    name: str
    description: str
    parameters: dict[str, Any]

    def model_description(self) -> dict[str, Any]:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


ToolDeclaration = LocalFunctionToolDeclaration | PassThroughFunctionToolDeclaration


@dataclass(frozen=True, kw_only=True)
class LocalToolCallExecuted:
    json_encoded_output: str


@dataclass(frozen=True, kw_only=True)
class ShouldPassThroughToolCall:
    decoded_function_args: dict[str, Any]


ExecuteToolCallResult = LocalToolCallExecuted | ShouldPassThroughToolCall


class ToolContext(abc.ABC):
    _tool_declarations: dict[str, ToolDeclaration]

    def __init__(self) -> None:
        # TODO should be an ordered dict
        self._tool_declarations = {}

    def register_function(
        self,
        *,
        name: str,
        description: str = "",
        parameters: dict[str, Any],
        fn: Callable[..., Any],
    ) -> None:
        self._tool_declarations[name] = LocalFunctionToolDeclaration(
            name=name, description=description, parameters=parameters, function=fn
        )

    def register_client_function(
        self,
        *,
        name: str,
        description: str = "",
        parameters: dict[str, Any],
    ) -> None:
        self._tool_declarations[name] = PassThroughFunctionToolDeclaration(
            name=name, description=description, parameters=parameters
        )

    async def execute_tool(
        self, tool_name: str, encoded_function_args: str
    ) -> ExecuteToolCallResult | None:
        tool = self._tool_declarations.get(tool_name)
        if not tool:
            return None

        args = json.loads(encoded_function_args)
        assert isinstance(args, dict)

        if isinstance(tool, LocalFunctionToolDeclaration):
            logger.info(f"Executing tool {tool_name} with args {args}")
            result = await tool.function(**args)
            logger.info(f"Tool {tool_name} executed with result {result}")
            return LocalToolCallExecuted(json_encoded_output=json.dumps(result))

        if isinstance(tool, PassThroughFunctionToolDeclaration):
            return ShouldPassThroughToolCall(decoded_function_args=args)

        assert_never(tool)

    def model_description(self) -> list[dict[str, Any]]:
        return [v.model_description() for v in self._tool_declarations.values()]


class ClientToolCallResponse(BaseModel):
    tool_call_id: str
    result: dict[str, Any] | str | float | int | bool | None = None
