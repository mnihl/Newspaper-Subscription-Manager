from typing import List, Union, Optional
import datetime

from .newspaper import Newspaper
from .editor import Editor
from .subscriber import Subscriber
from .issue import Issue


class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors : List[Editor] = []
        self.subscribers : List[Subscriber] = []

    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance

    def add_newspaper(self, new_paper: Newspaper):
        assert new_paper.paper_id not in [paper.paper_id for paper in self.newspapers], "A newspaper with ID {} already exists".format(new_paper.paper_id)
        self.newspapers.append(new_paper)

    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return None

    def update_newspaper(self, paper_id, data):
        # print(data)
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                paper.update(paper_id, data['name'], data['frequency'], data['price'])
                return paper

    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)
    
    # def list_all_issues(self, paper_id):
    #     for paper in self.newspapers:
    #         if paper.paper_id == paper_id:
    #             return paper.issues

    def specify_editor(self, issue_id, editor_id):
        for paper in self.newspapers:
            for issue in paper.issues:
                if issue.issue_id == issue_id:
                    for editor in self.editors:
                        if editor.editor_id == editor_id:
                            issue.editor = editor
                            editor.issues.append(issue_id)
                            return True
        return False

    def deliver_issue(self, issue_id, subscriber_id):
        for paper in self.newspapers:
            for issue in paper.issues:
                if issue.issue_id == issue_id:
                    for sub in self.subscribers:
                        if sub.subscriber_id == subscriber_id:
                            sub.receive_issue(issue)
                            return True
    
    def get_editor(self, editor_id):
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        return None
    
    def all_editors(self):
        return self.editors
    
    def new_editor(self, editor: Editor):
        self.editors.append(editor)
        return editor

    def update_editor(self, editor_id, name = None, address = None) -> bool:
        editor = self.get_editor(editor_id)
        if editor:
            editor.update(editor_id, name, address)
            return editor
        return False
    
    def delete_editor(self, editor_id):
        editor = self.get_editor(editor_id)
        if editor:
            self.editors.remove(editor)
        return False
    
    def editor_issues(self, editor_id):
        editor = self.get_editor(editor_id)
        if editor:
            return editor.issues
        return None
    
    def get_subscribers(self):
        return self.subscribers
    
    def get_subscriber(self, subscriber_id):
        for sub in self.subscribers:
            if sub.subscriber_id == subscriber_id:
                return sub
        return None
    
    def new_subscriber(self, subscriber: Subscriber):
        self.subscribers.append(subscriber)
        return subscriber
    
    def subscriber_info(self, subscriber_id):
        subscriber = self.get_subscriber(subscriber_id)
        if subscriber:
            return subscriber
        return None
    
    def subscriber_update(self, subscriber_id, name = None, address = None):
        subscriber = self.get_subscriber(subscriber_id)
        if subscriber:
            subscriber.name = name
            subscriber.address = address
            return subscriber
        return False
    
    def delete_subscriber(self, subscriber_id):
        subscriber = self.get_subscriber(subscriber_id)
        if subscriber:
            self.subscribers.remove(subscriber)
            return True
        return False
    
    def subscribe(self, newspaper_id, subscriber_id):
        newspaper = self.get_newspaper(newspaper_id)
        subscriber = self.get_subscriber(subscriber_id)
        if newspaper and subscriber:
            subscriber.subscribe(newspaper)
            return True
        return False
    