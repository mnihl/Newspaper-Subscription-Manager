import pytest

from ...src.model.newspaper import Newspaper
from ...src.model.editor import Editor
from ...src.model.issue import Issue
from ...src.model.subscriber import Subscriber
import uuid
from ..fixtures import app, client, agency, newspaper


# def test_list_all_issues(newspaper):
#     assert newspaper.list_all_issues(newspaper.paper_id) == []
#     newspaper.create_new_issue()
#     assert len(newspaper.list_all_issues(newspaper.paper_id)) == 1

# def test_create_new_issue(newspaper):
#     assert len(newspaper.issues) == 0
#     newspaper.create_new_issue()
#     assert len(newspaper.issues) == 1

# def test_get_issue(newspaper):
#     newspaper.create_new_issue()
#     issue = newspaper.issues[0]
#     assert newspaper.get_issue(issue.issue_id) == issue

# def test_update(newspaper):
#     assert newspaper.name == "The New York Times"
#     newspaper.update(newspaper.paper_id, name="The Washington Post")
#     assert newspaper.name == "The Washington Post"