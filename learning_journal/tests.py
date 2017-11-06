"""Test learning journal."""
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPNotFound
from learning_journal.models.meta import Base
from learning_journal.models import (Blog, get_tm_session)
from learning_journal.models.meta import Base
from pyramid import testing
import pytest
import transaction
from faker import Faker


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
        creation_date='November 19, 1955',
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
        title='Something Awesomer',
        creation_date='November 12, 1897',
        body='All the cool things I write.'
    )
    dummy_request.dbsession.add(new_detail)
    dummy_request.dbsession.commit()
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert isinstance(response, dict)

    
def test_detail_view_returns_sinlgle_item(dummy_request):
    """Test if detail view returns dictionary with contents of 'title'."""
    from learning_journal.views.default import detail_view
    new_detail = Blog(
        title='Something Awesomers',
        creation_date='January 1, 0001',
        body='All the cool things I write.'
    )
    dummy_request.dbsession.add(new_detail)
    dummy_request.dbsession.commit()
    dummy_request.matchdict['id'] = 2
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
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert isinstance(response, dict)


def test_update_view_returns_title_of_single_entry(dummy_request):
    """Test if update view title of single item chosen."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 2
    response = update_view(dummy_request)
    assert response['blog']['title'] == 'Something Awesomers'


def test_update_view_raises_exception_id_not_found(dummy_request):
    """Test if update raises exception on non-existent id."""
    from learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 25
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


# @pytest.fixture(scope="session")
# def testapp(request):
#     """Setup session to test front end of app."""
#     from webtest import TestApp
#     from pyramid.config import Configurator

#     def main():
#         config = Configurator()
#         settings = {
#             'sqlalchemy.url': 'postgres://localhost:5432/learning_journal'
#         }
#         config = Configurator(settings=settings)
#         config.include('pyramid_jinja2')
#         config.include('.routes')
#         config.include('learning_journal.routes')
#         config.include('learning_journal.models')
#         config.scan()
#         return config.make_wsgi_app()

#     app = main()

#     SessionFactory = app.registry["dbsession_factory"]
#     engine = SessionFactory().bind
#     Base.metadata.create_all(bind=engine)

#     def tearDown():
#         Base.metadata.drop_all(bind=engine)

#     request.addfinalizer(tearDown)

#     return TestApp(app)


# @pytest.fixture(scope="session")
# def fill_the_db(testapp):
#     """Fill the db with dummy data."""
#     SessionFactory = testapp.app.registry["dbsession_factory"]
#     with transaction.manager:
#         dbsession = get_tm_session(SessionFactory, transaction.manager)
#         dbsession.add_all(BLOGS)


# BLOGS = []


# FAKE = Faker()


# for i in range(20):
#     new_entry = Blog(
#         title='journal{}'.format(i),
#         creation_date=FAKE.date_time(),
#         body='A new entry. {}'.format(FAKE.sentence())
#     )
#     BLOGS.append(new_entry)


# def test_home_route_has_titles(testapp):
#     # from learning_journal.views.default import BLOGS
#     response = testapp.get("/")
#     assert len(BLOGS) == len(response.html.find_all('h2')) - 1
#     assert len(response.html.find_all('title')) == 20


# def test_home_route_with_expenses_has_rows(testapp, fill_the_db):
#     response = testapp.get("/")
#     assert len(response.html.find_all('tr')) == 21


# def test_detail_route_with_expenses_shows_expense_detail(testapp, fill_the_db):
#     response = testapp.get("/expenses/3")
#     assert 'potato2' in response.ubody


# def test_create_view_successful_post_redirects_home(testapp):
#     expense_info = {
#         "title": "Transportation",
#         "amount": 2.75,
#         "due_date": '2017-11-02'
#     }
#     response = testapp.post("/expenses/new-expense", expense_info)
#     assert response.location == 'http://localhost/'


# def test_create_view_successful_post_actually_shows_home_page(testapp):
#     expense_info = {
#         "title": "Booze",
#         "amount": 88.50,
#         "due_date": '2017-11-02'
#     }
#     response = testapp.post("/expenses/new-expense", expense_info)
#     next_page = response.follow()
#     assert "Booze" in next_page.ubody
