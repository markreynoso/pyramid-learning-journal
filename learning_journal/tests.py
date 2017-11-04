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


def test_journal_exists(dummy_request):
    from learning_journal.views.default import list_view
    new_entry = Blog(
        title='Something Awesome',
        creation_date=11-12-2019,
        body='All the cool things I write.'
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    response = list_view(dummy_request)
    assert new_entry.to_dict() in response['blogs']





# def test_list_view_returns_dict():
#     """Test if list view returns a dictionary."""
#     from learning_journal.views.default import list_view
#     req = DummyRequest()
#     response = list_view(req)
#     assert isinstance(response, dict)


# def test_list_view_returns_list_of_journals_in_dict():
#     """Test if list view returns list of blogs."""
#     from learning_journal.views.default import list_view
#     req = DummyRequest()
#     response = list_view(req)
#     assert 'title' in response['blogs'][0]


# def test_deatil_view_returns_single_journal():
#     """Test if list view returns list of blogs."""
#     from learning_journal.views.default import detail_view
#     req = DummyRequest()
#     req.matchdict['id'] = 1
#     response = detail_view(req)
#     assert 'Day 1 Journal' in response['blog']['title']


# def test_create_view_returns_dict():
#     """Test if create view returns a dictionary."""
#     from learning_journal.views.default import create_view
#     req = DummyRequest()
#     response = create_view(req)
#     assert isinstance(response, dict)


# def test_update_view_returns_dict():
#     """Test if update view returns a dictionary."""
#     from learning_journal.views.default import update_view
#     req = DummyRequest()
#     req.matchdict['id'] = 1
#     response = update_view(req)
#     assert isinstance(response, dict)


# def test_update_view_raises_exception_id_not_found():
#     """Test if update raises exception on non-existent id."""
#     from learning_journal.views.default import update_view
#     req = DummyRequest()
#     req.matchdict['id'] = 20
#     with pytest.raises(HTTPNotFound):
#         update_view(req)


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
