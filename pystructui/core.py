"""
Core presentation layer engine
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json


class Renderer(ABC):
    """Base renderer class that all UI renderers must inherit from"""

    @abstractmethod
    def render(self, data: Dict[str, Any]) -> str:
        """Render data structure to HTML string"""
        pass

    @abstractmethod
    def render_component(self, component: Dict[str, Any]) -> str:
        """Render a single component"""
        pass


class PresentationLayer:
    """Main presentation layer that manages renderers and rendering"""

    def __init__(self):
        self.renderers = {}
        self.default_renderer = None

    def add_renderer(self, name: str, renderer: Renderer):
        """Register a renderer"""
        self.renderers[name] = renderer
        if not self.default_renderer:
            self.default_renderer = name

    def render(self, data: Dict[str, Any], renderer: Optional[str] = None) -> str:
        """Render data using specified or default renderer"""
        renderer_name = renderer or self.default_renderer
        if not renderer_name or renderer_name not in self.renderers:
            raise ValueError(f"Renderer '{renderer_name}' not found")
        return self.renderers[renderer_name].render(data)

    def render_json(self, data: Dict[str, Any]) -> str:
        """Render data as JSON (useful for APIs)"""
        return json.dumps(data, indent=2)

    def get_renderers(self) -> List[str]:
        """Get list of available renderers"""
        return list(self.renderers.keys())