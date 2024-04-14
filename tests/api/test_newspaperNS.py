# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency
from ...src.model.newspaper import Newspaper
from ...src.model.editor import Editor
from ...src.model.issue import Issue
from ...src.model.subscriber import Subscriber

def test_get_newspaper_should_list_all_papers(client, agency):
    # send request
    response = client.get("/newspaper/")   # <-- note the slash at the end!

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["newspapers"]) == len(agency.newspapers)


def test_add_newspaper(client, agency):
    # prepare
    paper_count_before = len(agency.newspapers)

    # act
    response = client.post("/newspaper/",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response.status_code == 200
    # verify

    assert len(agency.newspapers) == paper_count_before + 1
    # parse response and check that the correct data is here
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["name"] == "Simpsons Comic"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 3.14

    # verify that the newspaper was added to the agency
    paper = agency.get_newspaper(paper_response["paper_id"])
    assert paper is not None

def test_delete_newspaper(client, agency):
    # prepare
    paper_count_before = len(agency.newspapers)
    paper_to_delete = agency.newspapers[0]
    assert paper_to_delete in agency.newspapers
    assert paper_count_before > 0
    assert type(paper_to_delete.paper_id) == int

    response = client.delete(f"/newspaper/{paper_to_delete.paper_id}")

    assert response.status_code == 200
    assert len(agency.newspapers) == paper_count_before - 1
    assert paper_to_delete not in agency.newspapers

def test_get_specific_newspaper(client, agency):
    paper = agency.newspapers[0]

    response = client.get(f"/newspaper/{paper.paper_id}")

    assert response.status_code == 200
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    assert paper_response["name"] == paper.name
    assert paper_response["frequency"] == paper.frequency
    assert paper_response["price"] == paper.price

def test_update_newspaper(client, agency):
    paper = agency.newspapers[0]

    response = client.post(f"/newspaper/{paper.paper_id}",
                           json={
                               "name": "New Name",
                               "frequency": 30,
                               "price": 12.34
                           })

    assert response.status_code == 200
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    assert paper_response["name"] == "New Name"
    assert paper_response["frequency"] == 30
    assert paper_response["price"] == 12.34

    updated_paper = agency.get_newspaper(paper.paper_id)
    assert updated_paper.name == "New Name"
    assert updated_paper.frequency == 30
    assert updated_paper.price == 12.34


#after extensive debugging this test still does not work, despite the method working in Swagger API
#the response.status_code shows up as 200 on the server but not in this test
#the issue functionality works but the tests for them do not get the correct response code
def test_create_new_issue(client, agency):
    paper = agency.newspapers[0]
    issue_count_before = len(paper.issues)

    response = client.post(f"/newspaper/{paper.paper_id}/issue")
    assert response.status_code == 200
    assert len(paper.issues) == issue_count_before + 1

def test_get_issues_of_newspaper(client, agency):
    paper = agency.newspapers[0]
    issue = Issue(pubdate="2020-10-10T00:00:00", pages=10, issue_id=1)
    paper.issues.append(issue)

    response = client.get(f"/newspaper/{paper.paper_id}/issue")

    assert response.status_code == 200
    parsed = response.get_json()
    issues = parsed["issues"]
    assert len(issues) == 1
    print(issues)
    assert issues[0]["pubdate"] == "2020-10-10T00:00:00"
    assert issues[0]["pages"] == 10
    assert issues[0]["issue_id"] == 1

def test_release_issue(client, agency):
    paper = agency.newspapers[0]
    issue = Issue(pubdate="2020-10-10T00:00:00", pages=10, issue_id=1)
    paper.issues.append(issue)

    response = client.post(f"/newspaper/{paper.paper_id}/issue/{issue.issue_id}/release")

    assert response.status_code == 200
    assert issue.published == True

def test_ns_stats(client, agency):
    paper = agency.newspapers[0]
    paper.subscribers = 10

    response = client.get(f"/newspaper/{paper.paper_id}/stats")

    assert response.status_code == 200
    parsed = response.get_json()
    stats = parsed["stats"]

    assert stats["name"] == paper.name
    assert stats["subscribers"] == 10
    assert stats["monthly revenue"] == 10 * paper.price
    assert stats["annual revenue"] == 10 * paper.price * 12

#editorns tests
# def test_get_all_editors(client, agency):
#     editor = Editor(editor_id=1, name="John Doe", address="1234 Elm Street")
#     agency.editors.append(editor)

#     response = client.get("/editor/")

#     assert response.status_code == 200
#     parsed = response.get_json()
#     editors = parsed["editors"]
#     assert len(editors) == 1
#     assert editors[0]["editor_id"] == 1
#     assert editors[0]["name"] == "John Doe"
#     assert editors[0]["address"] == "1234 Elm Street"

def test_create_editor(client, agency):
    editor_count_before = len(agency.editors)

    response = client.post("/editor/",
                           json={
                               "name": "John Doe",
                               "address": "1234 Elm Street"
                           })

    assert response.status_code == 200
    assert len(agency.editors) == editor_count_before + 1
    parsed = response.get_json()
    editor_response = parsed["editor"]

    assert editor_response["name"] == "John Doe"
    assert editor_response["address"] == "1234 Elm Street"