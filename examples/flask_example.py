"""
Flask + PyStructUI Example
Shows how to use data structures instead of HTML templates
"""

from flask import Flask, request, redirect, url_for
from pystructui import flask_integration

app = Flask(__name__)
ui = flask_integration(app, renderer='bootstrap')

# Simulate a database
todos = []


@app.route('/')
@ui.render
def index():
    """Home page using data structures instead of HTML"""
    return {
        'type': 'page',
        'title': 'Flask + PyStructUI Demo',
        'components': [
            {
                'type': 'navbar',
                'brand': 'Todo App',
                'links': [
                    {'text': 'Home', 'url': '/'},
                    {'text': 'About', 'url': '/about'},
                ]
            },
            {
                'type': 'hero',
                'title': 'Welcome to PyStructUI',
                'subtitle': 'Build UIs with data structures, not HTML',
                'variant': 'primary'
            },
            {
                'type': 'card',
                'title': '📝 Todo List',
                'body': {
                    'type': 'raw',
                    'content': _render_todo_list()
                },
                'footer': {
                    'type': 'button',
                    'text': 'Add Todo',
                    'variant': 'success',
                    'onclick': 'location.href="/add"'
                }
            }
        ]
    }


def _render_todo_list():
    """Render todo list as HTML"""
    if not todos:
        return '<p>No todos yet. Add one!</p>'

    items = ''.join([
        f'<li class="list-group-item d-flex justify-content-between">'
        f'{todo["text"]}'
        f'<a href="/delete/{i}" class="btn btn-sm btn-danger">Delete</a>'
        f'</li>'
        for i, todo in enumerate(todos)
    ])

    return f'<ul class="list-group">{items}</ul>'


@app.route('/add')
@ui.render
def add_todo_form():
    """Add todo form - pure data structure"""
    return {
        'type': 'page',
        'title': 'Add Todo',
        'components': [
            {
                'type': 'navbar',
                'brand': 'Todo App',
            },
            {
                'type': 'card',
                'title': 'Add New Todo',
                'body': {
                    'type': 'form',
                    'method': 'POST',
                    'action': '/add',
                    'fields': [
                        {
                            'type': 'text',
                            'name': 'todo_text',
                            'label': 'Todo Text',
                            'placeholder': 'Enter your todo...',
                            'required': True
                        }
                    ]
                }
            }
        ]
    }


@app.route('/add', methods=['POST'])
def add_todo_post():
    """Handle form submission"""
    todo_text = request.form.get('todo_text')
    if todo_text:
        todos.append({'text': todo_text})
    return redirect(url_for('index'))


@app.route('/delete/<int:index>')
def delete_todo(index):
    """Delete a todo"""
    if 0 <= index < len(todos):
        todos.pop(index)
    return redirect(url_for('index'))


@app.route('/about')
@ui.render
def about():
    """About page demonstrating different components"""
    return {
        'type': 'page',
        'title': 'About PyStructUI',
        'components': [
            {
                'type': 'navbar',
                'brand': 'Todo App',
                'links': [
                    {'text': 'Home', 'url': '/'},
                    {'text': 'About', 'url': '/about'},
                ]
            },
            {
                'type': 'grid',
                'columns': 3,
                'items': [
                    {
                        'type': 'card',
                        'title': '🚀 Fast',
                        'body': 'No template compilation, just data transformation'
                    },
                    {
                        'type': 'card',
                        'title': '🎨 Flexible',
                        'body': 'Switch UI frameworks without changing code'
                    },
                    {
                        'type': 'card',
                        'title': '🔧 Simple',
                        'body': 'Define UI as data structures, not HTML'
                    }
                ]
            },
            {
                'type': 'alert',
                'message': 'This entire app has ZERO HTML templates!',
                'variant': 'success',
                'dismissible': True
            }
        ]
    }


if __name__ == '__main__':
    app.run(debug=True, port=5000)