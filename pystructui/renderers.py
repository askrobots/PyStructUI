"""
Built-in renderers for different UI frameworks
"""

from typing import Dict, Any
from .core import Renderer


class BootstrapRenderer(Renderer):
    """Bootstrap 5 renderer"""

    def render(self, data: Dict[str, Any]) -> str:
        """Render complete page with Bootstrap"""
        if data.get('type') == 'page':
            return self._render_page(data)
        return self.render_component(data)

    def render_component(self, data: Dict[str, Any]) -> str:
        """Render individual component"""
        component_type = data.get('type', 'div')

        # Map component types to render methods
        renderers = {
            'navbar': self._render_navbar,
            'card': self._render_card,
            'button': self._render_button,
            'form': self._render_form,
            'table': self._render_table,
            'alert': self._render_alert,
            'modal': self._render_modal,
            'grid': self._render_grid,
            'hero': self._render_hero,
            'breadcrumb': self._render_breadcrumb,
            'raw': lambda d: d.get('content', ''),
        }

        renderer = renderers.get(component_type, self._render_div)
        return renderer(data)

    def _render_page(self, data: Dict[str, Any]) -> str:
        """Render full HTML page"""
        title = data.get('title', 'PyStructUI App')
        components = data.get('components', [])

        components_html = ''.join([
            self.render_component(c) for c in components
        ])

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css">
</head>
<body>
    {components_html}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

    def _render_navbar(self, data: Dict[str, Any]) -> str:
        """Render Bootstrap navbar"""
        brand = data.get('brand', 'App')
        links = data.get('links', [])

        nav_links = ''.join([
            f'<li class="nav-item"><a class="nav-link" href="{link.get("url", "#")}">{link.get("text", "Link")}</a></li>'
            for link in links
        ])

        return f"""
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">{brand}</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        {nav_links}
                    </ul>
                </div>
            </div>
        </nav>"""

    def _render_card(self, data: Dict[str, Any]) -> str:
        """Render Bootstrap card"""
        title = data.get('title', '')
        body = data.get('body', '')
        footer = data.get('footer')

        body_html = body if isinstance(body, str) else self.render_component(body)

        footer_html = ''
        if footer:
            if isinstance(footer, dict):
                footer_html = f'<div class="card-footer">{self.render_component(footer)}</div>'
            else:
                footer_html = f'<div class="card-footer">{footer}</div>'

        return f"""
        <div class="card">
            {f'<div class="card-header"><h5>{title}</h5></div>' if title else ''}
            <div class="card-body">{body_html}</div>
            {footer_html}
        </div>"""

    def _render_button(self, data: Dict[str, Any]) -> str:
        """Render Bootstrap button"""
        text = data.get('text', 'Button')
        variant = data.get('variant', 'primary')
        size = data.get('size', '')
        onclick = data.get('onclick', '')

        size_class = f'btn-{size}' if size else ''
        onclick_attr = f'onclick="{onclick}"' if onclick else ''

        return f'<button class="btn btn-{variant} {size_class}" {onclick_attr}>{text}</button>'

    def _render_form(self, data: Dict[str, Any]) -> str:
        """Render Bootstrap form"""
        fields = data.get('fields', [])
        method = data.get('method', 'POST')
        action = data.get('action', '#')

        fields_html = ''.join([self._render_form_field(f) for f in fields])

        return f"""
        <form method="{method}" action="{action}">
            {fields_html}
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>"""

    def _render_form_field(self, field: Dict[str, Any]) -> str:
        """Render form field"""
        field_type = field.get('type', 'text')
        name = field.get('name', '')
        label = field.get('label', '')
        placeholder = field.get('placeholder', '')
        required = 'required' if field.get('required') else ''

        if field_type == 'textarea':
            return f"""
            <div class="mb-3">
                <label for="{name}" class="form-label">{label}</label>
                <textarea class="form-control" id="{name}" name="{name}" placeholder="{placeholder}" {required}></textarea>
            </div>"""

        return f"""
        <div class="mb-3">
            <label for="{name}" class="form-label">{label}</label>
            <input type="{field_type}" class="form-control" id="{name}" name="{name}" placeholder="{placeholder}" {required}>
        </div>"""

    def _render_table(self, data: Dict[str, Any]) -> str:
        """Render Bootstrap table"""
        headers = data.get('headers', [])
        rows = data.get('rows', [])

        header_html = ''.join([f'<th>{h}</th>' for h in headers])
        rows_html = ''.join([
            '<tr>' + ''.join([f'<td>{cell}</td>' for cell in row]) + '</tr>'
            for row in rows
        ])

        return f"""
        <table class="table table-striped table-hover">
            <thead><tr>{header_html}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>"""

    def _render_alert(self, data: Dict[str, Any]) -> str:
        """Render Bootstrap alert"""
        message = data.get('message', '')
        variant = data.get('variant', 'info')
        dismissible = data.get('dismissible', False)

        dismiss_html = ''
        if dismissible:
            dismiss_html = '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>'

        return f"""
        <div class="alert alert-{variant} {'alert-dismissible fade show' if dismissible else ''}" role="alert">
            {message}
            {dismiss_html}
        </div>"""

    def _render_modal(self, data: Dict[str, Any]) -> str:
        """Render Bootstrap modal"""
        modal_id = data.get('id', 'modal')
        title = data.get('title', 'Modal')
        body = data.get('body', '')

        body_html = body if isinstance(body, str) else self.render_component(body)

        return f"""
        <div class="modal fade" id="{modal_id}" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">{body_html}</div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary">Save changes</button>
                    </div>
                </div>
            </div>
        </div>"""

    def _render_grid(self, data: Dict[str, Any]) -> str:
        """Render Bootstrap grid"""
        columns = data.get('columns', 3)
        items = data.get('items', [])

        items_html = ''.join([
            f'<div class="col">{self.render_component(item)}</div>'
            for item in items
        ])

        return f"""
        <div class="container">
            <div class="row row-cols-1 row-cols-md-{columns} g-4">
                {items_html}
            </div>
        </div>"""

    def _render_hero(self, data: Dict[str, Any]) -> str:
        """Render hero section"""
        title = data.get('title', '')
        subtitle = data.get('subtitle', '')
        variant = data.get('variant', 'primary')

        return f"""
        <div class="bg-{variant} text-white text-center py-5">
            <div class="container">
                <h1 class="display-4">{title}</h1>
                <p class="lead">{subtitle}</p>
            </div>
        </div>"""

    def _render_breadcrumb(self, data: Dict[str, Any]) -> str:
        """Render breadcrumb navigation"""
        items = data.get('items', [])

        breadcrumb_items = ''.join([
            f'<li class="breadcrumb-item {"active" if item.get("active") else ""}"><a href="{item.get("url", "#")}">{item.get("text", "")}</a></li>'
            if not item.get('active') else
            f'<li class="breadcrumb-item active">{item.get("text", "")}</li>'
            for item in items
        ])

        return f"""
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                {breadcrumb_items}
            </ol>
        </nav>"""

    def _render_div(self, data: Dict[str, Any]) -> str:
        """Fallback div renderer"""
        content = data.get('content', '')
        return f'<div>{content}</div>'


