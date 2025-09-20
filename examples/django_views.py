"""
Django + PyStructUI Example
Shows how to use data structures instead of Django templates

Add to your Django project's views.py:
"""

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from pystructui import django_integration

# Initialize PyStructUI
ui = django_integration(renderer='bootstrap')

# Simulate a database (in real app, use Django models)
todos = []


def index(request):
    """Home page using data structures instead of templates"""
    data = {
        'type': 'page',
        'title': 'Django + PyStructUI Demo',
        'components': [
            {
                'type': 'navbar',
                'brand': 'Django Todo',
                'links': [
                    {'text': 'Home', 'url': '/'},
                    {'text': 'Admin', 'url': '/admin/'},
                    {'text': 'API', 'url': '/api/'},
                ]
            },
            {
                'type': 'hero',
                'title': 'Django Without Templates!',
                'subtitle': 'Use data structures instead of HTML',
                'variant': 'success'
            },
            _render_todo_section()
        ]
    }

    return ui.render_response(data)


def _render_todo_section():
    """Generate todo section as data structure"""
    todo_items = []

    for i, todo in enumerate(todos):
        todo_items.append({
            'type': 'raw',
            'content': f"""
            <div class="list-group-item d-flex justify-content-between align-items-center">
                <span>{todo['text']}</span>
                <span>
                    <span class="badge bg-primary rounded-pill me-2">{todo.get('category', 'general')}</span>
                    <a href="/delete/{i}" class="btn btn-sm btn-danger">Delete</a>
                </span>
            </div>
            """
        })

    return {
        'type': 'card',
        'title': '📋 Your Todos',
        'body': {
            'type': 'raw',
            'content': f"""
            <form method="POST" action="/add" class="mb-3">
                <div class="input-group">
                    <input type="text" name="todo_text" class="form-control" placeholder="Add a new todo..." required>
                    <select name="category" class="form-select" style="max-width: 150px;">
                        <option value="personal">Personal</option>
                        <option value="work">Work</option>
                        <option value="urgent">Urgent</option>
                    </select>
                    <button class="btn btn-primary" type="submit">Add</button>
                </div>
            </form>
            <div class="list-group">
                {''.join([ui.render(item) for item in todo_items]) if todo_items else '<p class="text-muted">No todos yet!</p>'}
            </div>
            """
        }
    }


class TodoAPIView(View):
    """API endpoint returning data structures as JSON"""

    def get(self, request):
        """Return todos as data structure"""
        data = {
            'type': 'api_response',
            'status': 'success',
            'data': {
                'todos': todos,
                'count': len(todos)
            }
        }

        # Could return as JSON or HTML
        if request.GET.get('format') == 'html':
            return ui.render_response(self._wrap_in_page(data))

        import json
        return HttpResponse(
            json.dumps(data),
            content_type='application/json'
        )

    def _wrap_in_page(self, data):
        """Wrap API response in page structure"""
        return {
            'type': 'page',
            'title': 'API Response',
            'components': [
                {'type': 'navbar', 'brand': 'Django API'},
                {
                    'type': 'card',
                    'title': 'API Response',
                    'body': {
                        'type': 'raw',
                        'content': f'<pre class="bg-dark text-white p-3">{import.json.dumps(data, indent=2)}</pre>'
                    }
                }
            ]
        }


def add_todo(request):
    """Handle adding a todo"""
    if request.method == 'POST':
        todo_text = request.POST.get('todo_text')
        category = request.POST.get('category', 'general')
        if todo_text:
            todos.append({
                'text': todo_text,
                'category': category
            })

    return redirect('/')


def delete_todo(request, index):
    """Delete a todo by index"""
    if 0 <= index < len(todos):
        todos.pop(index)
    return redirect('/')


# Class-based view example
class DashboardView(View):
    """Dashboard using class-based views"""

    def get(self, request):
        stats = self._calculate_stats()

        data = {
            'type': 'page',
            'title': 'Dashboard',
            'components': [
                {
                    'type': 'navbar',
                    'brand': 'Dashboard',
                },
                {
                    'type': 'grid',
                    'columns': 4,
                    'items': [
                        self._stat_card('Total Todos', stats['total'], 'primary'),
                        self._stat_card('Personal', stats['personal'], 'info'),
                        self._stat_card('Work', stats['work'], 'success'),
                        self._stat_card('Urgent', stats['urgent'], 'danger'),
                    ]
                },
                {
                    'type': 'table',
                    'headers': ['Task', 'Category', 'Actions'],
                    'rows': [
                        [todo['text'], todo.get('category', 'general'), f'<a href="/delete/{i}">Delete</a>']
                        for i, todo in enumerate(todos)
                    ]
                }
            ]
        }

        return ui.render_response(data)

    def _calculate_stats(self):
        """Calculate todo statistics"""
        stats = {
            'total': len(todos),
            'personal': len([t for t in todos if t.get('category') == 'personal']),
            'work': len([t for t in todos if t.get('category') == 'work']),
            'urgent': len([t for t in todos if t.get('category') == 'urgent']),
        }
        return stats

    def _stat_card(self, title, value, variant):
        """Generate a statistics card"""
        return {
            'type': 'card',
            'body': {
                'type': 'raw',
                'content': f"""
                <h6 class="text-muted">{title}</h6>
                <h2 class="text-{variant}">{value}</h2>
                """
            }
        }


# URLs configuration (add to urls.py)
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add_todo, name='add_todo'),
    path('delete/<int:index>', views.delete_todo, name='delete_todo'),
    path('api/', views.TodoAPIView.as_view(), name='api'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
"""