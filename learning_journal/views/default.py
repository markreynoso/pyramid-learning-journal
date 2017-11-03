"""View functions to serve to routes."""
from pyramid.view import view_config
from datetime import datetime
from pyramid.httpexceptions import HTTPNotFound
from learning_journal.data.journal_data import BLOGS


FMT = '%m/%d/%Y'


@view_config(route_name='home',
             renderer='learning_journal:templates/index.jinja2')
def list_view(request):
    """Recieve request and serves home page."""
    return {
        "blogs": BLOGS
    }


@view_config(route_name='detail',
             renderer='learning_journal:templates/read.jinja2')
def detail_view(request):
    """Receive request and serves single blog entry page."""
    blog_id = int(request.matchdict['id'])
    if blog_id < 0 or blog_id > len(BLOGS):
        raise HTTPNotFound
    # blog = BLOGS.id[blog_id]
    blog = list(filter(lambda blog: blog['id'] == blog_id, BLOGS))[0]
    return {
        'blog': blog
    }


@view_config(route_name='create',
             renderer='learning_journal:templates/create.jinja2')
def create_view(request):
    """Receive request and serves create blog page."""
    return {
    }


@view_config(route_name='update',
             renderer='learning_journal:templates/edit.jinja2')
def update_view(request):
    """Receive request and serves edit blog page."""
    blog_id = int(request.matchdict['id'])
    if blog_id < 0 or blog_id > len(BLOGS):
        raise HTTPNotFound
    # blog = BLOGS.id[blog_id]
    blog = list(filter(lambda blog: blog['id'] == blog_id, BLOGS))[0]
    return {
        'blog': blog
    }
