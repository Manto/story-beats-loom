"""Base data models."""

from pydantic import BaseModel, Field


class NodeLink(BaseModel):
    link_to: str = Field(json_schema_extra=dict(title="Name of node this links to"))
    text: str = Field(default="", json_schema_extra=dict(title="Text describing the link"))


class Node(BaseModel):
    name: str = Field(json_schema_extra=dict(title="Name of node"))
    text: str = Field(default="", json_schema_extra=dict(title="Generated node text"))
    links: dict[str, NodeLink] = Field(default_factory=list)


class InteractiveDocument(BaseModel):
    title: str = "Untitled"
    nodes: dict[str, Node] = Field(default_factory=list)
