"""Test learning journal."""
from faker import Faker

from learning_journal.models import (Blog, get_tm_session)
from learning_journal.models.meta import Base

from pyramid import testing

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.testing import DummyRequest


import pytest

import transaction


@pytest.fixture(scope='session')
def configuration(request):
    """Set up a Configurator instance."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/test_learning_journal'
    })
    config.include("learning_journal.models")
    config.include("learning_journal.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database."""
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def make_db(dummy_request):
    """Make database for unit tests."""
    new_entry = Blog(
        title='Something Awesome',
        creation_date='November 19, 1955',
        body='All the cool things I write.'
    )
    dummy_request.dbsession.add(new_entry)


def test_list_view_returns_list_of_journals_in_dict(dummy_request):
    """Test if list view returns dictionary with word 'title'."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert isinstance(response, dict)


def test_list_view_returns_empty_dict_with_no_entered_data(dummy_request):
    """Test if list view returns dictionary with nothing in it if empty."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert len(response['blogs']) == 0


def test_list_view_contains_new_data_added(dummy_request, make_db):
    """Test if data sent through the request is added to the db."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert 'title' in response['blogs'][0]


def test_detail_view_returns_dict(dummy_request, make_db):
    """Test if detail view returns dictionary."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert isinstance(response, dict)


def test_detail_view_returns_single_item(dummy_request, make_db):
    """Test if detail view returns dictionary with contents of 'title'."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert response['blog']['title'] == 'Something Awesome'


def test_detail_view_raises_not_found_if_id_not_found(dummy_request):
    """Test if detail raises HTTPNotFound if id not in dict."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 10000
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_create_view_returns_dict(dummy_request):
    """Test if create view returns a dictionary."""
    from learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert isinstance(response, dict)


def test_create_view_returns_empty_dict(dummy_request):
    """Test if create view returns a dictionary."""
    from learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert len(response) == 0


def test_update_view_returns_dict(dummy_request, make_db):
    """Test if update view returns a dictionary."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert isinstance(response, dict)


def test_update_view_returns_title_of_single_entry(dummy_request, make_db):
    """Test if update view title of single item chosen."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert response['blog']['title'] == 'Something Awesome'


def test_update_view_raises_exception_id_not_found(dummy_request):
    """Test if update raises exception on non-existent id."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 25
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


def test_login_view_returns_empty_dict_if_get(dummy_request):
    """Test if login view returns empty dict if get request."""
    from learning_journal.views.default import login_view
    response = login_view(dummy_request)
    assert isinstance(response, dict)


def test_login_view_with_correct_login_return_httpfound(dummy_request):
    """Test if login view returns httpfound with good login."""
    from learning_journal.views.default import login_view
    dummy_request.method = 'POST'
    dummy_request.POST = {
        'username': 'markreynoso',
        'password': 'letmein'
    }
    response = login_view(dummy_request)
    assert isinstance(response, HTTPFound)


def test_login_view_returns_empty_dict_if_bad_login(dummy_request):
    """Test if login view returns empty dict if bad request."""
    from learning_journal.views.default import login_view
    dummy_request.method = 'POST'
    dummy_request.POST = {
        'username': 'markreynoso',
        'password': 'password'
    }
    response = login_view(dummy_request)
    assert response == {}


def test_logout_returns_httpfound(dummy_request):
    """Test logout view returns httpfound page."""
    from learning_journal.views.default import logout
    response = logout(dummy_request)
    assert isinstance(response, HTTPFound)


# ------------ Begin Functional tests ------------

@pytest.fixture(scope="session")
def testapp(request):
    """Setup session to test front end of app."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        config = Configurator()
        settings = {
            'sqlalchemy.url': 'postgres://localhost:5432/test_learning_journal'
        }
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.models')
        config.include('.security')
        config.scan()
        return config.make_wsgi_app()

    app = main()

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)

    return TestApp(app)


