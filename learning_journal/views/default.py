"""View functions to serve to routes."""
from pyramid.view import view_config
from datetime import datetime
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from pyramid.security import remember, forget
from learning_journal.models.mymodel import Blog
from learning_journal.security import is_authenticated


@view_config(route_name='home',
             renderer='learning_journal:templates/index.jinja2')
def list_view(request):
    """Recieve request and serves home page."""
    journals = request.dbsession.query(Blog).all()
    journals = [item.to_dict() for item in journals]
    return {
        "blogs": journals
    }


@view_config(route_name='detail',
             renderer='learning_journal:templates/read.jinja2')
def detail_view(request):
    """Receive request for one journal and returns that journals dict."""
    journal_id = int(request.matchdict['id'])
    journal = request.dbsession.query(Blog).get(journal_id)
    if journal:
        return {
            'blog': journal.to_dict()
        }
    raise HTTPNotFound


@view_config(route_name='create',
             renderer='learning_journal:templates/create.jinja2',
             permission='secret')
def create_view(request):
    """Receive request and serves create blog page."""
    if request.method == "POST":
        if not all([field in request.POST for field in ['title',
                                                        'body']]):
            raise HTTPBadRequest
        new_entry = Blog(
            title=request.POST['title'],
            creation_date=datetime.now().strftime('%B %d, %Y'),
            body=request.POST['body']
        )
        request.dbsession.add(new_entry)
        return HTTPFound(request.route_url('home'))
    return {}


@view_config(route_name='update',
             renderer='learning_journal:templates/edit.jinja2',
             permission='secret')
def update_view(request):
    """Receive request and serves edit blog page."""
    journal_id = int(request.matchdict['id'])
    journal = request.dbsession.query(Blog).get(journal_id)
    if journal:
        if request.method == 'POST' and request.POST:
            journal.title = request.POST['title'],
            journal.body = request.POST['body']
            request.dbsession.flush()
            return HTTPFound(request.route_url('detail', id=journal.id))
        return {
            'blog': journal.to_dict()
        }
    raise HTTPNotFound


@view_config(route_name='delete', permission='secret')
def delete_view(request):
    """Receive request and serves edit blog page."""
    journal_id = int(request.matchdict['id'])
    journal = request.dbsession.query(Blog).get(journal_id)
    if journal:
        request.dbsession.delete(journal)
        return HTTPFound(request.route_url('home'))
    raise HTTPNotFound


@view_config(route_name='login',
             renderer='learning_journal:templates/login.jinja2')
def login_view(request):
    """Receive request and serves edit blog page."""
    if request.method == 'GET':
        return {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if is_authenticated(username, password):
            headers = remember(request, username)
            return HTTPFound(request.route_url('home'), headers=headers)
        return {}


@view_config(route_name='logout')
def logout(request):
    """Receive request and serves edit blog page."""
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
