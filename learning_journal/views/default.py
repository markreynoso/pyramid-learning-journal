"""View functions to serve to routes."""
from pyramid.view import view_config
from datetime import datetime
from pyramid.httpexceptions import HTTPNotFound
from learning_journal.models.mymodel import Blog


FMT = '%B %d, %Y'


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
             renderer='learning_journal:templates/create.jinja2')
def create_view(request):
    """Receive request and serves create blog page."""
    # if request.method == "GET":
    #     return {}
    if request.method == "POST":
        if not all([field in request.POST for field in ['title',
                                                        'creation_date',
                                                        'body']]):
            raise HTTPBadRequest
        new_entry = Blog(
            title=request.POST['title'],
            creation_date=request.POST['creation_date'],
            body=datetime.strptime(request.POST['due_date'], '%Y-%m-%d')
        )
        request.dbsession.add(new_expense)
        return HTTPFound(request.route_url('home'))

@view_config(route_name='update',
             renderer='learning_journal:templates/edit.jinja2')
def update_view(request):
    """Receive request and serves edit blog page."""
    blog_id = int(request.matchdict['id'])
    journal_id = int(request.matchdict['id'])
    journal = request.dbsession.query(Blog).get(journal_id)
    if journal:
        return {
            'blog': journal.to_dict()
        }
    raise HTTPNotFound
