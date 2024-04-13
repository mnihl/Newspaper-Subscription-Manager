import pytest

from ...src.model.newspaper import Newspaper
from ...src.model.editor import Editor
from ...src.model.issue import Issue
from ...src.model.subscriber import Subscriber
from ..fixtures import app, client, agency



def test_add_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1


def test_add_newspaper_same_id_should_raise_error(agency):
    agency.newspapers = []
    before = len(agency.newspapers)
    
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)

    # first adding of newspaper should be okay
    agency.add_newspaper(new_paper)

    new_paper2 = Newspaper(paper_id=999,
                          name="Superman Comic",
                          frequency=7,
                          price=13.14)

    with pytest.raises(AssertionError, match='A newspaper with ID 999 already exists'):  # <-- this allows us to test for exceptions
        # this one should raise an exception!
        agency.add_newspaper(new_paper2)

    assert len(agency.all_newspapers()) == before + 1

def test_get_newspaper(agency):
    agency.newspapers = []
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert agency.get_newspaper(999) == new_paper

    #test if it returns None if the newspaper is not found
    assert agency.get_newspaper(1000) == None

def test_update_newspaper(agency):
    agency.newspapers = []
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert agency.get_newspaper(999).name == "Simpsons Comic"
    assert agency.get_newspaper(999).frequency == 7
    assert agency.get_newspaper(999).price == 3.14

    data = {
        'name': 'Superman Comic',
        'frequency': 1,
        'price': 13.14
    }

    updated_paper = agency.update_newspaper(999, data)
    assert updated_paper.name == "Superman Comic"
    assert updated_paper.frequency == 1
    assert updated_paper.price == 13.14

def test_all_newspapers(agency):
    agency.newspapers = []
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    new_paper2 = Newspaper(paper_id=1000,
                          name="Superman Comic",
                          frequency=1,
                          price=13.14)
    agency.add_newspaper(new_paper2)
    assert len(agency.all_newspapers()) == 2
    assert agency.all_newspapers()[0] == new_paper
    assert agency.all_newspapers()[1] == new_paper2

def test_remove_newspaper(agency):
    agency.newspapers = []
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    new_paper2 = Newspaper(paper_id=1000,
                          name="Superman Comic",
                          frequency=1,
                          price=13.14)
    agency.add_newspaper(new_paper2)
    assert len(agency.all_newspapers()) == 2
    agency.remove_newspaper(new_paper)
    assert len(agency.all_newspapers()) == 1
    assert agency.all_newspapers()[0] == new_paper2
    agency.remove_newspaper(new_paper2)
    assert len(agency.all_newspapers()) == 0

def test_specify_editor(agency):
    agency.newspapers = []
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    new_paper.create_new_issue()
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    agency.new_editor(new_editor)
    assert agency.specify_editor(new_paper.issues[0].issue_id, new_editor.editor_id) == True

def test_deliver_issue(agency):
    agency.newspapers = []
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    new_paper.create_new_issue()
    new_issue = new_paper.issues[0]
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Jane Doe",
                                address="1234 Main St")
    agency.new_subscriber(new_subscriber)
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    new_editor.newspapers.append(new_paper)
    new_issue.set_editor(new_editor)
    assert agency.deliver_issue(new_issue.issue_id, new_subscriber.subscriber_id) == True

def test_get_editor(agency):
    agency.editors = []
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    agency.new_editor(new_editor)
    assert agency.get_editor(1) == new_editor
    assert agency.get_editor(2) == None

def test_all_editors(agency):
    agency.editors = []
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    agency.new_editor(new_editor)
    new_editor2 = Editor(editor_id=2,
                        name="Jane Doe",
                        address="1234 Main St")
    agency.new_editor(new_editor2)
    assert len(agency.all_editors()) == 2
    assert agency.all_editors()[0] == new_editor
    assert agency.all_editors()[1] == new_editor2

def test_new_editor(agency):
    agency.editors = []
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    assert agency.new_editor(new_editor) == new_editor

