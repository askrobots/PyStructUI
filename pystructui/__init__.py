"""
PyStructUI - Universal Data Structure to HTML Rendering Engine
Convert data structures to HTML for any Python web framework
"""

from .core import PresentationLayer, Renderer
from .renderers import BootstrapRenderer, TailwindRenderer, MaterialUIRenderer
from .integrations import flask_integration, django_integration

__version__ = "0.1.0"
__all__ = [
    'PresentationLayer',
    'Renderer',
    'BootstrapRenderer',
    'TailwindRenderer',
    'MaterialUIRenderer',
    'flask_integration',
    'django_integration'
]

# Quick start
def render(data, renderer='bootstrap'):
    """Quick render function for simple use cases"""
    pl = PresentationLayer()
    if renderer == 'bootstrap':
        pl.add_renderer('bootstrap', BootstrapRenderer())
    elif renderer == 'tailwind':
        pl.add_renderer('tailwind', TailwindRenderer())
    elif renderer == 'material':
        pl.add_renderer('material', MaterialUIRenderer())
    return pl.render(data, renderer)