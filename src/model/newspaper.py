from typing import List
from flask_restx import Model
from .issue import Issue
from .editor import Editor
# from .agency import Agency
from .subscriber import Subscriber
import datetime
import random


class Newspaper(object):
    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.subscribers = 0
        self.issues: List[Issue] = []

    def list_all_issues(self):
        return self.issues
    
    def create_new_issue(self):
        self.issues.append(Issue(datetime.datetime.now(), random.randint(10, 20)))
    
    def get_issue(self, issue_id):
        for issue in self.issues:
            if issue.issue_id == issue_id:
                return issue
        return None

    def release_issue(self, issue_id):
        issue = self.get_issue(issue_id)
        if issue:
            issue.publish()
            return True
        return False

    # def specify_editor(self, issue_id, editor_id):
    #     issue = self.get_issue(issue_id)
    #     editor = Agency.get_instance().get_editor(editor_id)
    #     if issue and editor:
    #         issue.set_editor(editor)
    #         return True
    #     return False
    
    # def deliver_issue(self, issue_id, subscriber_id):
    #     issue = self.get_issue(issue_id)
    #     subscriber = Agency.get_instance().get_subscriber(subscriber_id)
    #     if issue and subscriber:
    #         subscriber.receive_issue(issue)
    #         return True
    #     return False
    
    def stats(self):
        return {
            "name": self.name,
            "subscribers": self.subscribers,
            "monthly revenue": self.subscribers * self.price,
            "annual revenue": (self.subscribers * self.price) * 12,
        }