def test_update_editor(agency):
    agency.editors = []
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    agency.new_editor(new_editor)
    assert agency.get_editor(1).name == "John Doe"
    assert agency.get_editor(1).address == "1234 Main St"

    data = {
        'name': 'Jane Doe',
        'address': '5678 Main St'
    }

    updated_editor = agency.update_editor(1, data["name"], data["address"])
    # print(data["name"], data["address"])
    # print(updated_editor.__dict__)
    assert updated_editor.name == "Jane Doe"
    assert updated_editor.address == "5678 Main St"

def test_delete_editor(agency):
    agency.editors = []
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    agency.new_editor(new_editor)
    assert len(agency.all_editors()) == 1
    assert agency.delete_editor(1) == True
    assert len(agency.all_editors()) == 0
    assert agency.delete_editor(1) == False

def test_editor_issues(agency):
    agency.editors = []
    agency.newspapers = []
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    agency.new_editor(new_editor)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    new_paper.create_new_issue()
    new_issue = new_paper.issues[0]
    new_editor.issues.append(new_issue)
    assert agency.editor_issues(1) == [new_issue]

def test_get_subscriber(agency):
    agency.subscribers = []
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Jane Doe",
                                address="1234 Main St")
    agency.new_subscriber(new_subscriber)
    assert agency.get_subscriber(1) == new_subscriber
    assert agency.get_subscriber(2) == None

def test_get_subscribers(agency):
    agency.subscribers = []
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Jane Doe",
                                address="1234 Main St")
    agency.new_subscriber(new_subscriber)
    assert agency.get_subscriber(1) == new_subscriber
    assert agency.get_subscriber(2) == None

def test_new_subscriber(agency):
    agency.subscribers = []
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Jane Doe",
                                address="1234 Main St")
    assert agency.new_subscriber(new_subscriber) == new_subscriber

def test_subscriber_info(agency):
    agency.subscribers = []
    agency.newspapers = []
    agency.editors= []
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Jane Doe",
                                address="1234 Main St")
    agency.new_subscriber(new_subscriber)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    new_subscriber.subscribe(new_paper)
    new_paper.create_new_issue()
    new_issue = new_paper.issues[0]
    new_issue.set_editor(new_editor)
    new_editor.newspapers.append(new_paper)
    new_subscriber.receive_issue(new_issue)
    print(agency.subscriber_info(1).__dict__)
    assert agency.subscriber_info(1).subscriber_id == 1
    assert agency.subscriber_info(1).name == "Jane Doe"
    assert agency.subscriber_info(1).address == "1234 Main St"
    assert len(agency.subscriber_info(1).newspapers) == 1
    assert len(agency.subscriber_info(1).received) == 1
    assert agency.subscriber_info(1).received_history == [{'issue_id': new_issue.issue_id, 'editor': new_editor.name}]

def test_subscriber_update(agency):
    agency.subscribers = []
    new_subscriber = Subscriber(subscriber_id=1,
                                name="John Doe",
                                address="1234 Main St")
    agency.new_subscriber(new_subscriber)
    assert agency.get_subscriber(1).name == "John Doe"
    assert agency.get_subscriber(1).address == "1234 Main St"

    data = {
        'name': 'Jane Doe',
        'address': '5678 Main St'
    }

    updated_subscriber = agency.subscriber_update(1, data["name"], data["address"])
    assert updated_subscriber.name == "Jane Doe"
    assert updated_subscriber.address == "5678 Main St"

def test_delete_subscriber(agency):
    agency.subscribers = []
    new_subscriber = Subscriber(subscriber_id=1,
                                name="John Doe",
                                address="1234 Main St")
    agency.new_subscriber(new_subscriber)
    assert len(agency.get_subscribers()) == 1
    assert agency.delete_subscriber(1) == True
    assert len(agency.get_subscribers()) == 0
    assert agency.delete_subscriber(1) == False

def test_subscribe(agency):
    agency.subscribers = []
    agency.newspapers = []
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Jane Doe",
                                address="1234 Main St")
    agency.new_subscriber(new_subscriber)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(new_subscriber.newspapers) == 0
    assert new_paper.subscribers == 0
    agency.subscribe(999, 1)
    assert len(new_subscriber.newspapers) == 1
    assert new_paper.subscribers == 1

    #newspaper.py tests here
    #had issues with the ID causing tests to wrongly fail when I tried the separate test_newspaper.py file
