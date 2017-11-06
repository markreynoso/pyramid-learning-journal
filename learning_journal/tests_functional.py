"""Test default.py."""
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPNotFound
from learning_journal.models.meta import Base
from learning_journal.models import (Blog, get_tm_session)
from learning_journal.models.meta import Base
from pyramid import testing
import pytest
import transaction
from faker import Faker


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
        # config.include('learning_journal.routes')
        config.include('.models')
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
    response = testapp.get("/")
    assert len(BLOGS) == len(response.html.find_all('h2')) - 1
    assert len(response.html.find_all('title')) == 20


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
