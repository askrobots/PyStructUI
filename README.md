# PyStructUI 🎨

**Transform data structures into beautiful UIs for any Python web framework**

PyStructUI is a universal presentation layer that lets you build web UIs using pure data structures instead of HTML templates. Works with Flask, Django, FastAPI, and any Python web framework.

## Why PyStructUI?

Traditional web development:
```html
<!-- 100s of HTML template files -->
<div class="card">
  <div class="card-header">{{ title }}</div>
  <div class="card-body">{{ content }}</div>
</div>
```

With PyStructUI:
```python
{'type': 'card', 'title': 'Hello', 'body': 'World'}
```

**Benefits:**
- ✅ **No HTML templates** - Define UI as data
- ✅ **Framework agnostic** - Works with Flask, Django, FastAPI, etc.
- ✅ **UI framework swappable** - Switch between Bootstrap, Tailwind, Material with one line
- ✅ **90% less code** - Data structures are more concise than HTML
- ✅ **AI-friendly** - LLMs understand data better than HTML
- ✅ **Testable** - Test data structures, not HTML strings

## Installation

```bash
pip install pystructui
```

Or install with framework support:
```bash
pip install pystructui[flask]
pip install pystructui[django]
pip install pystructui[fastapi]
```

## Quick Start

### Basic Usage

```python
from pystructui import render

# Define UI as data
ui_data = {
    'type': 'page',
    'title': 'My App',
    'components': [
        {'type': 'navbar', 'brand': 'PyStructUI'},
        {'type': 'hero', 'title': 'Welcome!', 'subtitle': 'Build UIs with data'},
        {'type': 'button', 'text': 'Get Started', 'variant': 'primary'}
    ]
}

# Render to HTML
html = render(ui_data)
```

### Flask Integration

```python
from flask import Flask
from pystructui import flask_integration

app = Flask(__name__)
ui = flask_integration(app)

@app.route('/')
@ui.render
def index():
    return {
        'type': 'page',
        'title': 'Flask App',
        'components': [
            {'type': 'card', 'title': 'Hello Flask!', 'body': 'No templates needed!'}
        ]
    }
```

### Django Integration

```python
# views.py
from pystructui import django_integration

ui = django_integration()

def index(request):
    data = {
        'type': 'page',
        'title': 'Django App',
        'components': [
            {'type': 'navbar', 'brand': 'Django + PyStructUI'},
            {'type': 'hero', 'title': 'No templates!'}
        ]
    }
    return ui.render_response(data)
```

### FastAPI Integration

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pystructui import fastapi_integration

app = FastAPI()
ui = fastapi_integration()

@app.get("/", response_class=HTMLResponse)
async def index():
    data = {
        'type': 'page',
        'components': [{'type': 'card', 'title': 'FastAPI + PyStructUI'}]
    }
    return ui.render(data)
```

## Component Reference

### Page Structure

```python
{
    'type': 'page',
    'title': 'Page Title',
    'components': [...]  # List of components
}
```

### Navigation

```python
{
    'type': 'navbar',
    'brand': 'My App',
    'links': [
        {'text': 'Home', 'url': '/'},
        {'text': 'About', 'url': '/about'}
    ]
}
```

### Cards

```python
{
    'type': 'card',
    'title': 'Card Title',
    'body': 'Card content or nested component',
    'footer': {'type': 'button', 'text': 'Action'}
}
```

### Forms

```python
{
    'type': 'form',
    'method': 'POST',
    'action': '/submit',
    'fields': [
        {
            'type': 'text',
            'name': 'username',
            'label': 'Username',
            'required': True
        },
        {
            'type': 'textarea',
            'name': 'message',
            'label': 'Message'
        }
    ]
}
```

### Tables

```python
{
    'type': 'table',
    'headers': ['Name', 'Email', 'Status'],
    'rows': [
        ['John', 'john@example.com', 'Active'],
        ['Jane', 'jane@example.com', 'Pending']
    ]
}
```

### Grids

```python
{
    'type': 'grid',
    'columns': 3,
    'items': [
        {'type': 'card', 'title': 'Card 1'},
        {'type': 'card', 'title': 'Card 2'},
        {'type': 'card', 'title': 'Card 3'}
    ]
}
```

### Alerts

```python
{
    'type': 'alert',
    'message': 'Operation successful!',
    'variant': 'success',  # success, danger, warning, info
    'dismissible': True
}
```

## Switching UI Frameworks

```python
from pystructui import PresentationLayer
from pystructui.renderers import BootstrapRenderer, TailwindRenderer

