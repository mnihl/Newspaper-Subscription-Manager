
import pytest

from ..src.app import create_app
from ..src.model.agency import Agency
from ..src.model.newspaper import Newspaper
from .testdata import populate
import uuid
# from .testdata import create_newspapers

# create_newspapers()

@pytest.fixture()
def app():
    yield create_app()


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture()
def agency(app):
    agency = Agency.get_instance()
    populate(agency)
    yield agency

paper1 = Newspaper(paper_id=uuid.uuid4().int % 100, name="The New York Times", frequency=7, price=13.14)

@pytest.fixture()
def newspaper(app):
    Agency.get_instance().add_newspaper(paper1)
    newspaper = Agency.get_instance().get_newspaper(paper1.paper_id)
    yield newspaper