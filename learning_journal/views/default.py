from pyramid.response import Response
import io
import os

HERE = os.path.dirname(__file__)


def list_view(request):
    """Serve home page html."""
    path = os.path.join(HERE, '../templates/index.html')
    with io.open(path) as imported_text:
        imported_text.read()
    return Response(imported_text)


def detail_view(request):
    """Serve single blog to user."""
    return Response('../templates/read.html')


def create_view(request):
    """Serve page to create new blog post."""
    return Response('../templates/create.html')


def update_view(request):
    """Serve page to update a single blog entry."""
    return Response('../templates/edit.html')