pl = PresentationLayer()

# Use Bootstrap
pl.add_renderer('bootstrap', BootstrapRenderer())
html = pl.render(data, 'bootstrap')

# Switch to Tailwind - same data, different output!
pl.add_renderer('tailwind', TailwindRenderer())
html = pl.render(data, 'tailwind')
```

## Custom Renderers

Create your own renderer for any UI framework:

```python
from pystructui import Renderer

class CustomRenderer(Renderer):
    def render(self, data):
        # Your rendering logic
        return html

    def render_component(self, component):
        # Component rendering
        return html

# Use it
pl.add_renderer('custom', CustomRenderer())
```

## Advanced Features

### Nested Components

Components can be nested infinitely:

```python
{
    'type': 'card',
    'body': {
        'type': 'grid',
        'columns': 2,
        'items': [
            {'type': 'button', 'text': 'Yes'},
            {'type': 'button', 'text': 'No'}
        ]
    }
}
```

### Raw HTML

When needed, include raw HTML:

```python
{
    'type': 'raw',
    'content': '<custom-element>Custom HTML</custom-element>'
}
```

### Dynamic Rendering

Use Python to generate dynamic UIs:

```python
def dashboard(user_data):
    return {
        'type': 'grid',
        'columns': 3,
        'items': [
            {
                'type': 'card',
                'title': metric['name'],
                'body': metric['value']
            }
            for metric in user_data.metrics
        ]
    }
```

## Why Data Structures?

1. **Simplicity** - No template syntax to learn
2. **Portability** - Same structure works with any renderer
3. **Testability** - Assert on data, not HTML strings
4. **AI-friendly** - LLMs excel at data transformation
5. **Version control** - Data diffs are cleaner than HTML diffs
6. **Performance** - No template compilation overhead

## Comparison

### Traditional Django Template
```html
{% extends "base.html" %}
{% block content %}
<div class="container">
  <div class="row">
    {% for item in items %}
    <div class="col-md-4">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">{{ item.title }}</h5>
          <p class="card-text">{{ item.description }}</p>
          <a href="{{ item.url }}" class="btn btn-primary">View</a>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
{% endblock %}
```

### With PyStructUI
```python
{
    'type': 'grid',
    'columns': 3,
    'items': [
        {
            'type': 'card',
            'title': item['title'],
            'body': item['description'],
            'footer': {'type': 'button', 'text': 'View', 'url': item['url']}
        }
        for item in items
    ]
}
```

## Real-World Example

Building a complete todo app:

```python
from flask import Flask
from pystructui import flask_integration

app = Flask(__name__)
ui = flask_integration(app)

todos = []

@app.route('/')
@ui.render
def index():
    return {
        'type': 'page',
        'components': [
            {'type': 'navbar', 'brand': 'Todo App'},
            {
                'type': 'card',
                'title': 'My Todos',
                'body': {
                    'type': 'table',
                    'headers': ['Task', 'Status'],
                    'rows': [[t['text'], t['status']] for t in todos]
                }
            }
        ]
    }

# That's it! No templates needed!
```

## Contributing

We welcome contributions! PyStructUI is designed to be extensible:

- Add new component types
- Create renderers for more UI frameworks
- Add framework integrations
- Improve documentation

## License

MIT License - Use PyStructUI in any project!

## Philosophy

> "Code is about data structures. UI should be too."

PyStructUI embraces the fundamental truth that all programming is data transformation. Instead of mixing logic with presentation through templates, we keep them separate: logic produces data, renderers transform data to UI.

This is the future of web development - where humans define intent through data structures, and machines handle the implementation details.

## Support

- GitHub: [github.com/askrobots/PyStructUI](https://github.com/askrobots/PyStructUI)
- Documentation: [pystructui.readthedocs.io](https://pystructui.readthedocs.io)
- PyPI: [pypi.org/project/pystructui](https://pypi.org/project/pystructui)

---

Built with ❤️ by the DBBasic team. Part of the movement to make web development simpler, faster, and more enjoyable.