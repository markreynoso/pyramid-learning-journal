"""Test default.py."""
from pyramid.testing import DummyRequest
import pytest


def test_list_view_returns_dict():
    """Test if list view returns a dictionary."""
    from learning_journal.views.default import list_view
    req = DummyRequest()
    response = list_view(req)
    assert isinstance(response, dict)


def test_list_view_returns_list_of_journals_in_dict():
    """Test if list view returns list of blogs."""
    from learning_journal.views.default import list_view
    req = DummyRequest()
    response = list_view(req)
    assert 'title' in response['blogs'][0]


def test_create_view_returns_dict():
    """Test if create view returns a dictionary."""
    from learning_journal.views.default import create_view
    req = DummyRequest()
    response = create_view(req)
    assert isinstance(response, dict)


@pytest.fixture
def testapp():
    """Initialize test route for testing."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        config = Configurator()
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main()
    return TestApp(app)


def test_home_route_has_h_two_titles(testapp):
    """Test if num of titles is same as length of blogs."""
    from learning_journal.views.default import BLOGS
    response = testapp.get("/")
    assert len(BLOGS) == len(response.html.find_all('h2'))


def test_detail_route_has_one_title(testapp):
    """Test if num of titles * 2 is same as length of blogs."""
    response = testapp.get("/journal/1")
    assert len(response.html.find_all('h2')) == 2


def test_detail_route_has_text_from_journal(testapp):
    """Test if detail route return text from served journal."""
    response = testapp.get("/journal/1")
    assert "I\'m lamenting the loss of the console" in str(response.html)


def test_create_route_has_one_item_in_dict(testapp):
    """Test if create route returns correct entry."""
    response = testapp.get("/journal/new-entry")
    assert 'Alright, self, create a awesome blog' in str(response.html)


def test_update_route_has_one_title(testapp):
    """Test if update route returns correct entry."""
    response = testapp.get("/journal/1/edit-entry")
    assert 'Day 1 Journal' in str(response.html)