class TailwindRenderer(Renderer):
    """Tailwind CSS renderer"""

    def render(self, data: Dict[str, Any]) -> str:
        """Render with Tailwind CSS"""
        # Similar structure to Bootstrap but with Tailwind classes
        if data.get('type') == 'page':
            return self._render_page(data)
        return self.render_component(data)

    def render_component(self, data: Dict[str, Any]) -> str:
        """Render component with Tailwind styles"""
        component_type = data.get('type', 'div')

        if component_type == 'card':
            return self._render_card(data)
        elif component_type == 'button':
            return self._render_button(data)

        return f'<div>{data.get("content", "")}</div>'

    def _render_page(self, data: Dict[str, Any]) -> str:
        """Render full page with Tailwind"""
        title = data.get('title', 'PyStructUI App')
        components = data.get('components', [])

        components_html = ''.join([
            self.render_component(c) for c in components
        ])

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    {components_html}
</body>
</html>"""

    def _render_card(self, data: Dict[str, Any]) -> str:
        """Render Tailwind card"""
        title = data.get('title', '')
        body = data.get('body', '')

        return f"""
        <div class="bg-white rounded-lg shadow-md p-6">
            {f'<h3 class="text-xl font-semibold mb-4">{title}</h3>' if title else ''}
            <div>{body}</div>
        </div>"""

    def _render_button(self, data: Dict[str, Any]) -> str:
        """Render Tailwind button"""
        text = data.get('text', 'Button')
        variant = data.get('variant', 'primary')

        colors = {
            'primary': 'bg-blue-500 hover:bg-blue-700',
            'success': 'bg-green-500 hover:bg-green-700',
            'danger': 'bg-red-500 hover:bg-red-700',
        }

        color_classes = colors.get(variant, colors['primary'])

        return f'<button class="{color_classes} text-white font-bold py-2 px-4 rounded">{text}</button>'


class MaterialUIRenderer(Renderer):
    """Material-UI inspired renderer"""

    def render(self, data: Dict[str, Any]) -> str:
        """Render with Material Design principles"""
        # Simplified Material Design implementation
        return f'<div class="mdc-component">{data.get("content", "")}</div>'

    def render_component(self, data: Dict[str, Any]) -> str:
        """Render Material Design component"""
        return f'<div class="mdc-{data.get("type", "container")}">{data.get("content", "")}</div>'