@pytest.fixture(scope="session")
def fill_the_db(testapp):
    """Fill the db with dummy data."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(BLOGS)


BLOGS = []


FAKE = Faker()


for i in range(20):
    new_entry = Blog(
        title='journal{}'.format(i),
        creation_date=FAKE.date_time(),
        body='A new entry. {}'.format(FAKE.sentence())
    )
    BLOGS.append(new_entry)


def test_home_route_has_titles(testapp, fill_the_db):
    """Test if home route has all titles from db."""
    response = testapp.get("/")
    # import pdb; pdb.set_trace()
    assert len(BLOGS) == len(response.html.find_all('h2'))


def test_detail_route_with_has_titles(testapp):
    """Test if detail route shows title expected."""
    response = testapp.get("/journal/5")
    assert 'journal' in response.ubody


def test_detail_route_includes_body(testapp):
    """Test if detail route shows title expected."""
    response = testapp.get("/journal/5")
    assert '<body>' in response.ubody


def test_create_route_no_login_is_403(testapp):
    """Test if detail route shows title expected."""
    assert testapp.get("/journal/new-entry", status=403)


def test_edit_route_no_login_is_403(testapp):
    """Test if edit route shows title expected."""
    assert testapp.get("/journal/5/edit-entry", status=403)


def test_create_view_successful_post_redirects_home(testapp):
    """Test create view redirects to home page after submission."""
    testapp.post('/login', {
        'username': 'markreynoso',
        'password': 'letmein',
    })
    csrf = testapp.get('/journal/new-entry').html.\
        find('input', {'type': 'hidden'})['value']
    new_entry = {
        "csrf_token": csrf,
        "title": "All the days",
        "date": 'January 1, 0001',
        "body": 'All tests and no work make mark a dull boy.'
    }
    response = testapp.post("/journal/new-entry", new_entry)
    assert response.location == 'http://localhost/'


def test_create_view_successful_post_actually_shows_on_home_page(testapp):
    """Test create view shows title of new entry on home page on redirect."""
    csrf = testapp.get('/journal/new-entry').html.\
        find('input', {'type': 'hidden'})['value']
    new_entry = {
        "csrf_token": csrf,
        "title": "Journal Me",
        "date": 'January 1, 0002',
        "body": 'All tests and no work make mark a dull boy.'
    }
    response = testapp.post("/journal/new-entry", new_entry)
    next_page = response.follow()
    assert "Journal Me" in next_page.ubody


def test_update_view_successfully_updates_title_on_home_page(testapp):
    """Test update view changes title on home page reroute."""
    csrf = testapp.get('/journal/20/edit-entry').html.\
        find('input', {'type': 'hidden'})['value']
    edit_entry = {
        "csrf_token": csrf,
        "title": "Journal Me, edit",
        "date": 'January 1, 0002',
        "body": 'All tests and no work make mark a dull boy.'
    }
    response = testapp.post("/journal/20/edit-entry", edit_entry)
    next_page = response.follow()
    assert "Journal Me, edit" in next_page.ubody


def test_delete_view_successfully_removes_entry_on_home_page(testapp):
    """Test update view changes title on home page reroute."""
    response = testapp.post("/journal/20/delete")
    next_page = response.follow()
    assert "Journal Me, edit" not in next_page.ubody


def test_delete_view_successfully_removes_all_entries_on_home_page(testapp):
    """Test update view changes title on home page reroute."""
    for i in reversed(range(2 - 20)):
        testapp.post("/journal/{}/delete".format(i))
    response = testapp.post("/journal/1/delete")
    next_page = response.follow()
    assert "<h2>" not in next_page.ubody


def test_logout_routes_to_home_page(testapp):
    """Test logout route takes user to homepage."""
    response = testapp.get('/logout')
    next_page = response.follow()
    assert '<h1>Mark\'s Thoughtful Spot</h1>' in next_page


def test_login_view_with_incorrect_login_returns_login_page(testapp):
    """Test login view routes home with successful login."""
    login = {
        'username': 'markreynoso',
        'password': 'password'
    }
    response = testapp.post("/login", login)
    assert '<h1>Super secret login</h1>' in response.ubody


def test_login_view_with_correct_login_routes_home(testapp):
    """Test login view routes home with successful login."""
    login = {
        'username': 'markreynoso',
        'password': 'letmein'
    }
    response = testapp.post("/login", login)
    assert response.status_int == 302


def test_login_view_get_request_returns_login_page(testapp):
    """Test login page diplays with get request to login view."""
    response = testapp.get('/login')
    assert '<h1>Super secret login</h1>' in response


def test_login_view_with_incorrect_post_login_returns_same_page(testapp):
    """Test login with bad credentials returns login page again."""
    login = {
        'username': 'markr',
        'password': 'letmein'
    }
    response = testapp.post("/login", login)
    assert '<h1>Super secret login</h1>' in response.ubody