def test_list_all_issues(agency):
    agency.newspapers = []
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    new_paper.create_new_issue()
    assert new_paper.list_all_issues(new_paper.paper_id) == new_paper.issues

def test_create_new_issue(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    assert len(new_paper.issues) == 0
    new_paper.create_new_issue()
    assert len(new_paper.issues) == 1

def test_get_issue(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_paper.create_new_issue()
    issue = new_paper.issues[0]
    assert new_paper.get_issue(issue.issue_id) == issue
    assert new_paper.get_issue(1000) == None


def test_update_newspaper(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    assert new_paper.name == "Simpsons Comic"
    new_paper.update(new_paper.paper_id, name="The Washington Post")
    assert new_paper.name == "The Washington Post"

def test_release_issue(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_paper.create_new_issue()
    issue = new_paper.issues[0]
    assert issue.released == False
    new_paper.release_issue(issue.issue_id)
    assert issue.released == True

def test_stats(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    assert new_paper.stats()["subscribers"] == 0
    new_paper.subscribers = 10
    assert new_paper.stats()["subscribers"] == 10


#issue.py tests

def test_set_editor(agency):
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    new_issue = Issue(pubdate=20,
                      pages = 20,
                      issue_id=1)
    new_issue.set_editor(new_editor)
    assert new_issue.editor == new_editor

def test_publish(agency):
    new_issue = Issue(pubdate=20,
                      pages = 20,
                      issue_id=1)
    assert new_issue.released == False
    new_issue.publish()
    assert new_issue.released == True

#editor.py tests

def test_update_editor(agency):
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    assert new_editor.name == "John Doe"
    assert new_editor.address == "1234 Main St"
    new_editor.update(1, "Jane Doe", "5678 Main St")
    assert new_editor.name == "Jane Doe"
    assert new_editor.address == "5678 Main St"

#subscriber.py tests
def test_subscribe_subscriber(agency):
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Jane Doe",
                                address="1234 Main St")
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    assert len(new_subscriber.newspapers) == 0
    assert new_paper.subscribers == 0
    new_subscriber.subscribe(new_paper)
    assert len(new_subscriber.newspapers) == 1
    assert new_paper.subscribers == 1

def test_receive_issue(agency):
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Jane Doe",
                                address="1234 Main St")
    new_issue = Issue(pubdate=20,
                      pages = 20,
                      issue_id=1)
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    new_newspaper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_issue.set_editor(new_editor)
    new_editor.newspapers.append(new_newspaper)
    assert len(new_subscriber.received) == 0
    assert len(new_subscriber.received_history) == 0
    new_subscriber.receive_issue(new_issue)
    assert len(new_subscriber.received) == 1
    assert len(new_subscriber.received_history) == 1

def test_subscriber_stats(agency):
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Jane Doe",
                                address="1234 Main St")
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    new_paper2 = Newspaper(paper_id=1000,
                          name="Superman Comic",
                          frequency=1,
                          price=13.14)
    new_subscriber.subscribe(new_paper)
    new_subscriber.subscribe(new_paper2)
    new_issue = Issue(pubdate=20,
                      pages = 20,
                      issue_id=1)
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    new_issue.set_editor(new_editor)
    new_editor.newspapers.append(new_paper)
    new_subscriber.receive_issue(new_issue)
    assert new_subscriber.stats()["name"] == "Jane Doe"
    assert new_subscriber.stats()["address"] == "1234 Main St"
    assert new_subscriber.stats()["subscriptions"] == ["Simpsons Comic", "Superman Comic"]

def test_check_undelivered(agency):
    new_subscriber = Subscriber(subscriber_id=1,
                                name="Jane Doe",
                                address="1234 Main St")
    new_issue = Issue(pubdate=20,
                      pages = 20,
                      issue_id=1)
    agency.deliver_issue(new_issue.issue_id, new_subscriber.subscriber_id)
    assert new_issue.issue_id not in new_subscriber.check_undelivered()