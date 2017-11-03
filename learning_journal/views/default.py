"""View functions to serve to routes."""
from pyramid.response import Response
import io
import os

HERE = os.path.dirname(__file__)


def list_view(request):
    """Serve home page html."""
    path = os.path.join(HERE, '../templates/index.html')
    with io.open(path) as imported_text:
        return Response(imported_text.read())


def detail_view(request):
    """Serve single blog to user."""
    path = os.path.join(HERE, '../templates/read.html')
    with io.open(path) as imported_text:
        return Response(imported_text.read())


def create_view(request):
    """Serve page to create new blog post."""
    path = os.path.join(HERE, '../templates/create.html')
    with io.open(path) as imported_text:
        return Response(imported_text.read())


def update_view(request):
    """Serve page to update a single blog entry."""
    path = os.path.join(HERE, '../templates/edit.html')
    with io.open(path) as imported_text:
        return Response(imported_text.read())
