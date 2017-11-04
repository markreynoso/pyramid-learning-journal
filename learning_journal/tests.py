"""Test default.py."""
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPNotFound
from learning_journal.models.meta import Base
from learning_journal.models.mymodel import Blog
from pyramid import testing
import pytest


@pytest.fixture(scope='session')
def configuration(request):
    """Set up a Configurator instance."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/learning_journal'
    })
    config.include("learning_journal.models")
    config.include("learning_journal.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture(scope='session')
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


@pytest.fixture(scope='session')
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session."""
    return testing.DummyRequest(dbsession=db_session)


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


def test_list_view_contains_new_data_added(dummy_request):
    """Test if data sent through the request is added to the db."""
    from learning_journal.views.default import list_view
    new_entry = Blog(
        id=100,
        title='Something Awesome',
        creation_date=11-12-2019,
        body='All the cool things I write.'
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    response = list_view(dummy_request)
    assert new_entry.to_dict() in response['blogs']


def test_detail_view_returns_dict(dummy_request):
    """Test if detail view returns dictionary."""
    from learning_journal.views.default import detail_view
    new_detail = Blog(
        id=101,
        title='Something Awesomer',
        creation_date=11-12-2019,
        body='All the cool things I write.'
    )
    dummy_request.dbsession.add(new_detail)
    dummy_request.dbsession.commit()
    dummy_request.matchdict['id'] = 101
    response = detail_view(dummy_request)
    assert isinstance(response, dict)


def test_detail_view_returns_sinlgle_item(dummy_request):
    """Test if detail view returns dictionary with contents of 'title'."""
    from learning_journal.views.default import detail_view
    new_detail = Blog(
        id=102,
        title='Something Awesomers',
        creation_date=11-12-2019,
        body='All the cool things I write.'
    )
    dummy_request.dbsession.add(new_detail)
    dummy_request.dbsession.commit()
    dummy_request.matchdict['id'] = 102
    response = detail_view(dummy_request)
    assert response['blog']['title'] == 'Something Awesomers'


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


def test_update_view_returns_dict(dummy_request):
    """Test if update view returns a dictionary."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 101
    response = update_view(dummy_request)
    assert isinstance(response, dict)


def test_update_view_returns_title_of_single_entry(dummy_request):
    """Test if update view title of single item chosen."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 102
    response = update_view(dummy_request)
    assert response['blog']['title'] == 'Something Awesomers'


def test_update_view_raises_exception_id_not_found(dummy_request):
    """Test if update raises exception on non-existent id."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 25
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)



# @pytest.fixture
# def testapp():
#     """Initialize test route for testing."""
#     from webtest import TestApp
#     from pyramid.config import Configurator

#     def main():
#         config = Configurator()
#         config.include('pyramid_jinja2')
#         config.include('.routes')
#         config.scan()
#         return config.make_wsgi_app()

#     app = main()
#     return TestApp(app)


# def test_home_route_has_h_two_titles(testapp):
#     """Test if num of titles is same as length of blogs."""
#     from learning_journal.views.default import BLOGS
#     response = testapp.get("/")
#     assert len(BLOGS) == len(response.html.find_all('h2'))


# def test_detail_route_has_one_title(testapp):
#     """Test if num of titles * 2 is same as length of blogs."""
#     response = testapp.get("/journal/1")
#     assert len(response.html.find_all('h2')) == 2


# def test_detail_route_has_text_from_journal(testapp):
#     """Test if detail route return text from served journal."""
#     response = testapp.get("/journal/1")
#     assert "I\'m lamenting the loss of the console" in str(response.html)


# def test_create_route_has_one_item_in_dict(testapp):
#     """Test if create route returns correct entry."""
#     response = testapp.get("/journal/new-entry")
#     assert 'Alright, self, create a awesome blog' in str(response.html)


# def test_update_route_has_one_title(testapp):
#     """Test if update route returns correct entry."""
#     response = testapp.get("/journal/1/edit-entry")
#     assert 'Day 1 Journal' in str(response.html)
