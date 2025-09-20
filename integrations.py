"""
Framework integrations for PyStructUI
"""

from functools import wraps
from typing import Dict, Any, Optional
from .core import PresentationLayer
from .renderers import BootstrapRenderer


# Flask Integration
def flask_integration(app, renderer='bootstrap'):
    """
    Integrate PyStructUI with Flask app

    Usage:
        from flask import Flask
        from pystructui import flask_integration

        app = Flask(__name__)
        ui = flask_integration(app)

        @app.route('/')
        @ui.render
        def index():
            return {
                'type': 'page',
                'title': 'My Flask App',
                'components': [
                    {'type': 'hero', 'title': 'Welcome!'},
                    {'type': 'card', 'title': 'Hello', 'body': 'From PyStructUI'}
                ]
            }
    """
    pl = PresentationLayer()

    # Add default renderer
    if renderer == 'bootstrap':
        pl.add_renderer('bootstrap', BootstrapRenderer())

    class FlaskUI:
        def __init__(self, presentation_layer):
            self.pl = presentation_layer

        def render(self, f):
            """Decorator to render data structures as HTML"""
            @wraps(f)
            def decorated_function(*args, **kwargs):
                data = f(*args, **kwargs)
                if isinstance(data, dict):
                    return self.pl.render(data)
                return data
            return decorated_function

        def component(self, component_data: Dict[str, Any]):
            """Render a single component"""
            return self.pl.render(component_data)

    return FlaskUI(pl)


# Django Integration
def django_integration(renderer='bootstrap'):
    """
    Integrate PyStructUI with Django views

    Usage in views.py:
        from django.http import HttpResponse
        from pystructui import django_integration

        ui = django_integration()

        def index(request):
            data = {
                'type': 'page',
                'title': 'My Django App',
                'components': [
                    {'type': 'navbar', 'brand': 'Django + PyStructUI'},
                    {'type': 'hero', 'title': 'Welcome!'},
                ]
            }
            return HttpResponse(ui.render(data))

    Or as a class-based view:
        from django.views import View

        class IndexView(View):
            def get(self, request):
                data = {...}
                return HttpResponse(ui.render(data))
    """
    pl = PresentationLayer()

    if renderer == 'bootstrap':
        pl.add_renderer('bootstrap', BootstrapRenderer())

    class DjangoUI:
        def __init__(self, presentation_layer):
            self.pl = presentation_layer

        def render(self, data: Dict[str, Any], renderer: Optional[str] = None) -> str:
            """Render data structure to HTML"""
            return self.pl.render(data, renderer)

        def render_response(self, data: Dict[str, Any], renderer: Optional[str] = None):
            """Render and return HttpResponse"""
            from django.http import HttpResponse
            html = self.render(data, renderer)
            return HttpResponse(html)

        def template_view(self, data_func):
            """Decorator for Django class-based views"""
            from django.http import HttpResponse
            from django.views import View

            class UIView(View):
                def get(self, request, *args, **kwargs):
                    data = data_func(request, *args, **kwargs)
                    return HttpResponse(self.pl.render(data))

            return UIView

    return DjangoUI(pl)


# FastAPI Integration
def fastapi_integration(renderer='bootstrap'):
    """
    Integrate PyStructUI with FastAPI

    Usage:
        from fastapi import FastAPI
        from fastapi.responses import HTMLResponse
        from pystructui import fastapi_integration

        app = FastAPI()
        ui = fastapi_integration()

        @app.get("/", response_class=HTMLResponse)
        async def index():
            data = {
                'type': 'page',
                'title': 'FastAPI App',
                'components': [...]
            }
            return ui.render(data)
    """
    pl = PresentationLayer()

    if renderer == 'bootstrap':
        pl.add_renderer('bootstrap', BootstrapRenderer())

    class FastAPIUI:
        def __init__(self, presentation_layer):
            self.pl = presentation_layer

        def render(self, data: Dict[str, Any], renderer: Optional[str] = None) -> str:
            """Render data structure to HTML"""
            return self.pl.render(data, renderer)

        def response(self, data: Dict[str, Any], renderer: Optional[str] = None):
            """Return FastAPI HTMLResponse"""
            from fastapi.responses import HTMLResponse
            html = self.render(data, renderer)
            return HTMLResponse(content=html)

    return FastAPIUI(pl)