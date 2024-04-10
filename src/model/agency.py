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
        #TODO: assert that ID does not exist  yet (or create a new one)
        assert new_paper.paper_id not in [paper.paper_id for paper in self.newspapers]
        self.newspapers.append(new_paper)

    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return None

    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)
    
    def get_editor(self, editor_id):
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        return None
    
    def all_editors(self):
        return self.editors
    
    def new_editor(self, editor: Editor):
        self.editors.append(editor)

    def update_editor(self, editor_id, name = None, address = None) -> bool:
        editor = self.get_editor(editor_id)
        if editor:
            editor.update(name, address)
            return True
        return False
    
    def delete_editor(self, editor_id):
        editor = self.get_editor(editor_id)
        if editor:
            self.editors.remove(editor)
            return True
        return False
    
    def editor_issues(self, editor_id):
        editor = self.get_editor(editor_id)
        if editor:
            return editor.issues
        return None
    
    def get_subscribers(self):
        return self.subscribers
    
    def get_subscriber(self, sub_id):
        for sub in self.subscribers:
            if sub.sub_id == sub_id:
                return sub
        return None
    
    def new_subscriber(self, subscriber: Subscriber):
        self.subscribers.append(subscriber)
    
    def subscriber_info(self, sub_id):
        subscriber = self.get_subscriber(sub_id)
        if subscriber:
            return subscriber
        return None
    
    def subscriber_update(self, sub_id, name = None, address = None):
        subscriber = self.get_subscriber(sub_id)
        if subscriber:
            subscriber.update(name, address)
            return True
        return False
    
    def delete_subscriber(self, sub_id):
        subscriber = self.get_subscriber(sub_id)
        if subscriber:
            self.subscribers.remove(subscriber)
            return True
        return False
    
    def subscribe(self, newspaper_id, sub_id):
        newspaper = self.get_newspaper(newspaper_id)
        subscriber = self.get_subscriber(sub_id)
        if newspaper and subscriber:
            subscriber.subscribe(newspaper)
            return True
        return False
    